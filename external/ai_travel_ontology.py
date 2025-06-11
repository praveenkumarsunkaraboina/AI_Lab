# -*- coding: utf-8 -*-
"""
AI Travel Ontology - Tourism Recommendation System

This ontology is built from scratch for the tourism domain, incorporating:
- Tourist (profile, preferences)
- Destination (location, attractions, accommodation)
- Activities (categories, durations, costs)
- Environmental factors (weather, season)
- Trip logistics (duration, budget, transportation)

The ontology is represented as a structured knowledge base with relationships
between these entities defined implicitly through the recommendation logic.
"""

import os
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
import requests
from datetime import datetime
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure GROQ_API_KEY is set
if not os.getenv('GROQ_API_KEY'):
    print("Warning: GROQ_API_KEY not found in environment variables.")
    print("Please set your GROQ API key as an environment variable.")
    print("You can create a .env file with: GROQ_API_KEY=your_api_key_here")


# Define the State Type for our Tourism Recommendation Agent
class TourismRecommenderState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "The messages in the conversation"]
    tourist_profile: Dict[str, Any]  # Age group, travel style, etc.
    travel_date: str  # Date of travel
    destination: str  # City or location
    duration: int  # Number of days
    start_date: str  # Start date of the trip
    budget: str  # Budget category
    interests: List[str]  # Tourist interests
    weather_info: Dict[str, Any]  # Weather information
    accommodation_preference: str  # Hotel preference
    hotel_info: Dict[str, Any]  # Hotel information
    itinerary: str  # Generated itinerary
    feedback: str  # User feedback on itinerary
    feedback_rating: str  # Simple rating (awesome/good/ok)
    iteration: int  # Number of iterations for itinerary generation


# Set up the LLM
llm = ChatGroq(
    temperature=0.3,  # Reduced temperature for more consistent output
    model_name="llama-3.3-70b-versatile"
)

# Initialize tools
search_tool = DuckDuckGoSearchRun()


def get_weather_info(destination: str, visit_date: str, duration: int):
    """Get weather data for the destination using DuckDuckGo Search and process with LLM."""
    try:
        search_query = f"weather forecast {destination} {visit_date}"
        search_results = search_tool.run(search_query)
        print("Raw search results:", search_results[:200], "...")

        # First try direct regex extraction from search results
        # Extract temperature
        temp_patterns = [
            r'temperature of (\d+)°?[CF]',  # "temperature of 29°C"
            r'(\d+)°[CF]',                  # "29°C"
            r'(\d+) ?degrees?'              # "29 degrees"
        ]

        current_temp = "Not available"
        for pattern in temp_patterns:
            temp_match = re.search(pattern, search_results, re.IGNORECASE)
            if temp_match:
                current_temp = f"{temp_match.group(1)}°C"
                break

        # Extract conditions
        conditions = "Variable"
        condition_keywords = {
            'mist': 'Misty',
            'fog': 'Foggy',
            'rain': 'Rainy',
            'shower': 'Showers',
            'overcast': 'Overcast',
            'cloudy': 'Cloudy',
            'sunny': 'Sunny',
            'clear': 'Clear',
            'partly cloudy': 'Partly Cloudy'
        }

        search_lower = search_results.lower()
        for keyword, condition in condition_keywords.items():
            if keyword in search_lower:
                conditions = condition
                break

        # Extract forecast info
        forecast = "Variable conditions expected"
        if 'shower' in search_lower or 'rain' in search_lower:
            forecast = "Expect rain or showers"
        elif 'overcast' in search_lower:
            forecast = "Overcast skies expected"
        elif 'mist' in search_lower:
            forecast = "Misty conditions likely"

        print(f"Direct extraction: Temp={current_temp}, Conditions={conditions}")

        # Try LLM extraction as backup only if direct extraction failed
        if current_temp == "Not available":
            print("Trying LLM extraction as backup...")

            weather_extraction_prompt = ChatPromptTemplate.from_messages([
                ("system", """Look at the weather search results and extract:
                1. Current temperature (just the number and unit like "29°C")
                2. Weather condition (one word like Sunny, Cloudy, Rainy, Misty)
                3. Brief forecast (max 10 words)

                Return format:
                Temperature: [temp]
                Condition: [condition]
                Forecast: [forecast]"""),
                ("user", "Weather data: {text}")
            ])

            try:
                extraction_response = llm.invoke(
                    weather_extraction_prompt.format_messages(text=search_results[:1000])
                )

                llm_response = extraction_response.content
                print(f"LLM response: {llm_response}")

                # Parse LLM response
                temp_match = re.search(r'Temperature:\s*([^\n]+)', llm_response)
                cond_match = re.search(r'Condition:\s*([^\n]+)', llm_response)
                fore_match = re.search(r'Forecast:\s*([^\n]+)', llm_response)

                if temp_match:
                    current_temp = temp_match.group(1).strip()
                if cond_match:
                    conditions = cond_match.group(1).strip()
                if fore_match:
                    forecast = fore_match.group(1).strip()

            except Exception as llm_error:
                print(f"LLM extraction failed: {llm_error}")

        return {
            "city": destination,
            "summary": f"Weather for {destination}: {current_temp}, {conditions}",
            "current_temp": current_temp,
            "conditions": conditions,
            "forecast": forecast,
            "raw_search_results": search_results[:500] + "..." if len(search_results) > 500 else search_results
        }

    except Exception as e:
        print(f"Weather fetch error: {e}")
        return {
            "city": destination,
            "summary": f"Weather information unavailable for {destination}",
            "current_temp": "Not available",
            "conditions": "Check local weather",
            "forecast": "Please check local weather services",
            "error": str(e)
        }


def get_hotel_recommendations(destination, preference):
    """Get hotel recommendations without relying on JSON parsing."""
    try:
        search_query = f"best {preference} hotels {destination} booking"
        print(f"Searching for {preference} hotels in {destination}...")
        results = search_tool.run(search_query)
        print("Raw search results:", results[:200], "...")

        # Use structured prompts for individual fields
        name_prompt = ChatPromptTemplate.from_messages([
            ("system", "Extract the hotel name or general hotel type from the search results. Return only the name, nothing else."),
            ("user", f"Search results for {preference} hotels in {destination}:\n{results}")
        ])

        price_prompt = ChatPromptTemplate.from_messages([
            ("system", "Extract price range from the search results. Return only the price range with currency (e.g., ₹2000-5000 per night), nothing else."),
            ("user", f"Search results for {preference} hotels in {destination}:\n{results}")
        ])

        amenities_prompt = ChatPromptTemplate.from_messages([
            ("system", "List 3-5 common amenities from the search results. Return as comma-separated list (e.g., WiFi, AC, Restaurant), nothing else."),
            ("user", f"Search results for {preference} hotels in {destination}:\n{results}")
        ])

        # Get individual responses
        try:
            name_response = llm.invoke(name_prompt.format_messages()).content.strip()
            name = name_response if name_response else f"{preference.title()} hotels in {destination}"
        except:
            name = f"{preference.title()} hotels in {destination}"

        try:
            price_response = llm.invoke(price_prompt.format_messages()).content.strip()
            price_range = price_response if price_response else get_default_price_range(preference)
        except:
            price_range = get_default_price_range(preference)

        try:
            amenities_response = llm.invoke(amenities_prompt.format_messages()).content.strip()
            amenities = [a.strip() for a in amenities_response.split(',') if a.strip()]
            if not amenities:
                amenities = ["WiFi", "Room service", "Air conditioning"]
        except:
            amenities = ["WiFi", "Room service", "Air conditioning"]

        return {
            "name": name,
            "price_range": price_range,
            "rating": "Check booking platforms for current ratings",
            "amenities": amenities,
            "raw_search_results": results[:500] + "..." if len(results) > 500 else results
        }

    except Exception as e:
        print(f"Hotel search error: {e}")
        return {
            "name": f"{preference.title()} accommodations in {destination}",
            "price_range": get_default_price_range(preference),
            "rating": "Check booking platforms",
            "amenities": ["Basic amenities", "WiFi", "Room service"],
            "error": str(e)
        }


def get_default_price_range(preference):
    """Get default price range based on preference."""
    price_ranges = {
        "budget": "₹800-2000 per night",
        "mid-range": "₹2000-5000 per night",
        "luxury": "₹5000+ per night"
    }
    return price_ranges.get(preference, "₹2000-5000 per night")


# Define Prompt Templates
profile_prompt = """Based on the following information, generate a tourist profile summary:
- Age group: {age_group}
- Travel style: {travel_style}
- Previous travel experience: {experience}

Create a brief profile that will help tailor tourism recommendations."""

itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a tourism recommendation expert with deep knowledge of destinations worldwide.

    Create a personalized travel itinerary based on the following information:

    TOURIST PROFILE:
    {tourist_profile}

    DESTINATION: {destination}
    DURATION: {duration} days
    BUDGET: {budget}
    INTERESTS: {interests}

    WEATHER INFO:
    {weather_info}

    ACCOMMODATION:
    {hotel_info}

    Create a detailed day-by-day itinerary that includes:
    1. Morning, afternoon, and evening activities
    2. Recommended local food experiences
    3. Transportation suggestions between attractions
    4. Estimated costs for activities
    5. Tips based on current weather conditions

    Format the itinerary in a clear, readable structure with days clearly marked.
    """),
    ("user", "Please generate my personalized travel itinerary.")
])


# Node Functions for the Graph
def collect_tourist_profile(state: TourismRecommenderState) -> TourismRecommenderState:
    """Collect basic tourist profile information."""
    print("\n===== TOURIST PROFILE =====")

    print("\nWhat is your age group?")
    print("1. 18-25")
    print("2. 26-40")
    print("3. 41-60")
    print("4. 60+")
    age_choice = input("Enter the number of your choice: ")
    age_map = {"1": "18-25", "2": "26-40", "3": "41-60", "4": "60+"}
    age_group = age_map.get(age_choice, "26-40")

    print("\nWhat is your travel style?")
    print("1. Adventure seeker")
    print("2. Cultural explorer")
    print("3. Relaxation oriented")
    print("4. Luxury traveler")
    print("5. Budget backpacker")
    style_choice = input("Enter the number of your choice: ")
    style_map = {
        "1": "Adventure seeker",
        "2": "Cultural explorer",
        "3": "Relaxation oriented",
        "4": "Luxury traveler",
        "5": "Budget backpacker"
    }
    travel_style = style_map.get(style_choice, "Cultural explorer")

    print("\nHow would you describe your travel experience?")
    print("1. Novice (first time traveling)")
    print("2. Occasional traveler")
    print("3. Experienced traveler")
    print("4. Expert globetrotter")
    exp_choice = input("Enter the number of your choice: ")
    exp_map = {
        "1": "Novice",
        "2": "Occasional traveler",
        "3": "Experienced traveler",
        "4": "Expert globetrotter"
    }
    experience = exp_map.get(exp_choice, "Occasional traveler")

    try:
        # Generate a profile summary using LLM
        profile_summary = llm.invoke(
            profile_prompt.format(
                age_group=age_group,
                travel_style=travel_style,
                experience=experience
            )
        ).content
    except Exception as e:
        print(f"Error generating profile: {e}")
        profile_summary = f"Tourist profile: {age_group}, {travel_style}, {experience} traveler"

    tourist_profile = {
        "age_group": age_group,
        "travel_style": travel_style,
        "experience": experience,
        "summary": profile_summary
    }

    return {
        **state,
        "tourist_profile": tourist_profile,
        "messages": state["messages"] + [AIMessage(content=f"Tourist profile created: {profile_summary}")],
        "iteration": 1
    }


def collect_destination_info(state: TourismRecommenderState) -> TourismRecommenderState:
    """Collect destination and trip details."""
    print("\n===== DESTINATION & TRIP DETAILS =====")

    destination = input("\nEnter the destination city you want to visit: ")

    print("\nHow many days will you be staying?")
    duration_str = input("Enter number of days: ")
    try:
        duration = int(duration_str)
    except ValueError:
        duration = 3
        print(f"Using default duration of {duration} days")

    print("\nWhat is your budget level for this trip?")
    print("1. Budget (economy)")
    print("2. Mid-range")
    print("3. Luxury")
    budget_choice = input("Enter the number of your choice: ")
    budget_map = {"1": "budget", "2": "mid-range", "3": "luxury"}
    budget = budget_map.get(budget_choice, "mid-range")

    print("\nWhat are your interests for this trip? (comma-separated)")
    print("Examples: history, food, nature, shopping, museums, adventure, relaxation, nightlife")
    interests_input = input("Enter your interests: ")
    interests = [interest.strip() for interest in interests_input.split(",")]

    return {
        **state,
        "destination": destination,
        "duration": duration,
        "budget": budget,
        "interests": interests,
        "messages": state["messages"] + [AIMessage(content=f"Destination details collected for {destination}, {duration} days, {budget} budget")],
    }


def get_weather_data(state: TourismRecommenderState) -> TourismRecommenderState:
    """Get weather information for the destination."""
    print("\n===== WEATHER INFORMATION =====")
    print(f"\nChecking current weather in {state['destination']}...")
    print(f"\nEnter the date of your travel to check Weather Conditions:")
    visit_date = input("Enter date (YYYY-MM-DD): ")

    weather_info = get_weather_info(state['destination'], visit_date, state['duration'])

    print(f"Current temperature: {weather_info['current_temp']}")
    print(f"Conditions: {weather_info['conditions']}")
    print(f"Forecast: {weather_info['forecast']}")

    return {
        **state,
        "visit_date": visit_date,
        "weather_info": weather_info,
        "messages": state["messages"] + [AIMessage(content=f"Weather information retrieved for {state['destination']}")],
    }


def get_accommodation_info(state: TourismRecommenderState) -> TourismRecommenderState:
    """Collect accommodation preferences and get recommendations."""
    print("\n===== ACCOMMODATION PREFERENCES =====")

    print("\nWhat type of accommodation are you looking for?")
    print("1. Budget (hostel, guesthouse)")
    print("2. Mid-range (3-star hotel)")
    print("3. Luxury (4-5 star hotel)")
    acc_choice = input("Enter the number of your choice: ")
    acc_map = {"1": "budget", "2": "mid-range", "3": "luxury"}
    accommodation_preference = acc_map.get(acc_choice, "mid-range")

    hotel_info = get_hotel_recommendations(state['destination'], accommodation_preference)

    print(f"\nFound: {hotel_info['name']}")
    print(f"Price range: {hotel_info['price_range']}")
    print(f"Rating: {hotel_info['rating']}")
    print(f"Amenities: {', '.join(hotel_info['amenities'])}")

    return {
        **state,
        "accommodation_preference": accommodation_preference,
        "hotel_info": hotel_info,
        "messages": state["messages"] + [AIMessage(content=f"Recommended accommodation: {hotel_info['name']}")],
    }


def generate_itinerary(state: TourismRecommenderState) -> TourismRecommenderState:
    """Generate a personalized itinerary using the LLM."""
    print("\n===== GENERATING PERSONALIZED ITINERARY =====")
    print(f"Creating itinerary for {state['destination']} ({state['duration']} days)...")

    weather_info_str = f"Temperature: {state['weather_info']['current_temp']}, Conditions: {state['weather_info']['conditions']}, Forecast: {state['weather_info']['forecast']}"
    hotel_info_str = f"Accommodation: {state['hotel_info']['name']}, {state['hotel_info']['price_range']}, {state['hotel_info']['rating']}"

    try:
        response = llm.invoke(
            itinerary_prompt.format_messages(
                tourist_profile=state['tourist_profile']['summary'],
                destination=state['destination'],
                duration=state['duration'],
                budget=state['budget'],
                interests=', '.join(state['interests']),
                weather_info=weather_info_str,
                hotel_info=hotel_info_str
            )
        )
        itinerary = response.content
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        itinerary = f"Basic itinerary for {state['destination']} ({state['duration']} days) - Please check local tourism websites for detailed planning."

    print("\n===== YOUR PERSONALIZED ITINERARY =====\n")
    print(itinerary)

    return {
        **state,
        "itinerary": itinerary,
        "messages": state["messages"] + [AIMessage(content=itinerary)],
    }


def collect_feedback(state: TourismRecommenderState) -> TourismRecommenderState:
    """Collect user feedback on the generated itinerary."""
    print("\n===== FEEDBACK =====")
    print("What do you think about this itinerary?")
    print("Type 'awesome' if you love it, 'good' if it's fine, or 'ok' if you want changes:")

    feedback = input("Your feedback (awesome/good/ok): ").strip().lower()

    print("Any specific comments or suggestions for improvement?")
    additional_comments = input("Additional comments (optional): ")

    full_feedback = f"Rating: {feedback}. Additional comments: {additional_comments}"

    return {
        **state,
        "feedback": full_feedback,
        "feedback_rating": feedback,
        "messages": state["messages"] + [HumanMessage(content=full_feedback)],
    }


def analyze_feedback(state: TourismRecommenderState) -> dict:
    """Analyze user feedback and determine next steps based on simple keywords."""
    print("\n===== ANALYZING FEEDBACK =====")

    feedback_rating = state.get("feedback_rating", "").strip().lower()

    if feedback_rating in ["awesome", "good"]:
        print("Great! You seem happy with the itinerary.")
        return {"next": "end"}
    else:
        print("Let's refine the itinerary based on your feedback.")
        return {"next": "refine_itinerary"}


def refine_itinerary(state: TourismRecommenderState) -> TourismRecommenderState:
    """Refine the itinerary based on user feedback."""
    print("\n===== REFINING ITINERARY =====")
    print("Based on your feedback, we'll create an improved itinerary.")

    iteration = state["iteration"] + 1

    print("\nPlease tell us what specific aspects you'd like to change:")
    refinement_requests = input("What would you like to change? ")

    refinement_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a tourism recommendation expert.

        REFINE the following travel itinerary based on user feedback:

        ORIGINAL ITINERARY:
        {original_itinerary}

        USER FEEDBACK:
        {feedback}

        SPECIFIC CHANGES REQUESTED:
        {refinement_requests}

        DESTINATION: {destination}
        DURATION: {duration} days
        BUDGET: {budget}
        INTERESTS: {interests}

        Create an IMPROVED day-by-day itinerary that addresses the feedback.
        """),
        ("user", "Please generate my refined travel itinerary.")
    ])

    try:
        response = llm.invoke(
            refinement_prompt.format_messages(
                original_itinerary=state["itinerary"],
                feedback=state["feedback"],
                refinement_requests=refinement_requests,
                destination=state['destination'],
                duration=state['duration'],
                budget=state['budget'],
                interests=', '.join(state['interests'])
            )
        )
        refined_itinerary = response.content
    except Exception as e:
        print(f"Error refining itinerary: {e}")
        refined_itinerary = "Unable to refine itinerary automatically. Please consult local tourism resources."

    print("\n===== YOUR REFINED ITINERARY =====\n")
    print(refined_itinerary)

    return {
        **state,
        "itinerary": refined_itinerary,
        "messages": state["messages"] + [AIMessage(content=refined_itinerary)],
        "iteration": iteration
    }


def finalize_itinerary(state: TourismRecommenderState) -> TourismRecommenderState:
    """Finalize the itinerary and provide a summary."""
    print("\n===== FINAL ITINERARY =====")
    print("Thank you for using our Tourism Recommendation System!")
    print(f"Your {state['duration']}-day itinerary for {state['destination']} is ready.")
    print("The itinerary is: ")
    print(state["itinerary"])

    try:
        summary_prompt = ChatPromptTemplate.from_messages([
            ("system", """Summarize the key highlights of this travel itinerary in 3-5 bullet points:

            {itinerary}

            Format as concise bullet points starting with emoji indicators.
            """),
            ("user", "Please summarize this travel itinerary.")
        ])

        summary_response = llm.invoke(
            summary_prompt.format_messages(itinerary=state["itinerary"])
        )

        print("\n===== ITINERARY HIGHLIGHTS =====")
        print(summary_response.content)
    except Exception as e:
        print(f"Error generating summary: {e}")
        print("\n===== ITINERARY HIGHLIGHTS =====")
        print("• Personalized recommendations based on your preferences")
        print("• Budget-friendly activities and accommodations")
        print("• Local cultural experiences and attractions")

    print("\nWe hope you enjoy your trip!")

    return {
        **state,
        "messages": state["messages"] + [AIMessage(content="Trip planning completed successfully!")],
    }


# Create and compile the graph
def create_tourism_recommendation_system():
    """Create the tourism recommendation system graph."""
    workflow = StateGraph(TourismRecommenderState)

    # Add nodes
    workflow.add_node("collect_tourist_profile", collect_tourist_profile)
    workflow.add_node("collect_destination_info", collect_destination_info)
    workflow.add_node("get_weather_data", get_weather_data)
    workflow.add_node("get_accommodation_info", get_accommodation_info)
    workflow.add_node("generate_itinerary", generate_itinerary)
    workflow.add_node("collect_feedback", collect_feedback)
    workflow.add_node("analyze_feedback", analyze_feedback)
    workflow.add_node("refine_itinerary", refine_itinerary)
    workflow.add_node("finalize_itinerary", finalize_itinerary)

    # Set entry point
    workflow.set_entry_point("collect_tourist_profile")

    # Define edges
    workflow.add_edge("collect_tourist_profile", "collect_destination_info")
    workflow.add_edge("collect_destination_info", "get_weather_data")
    workflow.add_edge("get_weather_data", "get_accommodation_info")
    workflow.add_edge("get_accommodation_info", "generate_itinerary")
    workflow.add_edge("generate_itinerary", "collect_feedback")
    workflow.add_conditional_edges(
        "analyze_feedback",
        lambda x: x["next"],
        {
            "refine_itinerary": "refine_itinerary",
            "end": "finalize_itinerary"
        }
    )
    workflow.add_edge("collect_feedback", "analyze_feedback")
    workflow.add_edge("refine_itinerary", "collect_feedback")
    workflow.add_edge("finalize_itinerary", END)

    return workflow.compile()


def run_tourism_recommendation_system():
    """Run the Tourism Recommendation System."""
    print("=" * 50)
    print("WELCOME TO THE TOURISM RECOMMENDATION SYSTEM")
    print("=" * 50)
    print("\nThis system will help you plan your perfect trip based on your preferences.")

    state = {
        "messages": [],
        "tourist_profile": {},
        "destination": "",
        "duration": 0,
        "budget": "",
        "interests": [],
        "weather_info": {},
        "accommodation_preference": "",
        "hotel_info": {},
        "itinerary": "",
        "feedback": "",
        "feedback_rating": "",
        "iteration": 0
    }

    app = create_tourism_recommendation_system()

    # Execute the graph
    for output in app.stream(state):
        pass


# Main execution
if __name__ == "__main__":
    run_tourism_recommendation_system()
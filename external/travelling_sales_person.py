import random

def route_distance(route, dist_matrix,start_city):
    """
    Given a route (which does NOT include the starting city) and the distance matrix,
    compute the total distance of traveling:
    start_city -> route[0] -> route[1] -> ... -> route[-1] -> start_city
    """
    total_dist=0
    current_city = start_city
    for next_city in route:
        total_dist+=dist_matrix[(current_city,next_city)]
        current_city=next_city
    
    total_dist+=dist_matrix[(current_city,start_city)]
    return total_dist

def generate_2opt_neighbors(route):
    """
    Generate all 2-opt neighbors for a given route.
    A 2-opt move reverses the order of cities between two indices,
    effectively removing two edges and reconnecting them in a different way.
    """
    neighbors=[]
    for i in range(len(route)-1):
        for j in range(i+1,len(route)):
            new_route=route[:]
            new_route[i:j+1]=list(reversed(new_route[i:j+1]))
            neighbors.append(new_route)
    return neighbors

def hill_climb(route, dist_matrix,start_city):
    """
    Perform hill climbing on the TSP route using 2-opt neighbors.
    Returns the best route (excluding the start city) and its total distance.
    """
    current_route = route
    current_dist = route_distance(current_route,dist_matrix,start_city)
    while True:
        improved=False
        neighbors = generate_2opt_neighbors(current_route)
        for neighbor in neighbors:
            dist_neighbor = route_distance(neighbor,dist_matrix,start_city)
            if dist_neighbor<current_dist:
                current_route=neighbor
                current_dist=dist_neighbor
                improved=True
                break
        if not improved:
            break
    return current_route, current_dist

def main():
    num_cities=int(input("Enter the number of cities:"))
    dist_matrix={}
    print("Enter the distances between cities (e.g., 0,1,20 0,2,10 1,2,15 ...):")
    distances_input = input().split()
    for dist_str in distances_input:
        city1, city2, distance = dist_str.split(",")
        city1,city2,distance=int(city1),int(city2),int(distance)
        dist_matrix[(city1,city2)]=distance
        dist_matrix[(city2,city1)]=distance

    start_city = int(input("Enter the starting city (0 to {}):".format(num_cities-1)))

    cities = list(range(num_cities))
    cities.remove(start_city)

    random.shuffle(cities) # initial route

    best_route,best_distance = hill_climb(cities,dist_matrix,start_city)

    print("Best route (excluding start city {}): {}".format(start_city, best_route))
    print("Distance of this route:", best_distance)
    full_path = [start_city] + best_route + [start_city]
    print("Full path:", full_path)

if __name__=="__main__":
    main()

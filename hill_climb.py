import random

dist_matrix = {
    (0, 1): 20, (1, 0): 20,
    (0, 2): 10, (2, 0): 10,
    (0, 3): 15, (3, 0): 15,
    (1, 2): 15, (2, 1): 15,
    (1, 3): 11, (3, 1): 11,
    (2, 3): 17, (3, 2): 17,
}

def route_distance(route, dist_matrix, start_city):
    """
    Given a route (which does NOT include the starting city) and the distance matrix,
    compute the total distance of traveling:
    start_city -> route[0] -> route[1] -> ... -> route[-1] -> start_city
    """
    total_dist = 0
    current_city = start_city
    for next_city in route:
        total_dist += dist_matrix[(current_city, next_city)]
        current_city = next_city
    
    # Return to the starting city
    total_dist += dist_matrix[(current_city, start_city)]
    return total_dist

def generate_2opt_neighbors(route):
    """
    Generate all 2-opt neighbors for a given route.
    A 2-opt move reverses the order of cities between two indices,
    effectively removing two edges and reconnecting them in a different way.
    """
    neighbors = []
    for i in range(len(route) - 1):
        for j in range(i + 1, len(route)):
            new_route = route[:]            # Make a copy of the current route
            new_route[i:j+1] = reversed(new_route[i:j+1])
            neighbors.append(new_route)
    return neighbors

def hill_climb(route, dist_matrix, start_city):
    """
    Perform hill climbing on the TSP route using 2-opt neighbors.
    Returns the best route (excluding the start city) and its total distance.
    """
    current_route = route
    current_dist = route_distance(current_route, dist_matrix, start_city)

    while True:
        improved = False
        neighbors = generate_2opt_neighbors(current_route)
        for neighbor in neighbors:
            dist_neighbor = route_distance(neighbor, dist_matrix, start_city)
            if dist_neighbor < current_dist:
                current_route = neighbor
                current_dist = dist_neighbor
                improved = True
                break  # Accept the first improvement
        if not improved:
            # print("No Better Neighbor Found!!")
            break
    
    return current_route, current_dist

def main():
    # --- For start city 0 ---
    # Route excludes start city 0, so use the remaining cities.
    cities = [1, 2, 3]
    random.shuffle(cities)
    best_route, best_distance = hill_climb(cities, dist_matrix, start_city=0)
    print("Best route (excluding start city 0):", best_route)
    print("Distance of this route:", best_distance)
    full_path = [0] + best_route + [0]
    print("Full path:", full_path, "\n")

    # --- For start city 1 ---
    # Route excludes start city 1, so use the remaining cities.
    cities = [0, 2, 3]
    random.shuffle(cities)
    best_route, best_distance = hill_climb(cities, dist_matrix, start_city=1)
    print("Best route (excluding start city 1):", best_route)
    print("Distance of this route:", best_distance)
    full_path = [1] + best_route + [1]
    print("Full path:", full_path, "\n")

    # --- For start city 2 ---
    # Route excludes start city 2, so use the remaining cities.
    cities = [0, 1, 3]
    random.shuffle(cities)
    best_route, best_distance = hill_climb(cities, dist_matrix, start_city=2)
    print("Best route (excluding start city 2):", best_route)
    print("Distance of this route:", best_distance)
    full_path = [2] + best_route + [2]
    print("Full path:", full_path)

if __name__ == "__main__":
    main()

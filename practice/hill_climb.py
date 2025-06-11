import random

dist_matrix={
    (0, 1): 20, (1, 0): 20,
    (0, 2): 10, (2, 0): 10,
    (0, 3): 15, (3, 0): 15,
    (1, 2): 15, (2, 1): 15,
    (1, 3): 11, (3, 1): 11,
    (2, 3): 17, (3, 2): 17,
}

def route_distance(route, dist_matrix,start_city):
    total_dist=0
    curr_city=start_city
    for next_city in route:
        total_dist+=dist_matrix[(curr_city,next_city)]
        curr_city=next_city
    total_dist+=dist_matrix[(curr_city,start_city)]
    return total_dist

def generate_2opt_neighbors(route):
    neighbors=[]
    for i in range(len(route)-1):
        for j in range(i+1,len(route)):
            new_route=route[:]
            new_route[i:j+1]=reversed(new_route[i:j+1])
            neighbors.append(new_route)
    
    return neighbors

def hill_climb(route, dist_matrix,start_city):
    curr_route=route
    current_dist=route_distance(curr_route,dist_matrix,start_city)

    while True:
        improved=False
        neighbors=generate_2opt_neighbors(curr_route)
        for neighbor in neighbors:
            dist_neighbor=route_distance(neighbor,dist_matrix,start_city)
            if dist_neighbor<current_dist:
                curr_route=neighbor
                current_dist=dist_neighbor
                improved=True
                break
        if not improved:
            break

    return curr_route, current_dist

def main():
    cities=[1,2,3]
    random.shuffle(cities)
    best_route, best_distance=hill_climb(cities,dist_matrix,start_city=0)
    print("Best route (excluding start city 0):",best_route)
    print("Distance of this route:",best_distance)
    full_path=[0]+best_route+[0]
    print("Full Path:",full_path,"\n")

    cities = [0, 2, 3]
    random.shuffle(cities)
    best_route, best_distance = hill_climb(cities, dist_matrix, start_city=1)
    print("Best route (excluding start city 1):", best_route)
    print("Distance of this route:", best_distance)
    full_path = [1] + best_route + [1]
    print("Full path:", full_path, "\n")

    cities = [0, 1, 3]
    random.shuffle(cities)
    best_route, best_distance = hill_climb(cities, dist_matrix, start_city=2)
    print("Best route (excluding start city 2):", best_route)
    print("Distance of this route:", best_distance)
    full_path = [2] + best_route + [2]
    print("Full path:", full_path)

if __name__ == "__main__":
    main()


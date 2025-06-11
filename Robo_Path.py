import heapq

# Define the heuristic function (Manhattan Distance)
def heuristic(start_row, start_col, end_row, end_col):
    return abs(start_row - end_row) + abs(start_col - end_col)

# A* algorithm to find the optimal path
def robo_path(start_row, start_col, end_row, end_col, matrix, directions_map, m, n):
    # Priority queue to store the nodes to be explored (f, g, row, col)
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start_row, start_col, end_row, end_col), 0, start_row, start_col))
    
    # A dictionary to store the best path to each cell
    came_from = {}
    g_score = { (start_row, start_col): 0 }  # Cost to reach each cell
    
    # Direction mappings for (U, D, L, R) -> (Up, Down, Left, Right)
    direction_map = {
        'U': (-1, 0),  # Up
        'D': (1, 0),   # Down
        'L': (0, -1),  # Left
        'R': (0, 1)    # Right
    }
    
    while open_list:
        # Get the cell with the lowest f value
        f, g, current_row, current_col = heapq.heappop(open_list)
        
        # If we reached the goal
        if (current_row, current_col) == (end_row, end_col):
            print("Path found!")
            path = []
            while (current_row, current_col) in came_from:
                path.append((current_row, current_col))
                current_row, current_col = came_from[(current_row, current_col)]
            path.append((start_row, start_col))
            path.reverse()
            for (r, c) in path:
                print(f"({r}, {c})")
            return
        
        # Explore neighbors based on valid directions for the current cell
        valid_directions = directions_map[(current_row, current_col)]
        for direction in valid_directions:
            # Map the direction to actual movement
            delta_row, delta_col = direction_map[direction]
            neighbor_row = current_row + delta_row
            neighbor_col = current_col + delta_col
            
            # Check if the neighbor is within bounds and not an obstacle
            if 0 <= neighbor_row < m and 0 <= neighbor_col < n and matrix[neighbor_row][neighbor_col] != 1:
                tentative_g = g + 1  # The cost to reach the neighbor is always 1
                
                # If this path to the neighbor is better, update the scores
                if (neighbor_row, neighbor_col) not in g_score or tentative_g < g_score[(neighbor_row, neighbor_col)]:
                    g_score[(neighbor_row, neighbor_col)] = tentative_g
                    f = tentative_g + heuristic(neighbor_row, neighbor_col, end_row, end_col)
                    heapq.heappush(open_list, (f, tentative_g, neighbor_row, neighbor_col))
                    came_from[(neighbor_row, neighbor_col)] = (current_row, current_col)
    
    # If we exhaust the open list and don't find a path
    print("Path not found.")

# Main function
def main():
    m = int(input("Enter the number of rows:\n"))
    n = int(input("Enter the number of columns:\n"))
    
    # Create matrix with obstacles (assuming 0 is open space; adjust if needed)
    print("Enter the elements of the matrix:")
    matrix = [[0 for j in range(n)] for i in range(m)]
    
    # Dictionary to store valid directions for each cell
    directions_map = {}
    
    # Input valid directions for each cell
    print("Enter valid directions for each cell (U for up, D for down, L for left, R for right):")
    for i in range(m):
        for j in range(n):
            # Use split() to avoid extra spaces being included
            directions = input(f"Enter directions for cell ({i}, {j}): ").upper().split()
            directions_map[(i, j)] = directions
    
    # Get the start and goal positions
    start_row = int(input("Enter the start row:\n"))
    start_col = int(input("Enter the start column:\n"))
    goal_row = int(input("Enter the goal row:\n"))
    goal_col = int(input("Enter the goal column:\n"))
    
    # Call the pathfinding function
    robo_path(start_row, start_col, goal_row, goal_col, matrix, directions_map, m, n)

# Run the main function
if __name__ == '__main__':
    main()

import heapq

def manhattan_heuristic(start_row, start_col, end_row, end_col):
    return abs(start_row - end_row) + abs(start_col - end_col)

def chebyshev_heuristic(start_row, start_col, end_row, end_col):
    return max(abs(start_row - end_row), abs(start_col - end_col))

def robo_path(start_row, start_col, end_row, end_col, matrix, directions_map, m, n, heuristic):
    open_list = []
    heapq.heappush(open_list, (heuristic(start_row, start_col, end_row, end_col), 0, start_row, start_col))
    
    came_from = {}
    g_score = {(start_row, start_col): 0}
    
    direction_map = {
        'U': (-1, 0),  # Up
        'D': (1, 0),   # Down
        'L': (0, -1),  # Left
        'R': (0, 1)    # Right
    }
    
    while open_list:
        f, g, current_row, current_col = heapq.heappop(open_list)
        
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
            return path
        
        valid_directions = directions_map[(current_row, current_col)]
        for direction in valid_directions:
            delta_row, delta_col = direction_map[direction]
            neighbor_row = current_row + delta_row
            neighbor_col = current_col + delta_col
            
            if 0 <= neighbor_row < m and 0 <= neighbor_col < n and matrix[neighbor_row][neighbor_col] != 1:
                tentative_g = g_score[(current_row, current_col)] + 1  # Correct g score calculation
                if (neighbor_row, neighbor_col) not in g_score or tentative_g < g_score[(neighbor_row, neighbor_col)]:
                    g_score[(neighbor_row, neighbor_col)] = tentative_g
                    f = tentative_g + heuristic(neighbor_row, neighbor_col, end_row, end_col)
                    heapq.heappush(open_list, (f, neighbor_row, neighbor_col))  # Correct push to open_list
                    came_from[(neighbor_row, neighbor_col)] = (current_row, current_col)
    
    print("Path not found.")
    return None

def main():
    m = int(input("Enter the number of rows:\n"))
    n = int(input("Enter the number of columns:\n"))
    
    print("Enter the elements of the matrix (0 or 1, separated by spaces):")
    matrix = []
    for i in range(m):
        row = list(map(int, input().split()))
        matrix.append(row)
    
    # Dictionary to store valid directions for each cell
    directions_map = {}
    
    print("Enter valid directions for each cell (U for up, D for down, L for left, R for right), separated by spaces:")
    for i in range(m):
        for j in range(n):
            directions = input(f"Enter directions for cell ({i}, {j}): ").upper().split()
            directions_map[(i, j)] = directions
    
    # Get the start and goal positions
    start_row = int(input("Enter the start row:\n"))
    start_col = int(input("Enter the start column:\n"))
    goal_row = int(input("Enter the goal row:\n"))
    goal_col = int(input("Enter the goal column:\n"))
    
    # Choose which heuristic to use
    choice = input("Choose heuristic (1 for Manhattan, 2 for Chebyshev): ")
    if choice == '1':
        heuristic = manhattan_heuristic
        print("Using Manhattan Distance:")
    else:
        heuristic = chebyshev_heuristic
        print("Using Chebyshev Distance:")
    
    # Call the pathfinding function
    path = robo_path(start_row, start_col, goal_row, goal_col, matrix, directions_map, m, n, heuristic)
    
    if path:
        print("Path found:")
        for r, c in path:
            print(f"({r}, {c})")

# Run the main function
if __name__ == '__main__':
    main()
from collections import deque

def solve_missionaries_cannibals():
    """Solve missionaries and cannibals puzzle using BFS"""
    # State: (missionaries_left, cannibals_left, boat_position)
    # boat_position: 0=left, 1=right
    start = (3, 3, 0)  # All on left side
    goal = (0, 0, 1)   # All on right side, boat on right
    
    queue = deque([(start, [])])  # (state, path_of_moves)
    visited = {start}
    
    while queue:
        (ml, cl, boat), path = queue.popleft()
        
        # Check if goal reached
        if (ml, cl, boat) == goal:
            return path
        
        # Generate all possible moves (1 or 2 people in boat)
        for m in range(3):      # 0, 1, or 2 missionaries
            for c in range(3):  # 0, 1, or 2 cannibals
                if 1 <= m + c <= 2:  # Boat capacity constraint
                    # Calculate new state after move
                    if boat == 0:  # Moving left to right
                        new_ml, new_cl, new_boat = ml - m, cl - c, 1
                    else:          # Moving right to left  
                        new_ml, new_cl, new_boat = ml + m, cl + c, 0
                    
                    # Check bounds and safety
                    if (0 <= new_ml <= 3 and 0 <= new_cl <= 3 and
                        (new_ml == 0 or new_ml >= new_cl) and      # Left safe
                        (new_ml == 3 or (3-new_ml) >= (3-new_cl)) # Right safe
                       ):
                        new_state = (new_ml, new_cl, new_boat)
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, path + [(m, c)]))
    
    return None  # No solution

# Solve and display
solution = solve_missionaries_cannibals()
if solution:
    print("Missionaries and Cannibals Solution:")
    state = [3, 3, 0]  # Track current state for display
    
    for i, (m, c) in enumerate(solution):
        boat_side = "left" if state[2] == 0 else "right" 
        target_side = "right" if state[2] == 0 else "left"
        
        print(f"Step {i+1}: Move {m}M + {c}C from {boat_side} to {target_side}")
        
        # Update state
        if state[2] == 0:  # Boat moving left to right
            state[0] -= m; state[1] -= c; state[2] = 1
        else:              # Boat moving right to left
            state[0] += m; state[1] += c; state[2] = 0
            
        print(f"        Left: {state[0]}M {state[1]}C | Right: {3-state[0]}M {3-state[1]}C")
        print()
else:
    print("No solution found!")
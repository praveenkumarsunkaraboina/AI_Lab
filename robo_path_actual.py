import heapq

# Grid size
ROWS, COLS = 4, 6
START, GOAL = (2, 1), (2, 4)

# Obstacles represented as blocked edges
OBSTACLES = {
    ((1, 1), (1, 2)), ((2, 1), (2, 2)), ((3, 1), (3, 2)),
    ((0, 5), (1, 5)), ((0, 4), (1, 4))
}

# Movement directions for different distance types
MOVES = {
    "manhattan": [(-1, 0), (1, 0), (0, -1), (0, 1)],  # Up, Down, Left, Right
    "chebyshev": [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Includes diagonals
}

def is_valid_move(curr, nxt, dist_type):
    r,c = nxt
    if not (0<=r<ROWS) or not(0<=c< COLS) or tuple(sorted([curr,nxt])) in OBSTACLES:
        return False
    if dist_type=='chebyshev' and abs(curr[0]-nxt[0]) ==1 and abs(curr[1]-nxt[1])==1 :
        mid1 = (curr[0],nxt[1])
        mid2 = (nxt[0],curr[1])
        
        return is_valid_move(curr,mid1,"manhattan") and is_valid_move(curr,mid2,"manhattan")
    return True

def heuristic(curr, goal, dist_type):
    """Calculates heuristic (h) based on Manhattan or Chebyshev distance."""
    return abs(curr[0]-goal[0])+abs(curr[1]-goal[1]) if dist_type == "manhattan" else max(abs(curr[0]-goal[0]),abs(curr[1]-goal[1]))

def a_star(start, goal, dist_type):
    """A* algorithm for pathfinding with Manhattan and Chebyshev distances."""
    queue = [(0, start)]  # Priority queue (f-score, node)
    parent = {start: None}
    g = {start: 0}  # Cost from start to each node

    while queue:
        cost, node = heapq.heappop(queue)  # Get node with lowest f-score
        if node == goal:
            path = []
            while node:
                path.append(node)
                node = parent[node]
            return path[::-1], g[goal]  # Return shortest path & total cost

        for dr, dc in MOVES[dist_type]:
            nxt = (node[0] + dr, node[1] + dc)
            if not is_valid_move(node, nxt, dist_type):
                continue

            step_cost = 1 if (dr, dc) in MOVES["manhattan"] else 2**0.5  # Cost for diagonal moves
            total_cost = g[node] + step_cost  # g(n) = cost from start to current node

            if nxt not in g or total_cost < g[nxt]:  # If new path is shorter, update
                g[nxt] = total_cost
                parent[nxt] = node
                heapq.heappush(queue, (total_cost + heuristic(nxt, goal, dist_type), nxt))  # f = g + h

    return None, float('inf')  # If no path found

# Run A* for both distance metrics
manhattan_path, manhattan_distance = a_star(START, GOAL, "manhattan")
chebyshev_path, chebyshev_distance = a_star(START, GOAL, "chebyshev")

# Print results
print("Shortest Path (Manhattan):", manhattan_path)
print("Total Distance (Manhattan):", manhattan_distance)
print("Shortest Path (Chebyshev):", chebyshev_path)
print("Total Distance (Chebyshev):", chebyshev_distance)
import heapq

ROWS, COLS = 4,6
start_x=2
start_y=1
goal_x=2
goal_y=4
START, GOAL = (start_x,start_y), (goal_x,goal_y)

# Obstacles represented as blocked edges
OBSTACLES = {
    ((1, 1), (1, 2)), ((2, 1), (2, 2)), ((3, 1), (3, 2)),
    ((0, 5), (1, 5)), ((0, 4), (1, 4))
}

MOVES={
    "manhattan":[(-1,0),(1,0),(0,-1),(0,1)],
    "chebyshev":[(-1,0),(1,0),(0,-1),(0,1),(1,-1),(-1,1),(-1,-1),(1,1)]
}

def is_valid_move(curr,nxt,dist_type):
    r,c =nxt
    if not (0<=r<=ROWS) or not(0<=c<=COLS) or tuple(sorted([curr,nxt])) in OBSTACLES:
        return False
    if dist_type=='chebyshev' and abs(curr[0]-nxt[0])==1 and abs(curr[1]-nxt[1])==1:
        mid1=(curr[0],nxt[1])
        mid2=(nxt[0],curr[1])

        return is_valid_move(curr,mid1,"manhattan") and is_valid_move(curr,mid2,"manhattan")
    return True

def heuristic(curr,goal,dist_type):
    return abs(curr[0]-goal[0])+abs(curr[1]-goal[1]) if dist_type=="manhattan" else max(abs(curr[0]-goal[0]),abs(curr[1]-goal[1]))

def a_star(start,goal,dist_type):
    queue = [(heuristic(start,goal,dist_type),start,0,[start])]
    vis=set()
    while queue:
        h_x,node,cost,curr_path = heapq.heappop(queue)
        if node in vis:
            continue
        vis.add(node)
        path = curr_path+[node]
        if node == goal:
            return path, cost
        for dr,dc in MOVES[dist_type]:
            nxt = (node[0]+dr,node[1]+dc)
            if not is_valid_move(node,nxt,dist_type):
                continue

            step_cost = 1 if (dr,dc) in MOVES["manhattan"] else 2**0.5
            total_cost = cost+step_cost
            heapq.heappush(queue, (total_cost+heuristic(nxt,goal,dist_type),nxt,total_cost,curr_path+[nxt]))
    return None, float('inf')


# Run A* for both distance metrics
manhattan_path, manhattan_distance = a_star(START, GOAL, "manhattan")
chebyshev_path, chebyshev_distance = a_star(START, GOAL, "chebyshev")

# Print results
print("Shortest Path (Manhattan):", manhattan_path)
print("Total Distance (Manhattan):", manhattan_distance)
print("Shortest Path (Chebyshev):", chebyshev_path)
print("Total Distance (Chebyshev):", chebyshev_distance)

    


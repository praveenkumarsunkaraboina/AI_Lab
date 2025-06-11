import heapq
from collections import deque
graph = {
    0: [(1, 2), (2, 1)],
    1: [(0, 2),(2,5),(3,11),(4,3)],
    2: [(0,1),(1,5),(4,1),(5,15)],
    3: [(1,11),(4,2),(6,1)],
    4: [(1,3),(2,1),(3,2),(5,4),(6,5)],
    5: [(2,15),(4,4),(6,1)],
    6:[(3,1),(4,5),(5,1)]
}

heuristics ={
    0:1,
    1:3,
    2:15,
    3:2,
    4:1,
    5:float('inf'),
    6:0
}

def a_star_search(graph,heuristics,start,goal):
    nodes_gen=0
    vis=set()
    pq=[(0,start,[start],0)]
    nodes_gen=nodes_gen+1
    total_cost=float('inf')
    path=[]
    while pq:
        curr_cost, curr_node, curr_path, total_path_cost = heapq.heappop(pq)
        if curr_node in vis:
            continue
        vis.add(curr_node)

        if curr_node == goal:
            print("Total Path Cost:",total_path_cost)
            return curr_path, nodes_gen

        
        for neighbor, weight in graph[curr_node]:
            if neighbor not in vis:
                tentative_cost = total_path_cost + weight
                heuristic = heuristics[neighbor]
                f = tentative_cost + heuristic
                nodes_gen=nodes_gen+1
                heapq.heappush(pq, (f, neighbor, curr_path+[neighbor], tentative_cost))
    return path, nodes_gen

def uniform_cost_search(graph,start,goal):
    pq=[(0,start)]
    visited=set()
    parent={start:None}
    cost_so_far = {start: 0}
    nodes_gen=1
    actual_cost = float('inf')
    actual_path=[]
    while pq:
        cost, node=heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            path=[]
            while node:
                path.append(node)
                node=parent[node]
            
            path.reverse()
            if actual_cost>cost:
                actual_cost=cost
                actual_path=path
            continue
        
        for neighbor, weight in graph.get(node,[]):
            new_cost = cost + weight
            if new_cost < cost_so_far.get(neighbor, float('inf')):
                cost_so_far[neighbor] = new_cost
                nodes_gen+=1
                heapq.heappush(pq,(new_cost,neighbor))
                parent[neighbor]=node
    
    return actual_path, nodes_gen

def dfs(graph, start_node, goal_node, result=None, vis=None, nodes_gen=0):
    if result is None:
        result = []
    if vis is None:
        vis = set()
    
    result.append(start_node)
    vis.add(start_node)
    nodes_gen += 1 
    if start_node==goal_node:
        return result, nodes_gen

    for neighbor, _ in graph.get(start_node, []):
        if neighbor not in vis:
            nodes_gen = dfs(graph, neighbor, goal_node, result, vis, nodes_gen)[1]
    
    return result, nodes_gen

def bfs(graph,start_node,goal_node):
    q=deque([start_node])
    result=[]
    vis=set()
    nodes_gen=1
    while q:
        curr=q.popleft()
        if curr not in vis:
            result.append(curr)
            vis.add(curr)
            if curr==goal_node:
                return result, nodes_gen
        for neigh, _ in graph.get(curr, []): 
            if neigh not in vis:
                q.append(neigh)
                nodes_gen += 1 
    
    return result, nodes_gen

def main():
    start_node = int(input("Enter the start node: "))
    goal_node = int(input("Enter the goal node: ")) 
    a_star_path, a_star_nodes_gen = a_star_search(graph, heuristics, start_node, goal_node)
    # a_star_cost = 0
    # for i in range(len(a_star_path)-1):
    #     current_node = a_star_path[i]
    #     next_node = a_star_path[i+1]
    #     # Find the weight for the edge between current_node and next_node
    #     for neighbor, weight in graph[current_node]:
    #         if neighbor == next_node:
    #             a_star_cost += weight
    #             break
    print(f"A* search found the path: {a_star_path}")

    print("Comparing with DFS, BFS, UCS based on number of nodes generated: ")

    dfs_nodes_gen = dfs(graph, start_node, goal_node)[1]
    bfs_nodes_gen = bfs(graph, start_node, goal_node)[1]
    ucs_nodes_gen = uniform_cost_search(graph, start_node, goal_node)[1]

    print(f"No. of nodes generated for DFS: {dfs_nodes_gen}")
    print(f"No. of nodes generated for BFS: {bfs_nodes_gen}")
    print(f"No. of nodes generated for UCS: {ucs_nodes_gen}")
    print(f"No. of nodes generated for A*: {a_star_nodes_gen}")

if __name__ == "__main__":
    main()
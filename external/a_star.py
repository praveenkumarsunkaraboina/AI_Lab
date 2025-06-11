import heapq
from collections import deque

def a_star_search(graph,heuristics,start,goal):
    nodes_gen=0
    vis=set()
    pq=[(heuristics[start],start,[start],0)]
    nodes_gen+=1
    while pq:
        curr_f,curr_node,curr_path,total_path_cost=heapq.heappop()
        if curr_node in vis:
            continue
        vis.add(curr_node)

        if curr_node==goal:
            print("Total path Cost:",total_path_cost)
            return curr_path, nodes_gen
        
        for neighbor, weight in graph.get(curr_node,[]):
            if neighbor not in vis:
                tentative_cost = total_path_cost+weight
                heuristic = heuristics[neighbor]
                f=tentative_cost+heuristic
                nodes_gen+=1
                heapq.heappush(pq,(f,neighbor,curr_path+[neighbor],tentative_cost))
    
    return [],nodes_gen

def uniform_cost_search(graph,start,goal):
    pq=[(0,start,[start])]
    vis=set()
    cost_so_far = {start: 0}  # Initialize cost_so_far
    nodes_gen=0
    while pq:
        cost,node,path=heapq.heappop(pq)
        nodes_gen+=1

        if node in vis:
            continue
        vis.add(node)

        if node==goal:
            return path, nodes_gen
        
        for neighbor, weight in graph.get(node,[]):
            new_cost=cost+weight
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:  # Check cost_so_far
                cost_so_far[neighbor] = new_cost  # Update cost_so_far
                new_path=path+[neighbor]
                heapq.heappush(pq,(new_cost,neighbor,new_path))

    return [],nodes_gen

def dfs(graph,start_node,goal_node,result=None,vis=None,nodes_gen=0):
    if result is None:
        result=[]
    if vis is None:
        vis=set()

    result.append(start_node)
    vis.add(start_node)

    nodes_gen+=1

    if start_node == goal_node:
        return result, nodes_gen
    for neighbor, _ in graph.get(start_node,[]):
        if neighbor not in vis:
            new_result, nodes_gen = dfs(graph,neighbor,goal_node,result,vis,nodes_gen)
            if new_result:
                return new_result, nodes_gen
    
    return [],0


def bfs(graph, start_node,goal_node):
    q=deque([(start_node,[start_node])])
    vis=set()
    nodes_gen=0

    while q:
        node,path = q.popleft()
        nodes_gen+=1

        if node in vis:
            continue
        vis.add(node)

        if node == goal_node:
            return path, nodes_gen
        
        for neighbor, _ in graph.get(node,[]):
            if neighbor not in vis:
                new_path =path+[neighbor]
                q.append((neighbor,new_path))

    return [],nodes_gen

def main():
    graph={}
    num_nodes = int(input("Enter the number of nodes in the graph:"))
    for i in range(num_nodes):
        node = input(f"Enter the name of node {i+1}:")
        neighbors_str = input(f"Enter the neighbors of {node} in the formaat 'neigh1,weight1")
        neighbors=[]
        if neighbors_str:
            neighbors_list=neighbors_str.split()
            for neighbor_info in neighbors_list:
                neigh, weight = neighbor_info.split(",")
                neighbors.append((neigh,int(weight)))
        graph[node]=neighbors

    heuristics={}
    for node in graph:
        heuristic_value = int(input(f"Enter heuristic value for node {node}:"))
        heuristics[node]=heuristic_value

    start_node = input("Enter the start node: ")
    goal_node = input("Enter the goal node: ")

    a_star_path, a_star_nodes_gen = a_star_search(graph, heuristics, start_node, goal_node)
    print(f"A* search found the path: {a_star_path}")
    
    print("Comparing with DFS, BFS, UCS based on number of nodes generated: ")

    dfs_path, dfs_nodes_gen = dfs(graph, start_node, goal_node)
    bfs_path, bfs_nodes_gen = bfs(graph, start_node, goal_node)
    ucs_path, ucs_nodes_gen = uniform_cost_search(graph, start_node, goal_node)

    print(f"No. of nodes generated for DFS: {dfs_nodes_gen}")
    print(f"No. of nodes generated for BFS: {bfs_nodes_gen}")
    print(f"No. of nodes generated for UCS: {ucs_nodes_gen}")
    print(f"No. of nodes generated for A*: {a_star_nodes_gen}")


if __name__ == "__main__":
    main()


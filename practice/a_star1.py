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
    nodes_gen+=1
    path=[]
    while pq:
        curr_cost, curr_node,curr_path,total_path_cost=heapq.heappop(pq)
        if curr_node in vis:
            continue
        vis.add(curr_node)

        if curr_node==goal:
            print("Total Path Cost:", total_path_cost)
            return curr_path, nodes_gen
        
        for neighbor, weight in graph[curr_node]:
            if neighbor not in vis:
                tentaive_cost=total_path_cost+weight
                heuristic=heuristics[neighbor]
                f_score=tentaive_cost+heuristic
                nodes_gen+=1
                heapq.heappush(pq,(f_score,neighbor,curr_path+[neighbor],tentaive_cost))
    return path, nodes_gen

def uniform_cost_search(graph,start,goal):
    pq=[(0,start)]
    vis=set()
    parent={start:None}
    cost_so_far={start:0}
    nodes_gen=1
    actual_cost=float('inf')
    actual_path=[]
    while pq:
        cost, node=heapq.heappop(pq)
        if node in vis:
            continue
        vis.add(node)

        if node==goal:
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
            new_cost=cost+weight
            if new_cost<cost_so_far.get(neighbor,float('inf')):
                cost_so_far[neighbor]=new_cost
                nodes_gen+=1
                parent[neighbor]=node
                heapq.heappush(pq,(new_cost,neighbor))

    return actual_path, nodes_gen


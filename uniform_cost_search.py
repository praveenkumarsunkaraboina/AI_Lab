import heapq

graph={
    'S':[('d',3),('e',9),('p',1)],
    'b':[('a',2)],
    'a':[],
    'd':[('b',1),('c',8),('e',2)],
    'c':[('a',float('inf'))],
    'e':[('h',8),('r',2)],
    'h':[('p',float('inf')),('q',float('inf'))],
    'f':[('G',2),('c',float('inf'))],
    'r':[('f',1)],
    'G':[],
    'p':[('q',15)],
    'q':[]
}

def uniform_cost_search(graph,start,goal):
    pq=[(0,start)]
    visited=set()
    parent={start:None}
    cost_so_far = {start: 0}

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
                heapq.heappush(pq,(new_cost,neighbor))
                parent[neighbor]=node
    
    return actual_cost, actual_path


start_node ='S'
goal_node='G'

cost, path = uniform_cost_search(graph,start_node,goal_node)

print(f"Minimum Cost: {cost}")

print(f"Optimal Path:{'->'.join(path)}")
import heapq

def uniform_cost_search(graph,start,goal):
    pq=[(0,start)]
    visited=set()
    parent={start:None}
    cost_so_far={start:0}

    actual_cost = float('inf')
    actual_path=[]
    while pq:
        cost, node = heapq.heappop(pq)
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
            break

        for neighbor, weight in graph.get(node,[]):
            new_cost = cost+weight
            if neighbor not in cost_so_far or new_cost<cost_so_far.get(neighbor,float('inf')):
                cost_so_far[neighbor]=new_cost
                heapq.heappush(pq,(new_cost,neighbor))
                parent[neighbor]=node

        return actual_cost, actual_path
    
if __name__=="__main__":
    graph={}
    num_nodes=int(input("Enter the number of nodes in the graph:"))
    for i in range(num_nodes):
        node = input(f"Enter the name of node {i + 1}: ")
        neighbors_str = input(f"Enter the neighbors of {node} in the format 'neighbor1,weight1 neighbor2,weight2': ")
        neighbors=[]
        if neighbors_str:
            neighbors_list=neighbors_str.split()
            for neighbor_info in neighbors_list:
                neighbor, weight = neighbor_info.split(",")
                neighbors.append((neighbor,float(weight)))
            graph[node]=neighbors
    
    start_node = input("Enter the start node:")
    goal_node = input("Enter the goal node:")

    cost, path = uniform_cost_search(graph,start_node,goal_node)

    print(f"Minimum Cost: {cost}")
    print(f"Optimal Path: {'->'.join(path)}")

from collections import deque

def create_graph():
    graph={}
    n=int(input("Enter the number of nodes:\n"))
    for i in range(0,n):
        print(f"Enter node {i+1}")
        node=input()
        neighbors=input(f"Enter the neighbors of {node} with space seperation:\n").split()
        graph[node]=neighbors
    return graph

def bfs(graph,start_node):
    q=deque([start_node])
    result=[]
    vis=set()
    while q:
        curr=q.popleft()
        if curr not in vis:
            result.append(curr)
            vis.add(curr)
            q.extend(neighbor for neighbor in graph[curr] if neighbor not in vis)
    
    return result

def main():
    graph=create_graph()
    print("Enter the startnode of the bfs traversal:\n")
    start_node=input()
    print("BFS Traversal is :\n")
    bfs_list=bfs(graph,start_node)
    print("->".join(bfs_list))

if __name__=="__main__":
    main()

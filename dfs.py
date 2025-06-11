def create_graph():
    graph={}
    n=int(input("Enter the number of nodes in graph:\n"))
    for i in range(0,n):
        print(f"Enter the node {i+1}:\n")
        node=input()
        neighbors=input(f"Enter the neighbors of {node} (space separated): ").split()
        graph[node]=neighbors
    return graph

def dfs(graph,start_node,result=None,vis=None):
    if result is None:
        result=[]
    if vis is None:
        vis=set()
    
    result.append(start_node)
    vis.add(start_node)

    for neigh in graph[start_node]:
        if neigh not in vis:
            dfs(graph,neigh,result,vis)
        
    return result


def main():
    graph = create_graph()
    start_node = input("Enter the starting node for traversal:")

    print("\nPerforming DFS:")
    dfs_result=dfs(graph,start_node)
    print("DFS Traversal:","->".join(dfs_result))


if __name__ == "__main__":
    main()

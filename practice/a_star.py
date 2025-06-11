import heapq

# A* Search
def a_star_search(graph, start, goal, heuristic_values):
    pq = [(0, start, [], 0)]  # (priority, node, path, cost)
    nodes = 1  # Number of nodes generated
    while pq:
        current_cost, current_node, current_path, total_path_cost = heapq.heappop(pq)
        if current_node == goal:
            print("A* Search - Number of nodes expanded:", nodes)
            return current_path + [current_node]
        for neighbor, weight in graph[current_node]:
            if neighbor not in current_path:
                new_cost = total_path_cost + weight
                new_heuristic = heuristic_values[neighbor]
                new_path = current_path + [current_node]
                heapq.heappush(pq, (new_cost + new_heuristic, neighbor, new_path, new_cost))
                nodes += 1
    return None

# BFS Search
def bfs(graph, start, goal):
    queue = [(start, [])]  # (node, path)
    nodes = 1  # Number of nodes generated
    visited = set()
    visited.add(start)
    while queue:
        current_node, path = queue.pop(0)
        if current_node == goal:
            print("BFS Search - Number of nodes expanded:", nodes)
            return path + [current_node]
        for neighbor, weight in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [current_node]))
                nodes += 1
    return None

# DFS Search
def dfs(graph, node, goal, visited, path, nodes):
    if node == goal:
        return path + [node]
    visited.add(node)
    for neighbor, weight in graph[node]:
        if neighbor not in visited:
            nodes[0] += 1
            result = dfs(graph, neighbor, goal, visited, path + [node], nodes)
            if result:
                return result
    return None

# Uniform Cost Search (UCS)
def ucs(graph, start, goal):
    pq = [(0, start, [], 0)]  # (cost, node, path, path_cost)
    nodes = 1  # Number of nodes generated
    while pq:
        current_cost, current_node, current_path, total_path_cost = heapq.heappop(pq)
        if current_node == goal:
            print("UCS Search - Number of nodes expanded:", nodes)
            return current_path + [current_node]
        for neighbor, weight in graph[current_node]:
            new_cost = total_path_cost + weight
            new_path = current_path + [current_node]
            heapq.heappush(pq, (new_cost, neighbor, new_path, new_cost))
            nodes += 1
    return None

# Example graph and heuristic values
EXAMPLE_GRAPH = {
    0: [(1, 2), (2, 1)],
    1: [(0, 2), (2, 5), (3, 11), (4, 3)],
    2: [(0, 1), (1, 5), (4, 1), (5, 15)],
    3: [(1, 11), (4, 2), (6, 1)],
    4: [(1, 3), (2, 1), (3, 2), (5, 4), (6, 5)],
    5: [(2, 15), (4, 4), (6, 1)],
    6: [(3, 1), (4, 5), (5, 1)]
}
EXAMPLE_HEURISTIC_VALUES = {
    0: 1,
    1: 3,
    2: 15,
    3: 2,
    4: 1,
    5: float("inf"),
    6: 0
}

# A* Search
print("A* Search")
result = a_star_search(EXAMPLE_GRAPH, 0, 6, EXAMPLE_HEURISTIC_VALUES)
print("Path:", result)

# BFS Search
print("\nBFS Search")
result = bfs(EXAMPLE_GRAPH, 0, 6)
print("Path:", result)

# DFS Search
print("\nDFS Search")
nodes = [1]
result = dfs(EXAMPLE_GRAPH, 0, 6, set(), [], nodes)
print("DFS Search - Number of nodes expanded:", nodes[0])
print("Path:", result)

# UCS Search
print("\nUCS Search")
result = ucs(EXAMPLE_GRAPH, 0, 6)
print("Path:", result)
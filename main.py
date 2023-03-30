import numpy as np

def edmonds_karp(graph, source, sink):
    # Initialize residual graph and flow to 0
    residual_graph = np.zeros((len(graph), len(graph)))
    flow = np.zeros((len(graph), len(graph)))

    # Build residual graph
    for u in graph:
        for v, capacity in graph[u].items():
            residual_graph[u][v] = capacity

    # Keep track of the parent of each node in the BFS
    parent = np.zeros(len(graph), dtype=int)

    max_flow = 0

    # Loop until no path exists from source to sink
    while bfs(residual_graph, source, sink, parent):
        # Find the bottleneck capacity
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual_graph[u][v])
            v = u

        # Update residual graph and flow with bottleneck capacity
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u

        # Add bottleneck capacity to max flow
        max_flow += path_flow

    return max_flow, flow

def bfs(graph, source, sink, parent):
    # Initialize visited array and queue
    visited = np.zeros(len(graph), dtype=bool)
    queue = [source]
    visited[source] = True
    parent[source] = -1

    # BFS loop
    while queue:
        u = queue.pop(0)

        # Check neighbors of u
        for v in range(len(graph)):
            if not visited[v] and graph[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)

                # Stop BFS if sink is found
                if v == sink:
                    return True

    # No path from source to sink
    return False


# Exemple d'utilisation de l'algorithme avec un graphe représentant le réseau routier donnée en exemple dans le sujet
# Chaque clé du dictionnaire représente un sommet du graphe, et chaque valeur est un dictionnaire dont les clés sont les sommets
graph = {
    0: {1: 4, 2: 5, 3: 6},
    1: {2: 2, 5: 6},
    2: {4: 8},
    3: {2: 2, 7: 7},
    4: {1: 5, 3: 4, 5: 3, 7: 5},
    5: {6: 3, 8: 4, 9: 3},
    6: {4: 7, 8: 2},
    7: {6: 4, 8: 5, 9: 2},
    8: {9: 10},
    9: {}
}

# La commune N
N = 9
# Calcul du flot maximal de la commune 0 à la commune N
max_flow, flow = edmonds_karp(graph, 0, N)
print("Maximum flow:", max_flow)
print("Flow matrix:")
print(flow)
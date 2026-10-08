# The Dijkstra Algorithm implemented using an adjacency matrix. 
# Weights and vertex names are all integers.

def dijkstra_adj_mat(start_node, num_vertices, graph):
    if not (0 <= start_node < num_vertices):
        return {}, {}
    dists = [float("inf")] * num_vertices
    dists[start_node] = 0
    visited = [False] * num_vertices
    parent = {node: None for node in range(num_vertices)}
    for _ in range(num_vertices):
        min_dist = float("inf")
        u = -1
        for v in range(num_vertices):
            if not visited[v] and dists[v] < min_dist:
                min_dist = dists[v]
                u = v
        if u == -1:
            break
        visited[u] = True

        for v in range(num_vertices):
            weight = graph[u][v]
            if weight is not None and weight > 0 and not visited[v]:
                if dists[u] + weight < dists[v]:
                    dists[v] = dists[u] + weight
                    parent[v] = u
    ans_dists = {i: dists[i] for i in range(num_vertices)}
    return ans_dists, parent
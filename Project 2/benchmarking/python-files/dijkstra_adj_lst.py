# The Dijkstra Algorithm implemented using an array (list) of adjacency lists (NOT using dictionaries). 
# Weights and vertex names are all integers.

import heapq

def dijkstra_adj_lst(start_node, num_vertices, graph):
    if not (0 <= start_node < num_vertices):
        return {}, {}
    heap = [(0, start_node)]
    ans_dist = {node: float("inf") for node in range(num_vertices)}
    ans_dist[start_node] = 0
    parent = {node: None for node in range(num_vertices)}
    while heap:
        dist, temp = heapq.heappop(heap)
        if dist > ans_dist[temp]: # Pruning
            continue
        for neighbour, weight in graph[temp]:
            if ans_dist[neighbour] > ans_dist[temp] + weight:
                ans_dist[neighbour] = ans_dist[temp] + weight
                parent[neighbour] = temp
                heapq.heappush(heap, (ans_dist[neighbour], neighbour))
    return ans_dist, parent
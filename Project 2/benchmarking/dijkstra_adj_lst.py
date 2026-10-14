# The Dijkstra Algorithm implemented using an array (list) of adjacency lists.
# NOT using dictionaries.
# Weights and vertex names are all integers.

import heapq

def dijkstra_adj_lst(
    start_node: int,
    num_vertices: int,
    graph: list[list[tuple[int, int]]],
) -> tuple[dict[int, float], dict[int, int | None]]:
    """
    Single-source shortest paths using an adjacency list and a min-heap.

    Args:
        start_node: Vertex id the search starts from (0 <= start_node < num_vertices).
        num_vertices: Number of vertices V. Vertices are labelled 0..V-1.
        graph: Adjacency list. graph[u] is a list of (neighbour, weight) tuples,
            one per edge leaving u. len(graph) == num_vertices.

    Returns:
        ans_dist: {vertex: shortest distance from start_node}. float("inf") if unreachable.
        parent: {vertex: previous vertex on its shortest path}. None for start_node
            and for unreachable vertices.
        Both are empty dicts if start_node is out of range.
    """
    if not (0 <= start_node < num_vertices):
        return {}, {}
    # heap: list of (distance, vertex) tuples, ordered by distance (smallest at heap[0]).
    heap: list[tuple[int, int]] = [(0, start_node)]
    ans_dist: dict[int, float] = {node: float("inf") for node in range(num_vertices)}
    ans_dist[start_node] = 0
    parent: dict[int, int | None] = {node: None for node in range(num_vertices)}

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
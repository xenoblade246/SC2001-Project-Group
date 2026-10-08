import csv

def load_csv(file_path: str):
    """Helper function to read the .csv files."""
    edges = []
    max_vertex_id = 0

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            u, v, w = map(int, row)
            edges.append((u, v, w))
            max_vertex_id = max(max_vertex_id, u, v)

    # Vertices are zero-indexed, so vertex count is max_id + 1
    num_vertices = max_vertex_id + 1
    num_edges = len(edges)
    return edges, num_vertices, num_edges

def add_edge_adj_mat(file_path: str):
    """Reads the edge list .csv files and return an adjacency matrix."""
    edges, num_vertices, num_edges = load_csv(file_path)

    # Initialize N x N matrix with NULLs
    graph = [[None] * num_vertices for _ in range(num_vertices)]

    # Populate edges
    for u, v, w in edges:
        if graph[u][v] is None or w < graph[u][v]:
            graph[u][v] = w

    return num_vertices, num_edges, graph

def add_edge_adj_lst(file_path: str):
    """Reads the edge list .csv files and return an adjacency list."""
    edges, num_vertices, num_edges = load_csv(file_path)

    # Create an array (list) of lists for the adjacency list
    graph = [[] for _ in range(num_vertices)]

    # Populate edges: graph[u] stores tuples of (neighbor, weight)
    for u, v, w in edges:
        graph[u].append((v, w))

    return num_vertices, num_edges, graph
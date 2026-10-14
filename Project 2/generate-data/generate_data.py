import math
import os
from pathlib import Path
import random

MAX_WEIGHT = 101
SEED = 42

def generate_csv_dataset(dir_path: str, filename: str, num_vertices: int, num_edges: int, seed: int = SEED, max_weight: int = MAX_WEIGHT) -> None:
    """
    Generates a CSV file containing graph edges in 3 columns: u, v, w (all purely numbers).
    
    Args:
        dir_path: Output directory path.
        filename: Output filename (e.g., "graph_1000_5000.csv").
        num_vertices: Number of vertices (vertices will be labeled 0 to num_vertices - 1).
        num_edges: Number of edges to generate.
        seed: Random seed value.
        max_weight: Maximum weight for edges.
    Returns:
        None (creates the .csv files)
    """

    target_dir = Path(dir_path)
    target_dir.mkdir(parents=True, exist_ok=True)
    full_path = target_dir / filename

    # Check if file already exists
    if full_path.exists():
        print(f"'{dir_path}/{filename}' already exists. Skipping.")
        return

    # Use Python's Built-in Random instance for seeded generation
    rng = random.Random(seed)

    # Fast batch writing using a list buffer to minimize file I/O operations
    batch_size = 65536

    # 1MB buffering on file output matching standard C++ stream buffer behavior
    with open(full_path, "w", encoding="utf-8", buffering=1024 * 1024) as file:

        written = 0
        while written < num_edges:
            current_batch_size = min(num_edges - written, batch_size)
            
            # Generate and format each row as u,v,w in memory
            batch = [
                f"{rng.randint(0, num_vertices - 1)},{rng.randint(0, num_vertices - 1)},{rng.randint(1, max_weight)}"
                for _ in range(current_batch_size)
            ]
            
            # Write out buffered text block efficiently
            file.write("\n".join(batch) + "\n")
            written += current_batch_size

    print(f"Successfully generated {num_edges} edges across {num_vertices} vertices in '{filename}'")



DIRECTED = False

def max_edges(v):
    return v * (v - 1) if DIRECTED else v * (v - 1) // 2

graph_configs = []

# Sparse, E = 5V
for v in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2500, 5000, 10000, 20000]:
    graph_configs.append((v, 5 * v))

# Dense, near-complete
for v in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
    graph_configs.append((v, max_edges(v)))

# Density sweep at fixed V
for v in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000]:
    for d in [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0]:
        e = max(v - 1, int(d * max_edges(v)))
        graph_configs.append((v, e))

# Drop duplicates
graph_configs = sorted(set(graph_configs))

# Write into a .csv file
target_dir = "../data/new_graphs"
for v_size, e_size in graph_configs:
    filename = f"graph_{v_size}_{e_size}.csv"
    print(f"Generating {filename}...")
    generate_csv_dataset(target_dir, filename, v_size, e_size)

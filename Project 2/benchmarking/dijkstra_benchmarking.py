# Benchmark both dijkstra algorithms
import csv
import gc
import time
from pathlib import Path
from dijkstra_adj_mat import dijkstra_adj_mat 
from dijkstra_adj_lst import dijkstra_adj_lst 
import Dataset_Loader

def benchmark_dijkstra_adj_mat(start_node: int, file_path: str, runs: int = 3):
    """Measure algorithm runtime on CPU. Each dataset is measured 3 times before taking the average."""
    num_vertices, num_edges, graph = Dataset_Loader.add_edge_adj_mat(file_path)
    runtimes = []
    for _ in range(runs):
        gc.disable()
        t = time.perf_counter()
        ans_dists, _ = dijkstra_adj_mat(start_node, num_vertices, graph)
        run_time = time.perf_counter() - t
        gc.enable()
        runtimes.append(run_time)
    solve_time = sum(runtimes) / runs
    return {"num_vertices": num_vertices, "num_edges": num_edges, "solve_time": solve_time, "distances": ans_dists}

def benchmark_dijkstra_adj_lst(start_node: int, file_path: str, runs: int = 3):
    """Measure algorithm runtime on CPU. Each dataset is measured 3 times before taking the average."""
    num_vertices, num_edges, graph = Dataset_Loader.add_edge_adj_lst(file_path)
    runtimes = []
    for _ in range(runs):
        gc.disable()
        t = time.perf_counter()
        ans_dists, _ = dijkstra_adj_lst(start_node, num_vertices, graph)
        run_time = time.perf_counter() - t
        gc.enable()
        runtimes.append(run_time)
    solve_time = sum(runtimes) / runs
    return {"num_vertices": num_vertices, "num_edges": num_edges, "solve_time": solve_time, "distances": ans_dists}

def get_first_start_node(file_path: str) -> int:
    """Reads the very first number from the first row of the .csv file to get our starting node."""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                return int(row[0])
    return 0

def gen_benchmark_files(file_path: str):
    """Get benchmarking results for 1 file."""
    path = Path(file_path)
    if not path.exists():
        print(f"File {file_path} not found. Skipping.")
        return
    start_node = get_first_start_node(file_path)
    res_list_mat = benchmark_dijkstra_adj_mat(start_node, file_path)
    res_list_lst = benchmark_dijkstra_adj_lst(start_node, file_path)
    return res_list_mat, res_list_lst

def benchmarking(target_dir: str, output_dir: str):
    """Measure across all .csv graph datasets in a directory."""
    dir_path = Path(target_dir)
    if not dir_path.exists():
        print(f"Directory '{target_dir}' does not exist.")
        return

    csv_files = list(dir_path.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in '{target_dir}'.")
        return
    
    results = []

    print(f"Starting benchmarks across {sum(1 for _ in csv_files)} datasets...")

    for csv_file in csv_files:
        print(f"Processing: {csv_file.name}...")
        res_mat, res_lst = gen_benchmark_files(str(csv_file))
        if res_lst is None:
            continue
        v = res_lst["num_vertices"]
        e = res_lst["num_edges"]
        runtime_adj = res_lst["solve_time"]
        runtime_mat = res_mat["solve_time"]
        results.append({"num_vertices": v,"num_edges": e, "runtime_mat": runtime_mat, "runtime_adj": runtime_adj})

    # Write summary output CSV
    output_path = Path(output_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["num_vertices", "num_edges", "runtime_mat", "runtime_adj"]
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSuccessfully saved benchmark report to '{output_path}'!")

def run_demo(file_path: str): # Demo run to show both algorithms work. |V| = 6 and |E| = 10 
    dir_path = Path(file_path)
    if not dir_path.exists():
        print(f"File '{file_path}' does not exist.")
        return
    start_node = get_first_start_node(file_path)
    
    _, num_vertices, num_edges = Dataset_Loader.load_csv(file_path)
    _, _, graph_adj_mat = Dataset_Loader.add_edge_adj_mat(file_path)
    _, _, graph_adj_lst = Dataset_Loader.add_edge_adj_lst(file_path)
    ans_dists_adj_mat, parents_adj_mat = dijkstra_adj_mat(start_node, num_vertices, graph_adj_mat)
    ans_dists_adj_lst, parents_adj_lst = dijkstra_adj_lst(start_node, num_vertices, graph_adj_lst)

    print(f"Graph Overview: Number of Vertices: {num_vertices}; Number of Edges: {num_edges}")
    print("Dijkstra with Adjacency Matrix:")
    print(f"Minimal distances: {ans_dists_adj_mat}")
    print(f"Parent nodes: {parents_adj_mat}")
    print("Dijkstra with Adjacency List:")
    print(f"Minimal distances: {ans_dists_adj_lst}")
    print(f"Parent nodes: {parents_adj_lst}")

if __name__ == "__main__":
    benchmarking("../data/new_graphs", "../data/results/runtimes.csv")
    run_demo("../data/new_graphs/graph_6_10.csv")
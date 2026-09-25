import math
import os
from pathlib import Path
import random

MAX_VAL = int(1e8) + 5
SEED = 42

def generate_csv_dataset(dir_path: str, filename: str, count: int, seed: int = SEED, max_val: int = MAX_VAL) -> None:
    """
    Generates a CSV file containing random integers.
    
    Args:
        dir_path: Name of the output directory.
        filename: Name of the output CSV file (e.g., "data_10m.csv").
        count: Number of random numbers to generate.
        seed: Random seed value.
        max_val: Maximum random integer value.
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

    # Use python's Built-in Random instance for seeded generation
    rng = random.Random(seed)

    # Fast batch writing using a list buffer to minimize file I/O operations
    batch_size = 65536
    
    # 1MB buffering on file output matching standard C++ stream buffer behavior
    with open(full_path, "w", encoding="utf-8", buffering=1024 * 1024) as file:
        file.write("value\n")
        
        written = 0
        while written < count:
            current_batch_size = min(count - written, batch_size)
            
            # Generate and format a batch of numbers in memory
            batch = [str(rng.randint(1, max_val)) for _ in range(current_batch_size)]
            
            # Write out buffered text block efficiently
            file.write("\n".join(batch) + "\n")
            written += current_batch_size

    print(f"Successfully generated {count} values in '{filename}'")



# Generate random array sizes from 1e3 to 1e7
sizes = []
for i in range(3, 7):
    for j in range(1, 10):
        sizes.append(int(j * (10 ** i)))
sizes.append(10000000)

# Write into a .csv file
target_dir = "data/new_arrays"
for size in sizes:
    filename = f"data_{size}.csv"
    print(f"Generating {filename}...")
    generate_csv_dataset(target_dir, filename, size)
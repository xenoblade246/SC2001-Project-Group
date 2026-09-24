#include <bits/stdc++.h>

using namespace std;

const int MAX_VAL = 1e8 + 5;
const int SEED = 42;

/**
 * Generates a CSV file containing random integers.
 *
 * @param dir_path Name of the output directory.
 * @param filename Name of the output CSV file (e.g., "data_10m.csv").
 * @param count Number of random numbers to generate.
 * @param seed Random seed value.
 * @param max_val Maximum random integer value.
 */

void generate_csv_dataset(const string& dir_path, const string& filename, int64_t count, int seed = SEED, int max_val = MAX_VAL) {
    // Create end file directory.
    filesystem::create_directories(dir_path);
    filesystem::path full_path = filesystem::path(dir_path) / filename;

    // Check if file already exists.
    if (filesystem::exists(full_path)) {
        cout << "'" << dir_path << "/" << filename << "' already exists. Skipping.\n";
        return;
    }

    ofstream file(full_path, ios::out | ios::binary);
    if (!file.is_open()) {
        cerr << "Error opening file: " << full_path.string() << endl;
        return;
    }

    // Allocate a large 1MB internal stream buffer for fast disk I/O.
    constexpr int64_t STREAM_BUF_SIZE = 1024 * 1024;
    vector<char> stream_buffer(STREAM_BUF_SIZE);
    file.rdbuf()->pubsetbuf(stream_buffer.data(), STREAM_BUF_SIZE);

    // High-performance Mersenne Twister random generator using passed seed.
    mt19937 gen(seed);
    uniform_int_distribution<int> distrib(1, max_val);

    file << "value\n";

    // Fast batch text conversion to speed up file writes for large datasets.
    constexpr int64_t BATCH_SIZE = 65536;
    vector<char> text_buffer(BATCH_SIZE * 12);

    int64_t written = 0;
    while (written < count) {
        int64_t current_batch = min(count - written, BATCH_SIZE);
        char* ptr = text_buffer.data();

        for (int64_t i = 0; i < current_batch; i++) {
            int num = distrib(gen);
            auto [next_ptr, ec] = to_chars(ptr, ptr + 11, num);
            ptr = next_ptr;
            *ptr++ = '\n';
        }

        file.write(text_buffer.data(), ptr - text_buffer.data());
        written += current_batch;
    }

    file.close();
    cout << "Successfully generated " << count << " values in '" << filename << "'\n";
}

int main() {
    // Generate random array sizes from 1e3 to 1e8
    vector<int64_t> sizes;
    for (int i = 3; i <= 6; i++){
        for (int j = 1; j <= 9; j++){
            sizes.push_back(static_cast<int64_t>(j * pow(10, i)));
        }
    }
    sizes.push_back(10000000);

    // Write into a .csv file
    string target_dir = "data/new_arrays";
    for (int64_t size : sizes) {
        string filename = "data_" + to_string(size) + ".csv";
        cout << "Generating " << filename << "..." << endl;
        generate_csv_dataset(target_dir, filename, size);
    }
    return 0;
}
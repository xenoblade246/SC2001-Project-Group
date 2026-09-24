#include <bits/stdc++.h>
#include "Dataset_Loader.h"

using namespace std;

/**
 * Reads a single-column CSV dataset into a vector<int>.
 * 
 * @param filename Name of the file
 * @return vector<int> containing the parsed integers
 */

vector<int> load_csv_dataset(const string& filename) {
    filesystem::path file_path = filesystem::path("data/new_arrays") / filename;

    ifstream file(file_path);

    // 1MB buffer for fast file reading
    constexpr int64_t STREAM_BUF_SIZE = 1024 * 1024;
    vector<char> stream_buffer(STREAM_BUF_SIZE);
    file.rdbuf()->pubsetbuf(stream_buffer.data(), STREAM_BUF_SIZE);

    if (!file.is_open()) {
        cerr << "Error opening file: " << file_path.string() << endl;
        return {};
    }

    string line;
    // Skip the "value" header line
    getline(file, line);

    vector<int> data;
    // Reserve memory if possible to avoid multiple reallocations
    data.reserve(100000); 

    while (getline(file, line)) {
        if (!line.empty()) {
            data.push_back(stoi(line));
        }
    }

    file.close();
    return data;
}
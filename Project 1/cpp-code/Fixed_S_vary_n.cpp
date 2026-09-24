#include <bits/stdc++.h>
#include "Dataset_Loader.h"
#include "Sorting_Algorithms.h"

using namespace std;

// Experiment (c)(i): fixed threshold S, varying input size n.
const int S = 32;

int main() {
    // Results are written to a CSV file for easy plotting in the report.
    filesystem::create_directories("data/results");
    ofstream results("data/results/fixed_S_vary_n.csv");
    if (!results.is_open()) {
        cerr << "Error creating results file: data/results/fixed_S_vary_n.csv" << endl;
        return 1;
    }

    cout << "Fixed S = " << S << ", varying n\n";
    cout << setw(12) << "n"
         << setw(20) << "Key Comparisons"
         << setw(15) << "Time (ms)"
         << setw(10) << "Sorted" << "\n";

    results << "n,S,key_comparisons,time_ms,is_sorted\n";
    cout << fixed << setprecision(3);

    vector<int64_t> sizes;
    for (int i = 3; i <= 6; i++){
        for (int j = 1; j <= 9; j++){
            sizes.push_back(static_cast<int64_t>(j * pow(10, i)));
        }
    }
    sizes.push_back(10000000);

    // Dataset sizes match Generate_Data.cpp: 1e3, 2e3, ..., 1e7.
    for (auto n: sizes) {
        string filename = "data_" + to_string(n) + ".csv";

        // load_csv_dataset reads from data/new_arrays/<filename>.
        vector<int> data = load_csv_dataset(filename);
        if (data.empty()) {
            cerr << "Skipping '" << filename << "' (missing or empty dataset).\n";
            continue;
        }

        auto start_time = chrono::high_resolution_clock::now();
        int64_t kcomp = hybrid_sort(data, S);
        auto end_time = chrono::high_resolution_clock::now();

        double time_ms = chrono::duration<double, milli>(end_time - start_time).count();
        bool sorted_ok = is_sorted(data.begin(), data.end());

        cout << setw(12) << n
                << setw(20) << kcomp
                << setw(15) << time_ms
                << setw(10) << (sorted_ok ? "Yes" : "NO!") << "\n";

        results << n << "," << S << "," << kcomp << ","
                << time_ms << "," << (sorted_ok ? 1 : 0) << "\n";
    }

    results.close();
    cout << "\nResults written to data/results/fixed_S_vary_n.csv\n";
    return 0;
}
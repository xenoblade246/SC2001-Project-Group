#include <bits/stdc++.h>
#include "Dataset_Loader.h"
#include "Sorting_Algorithms.h"

using namespace std;

// Experiment (c)(ii): fixed input size n, varying threshold S.
// This will also be used to find the optimal S in (c) (iii)
const vector<int> sizes = {1000, 10000, 100000, 1000000, 10000000};

int main() {
    // Results are written to a CSV for easy plotting in the report.
    filesystem::create_directories("data/results");

    for (auto n: sizes){
        string end_path = "data/results/fixed_n_vary_S_" + to_string(n) + ".csv";
        ofstream results(end_path);
        if (!results.is_open()) {
            cerr << "Error creating results file: " << end_path << endl;
            return 1;
        }

        cout << "Fixed n = " << n << ", varying S\n";
        cout << setw(12) << "S"
            << setw(20) << "Key Comparisons"
            << setw(15) << "Time (ms)"
            << setw(20) << "Ratio with S = 1"
            << setw(10) << "Sorted" << "\n";

        results << "n,S,key_comparisons,time_ms,ratio_with_S=1,is_sorted\n";
        cout << fixed << setprecision(3);

        // The load_csv_dataset(filename) function reads from data/new_arrays/<filename>.
        string filename = "data_" + to_string(n) + ".csv";
        vector<int> master_data = load_csv_dataset(filename);
        for (int S = 1; S <= 80; S++) {
            vector<int> data = master_data;
            if (data.empty()) {
                cerr << "Skipping '" << filename << "' (missing or empty dataset).\n";
                continue;
            }
            double base_time;
            auto start_time = chrono::high_resolution_clock::now();
            int64_t kcomp = hybrid_sort(data, S);
            auto end_time = chrono::high_resolution_clock::now();

            double time_ms = chrono::duration<double, milli>(end_time - start_time).count();
            if (S == 1){
                base_time = time_ms;
            }
            bool sorted_ok = is_sorted(data.begin(), data.end());

            cout << setw(12) << S
                    << setw(20) << kcomp
                    << setw(15) << time_ms
                    << setw(20) << time_ms / base_time
                    << setw(10) << (sorted_ok ? "Yes" : "NO!") << "\n";

            results << n << "," << S << "," << kcomp << ","
                    << time_ms << "," << time_ms/base_time << "," << (sorted_ok ? 1 : 0) << "\n";
        }
        results.close();
        cout << "\nResults written to " << end_path << "\n";
    }
    return 0;
}
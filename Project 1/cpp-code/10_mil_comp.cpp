#include <bits/stdc++.h>
#include "Dataset_Loader.h"
#include "Sorting_Algorithms.h"

using namespace std;

const int S = 32;
// For now, if we cannot find an optimal S in (c) we can use S as above.
// S optimal for n = 1e7 is 33, so S = 32 is acceptable. 

int main(){
    int n = 10000000;

    filesystem::create_directories("data/results");
    ofstream results("data/results/10_mil_comp.csv");
    if (!results.is_open()) {
        cerr << "Error creating results file: data/results/10_mil_comp.csv" << endl;
        return 1;
    }

    cout << "Comparison on fixed n = " << n << " with S = " << S << "\n\n";
    cout << setw(15) << "Algorithm"
         << setw(20) << "Key Comparisons"
         << setw(15) << "Time (ms)"
         << setw(10) << "Sorted" << "\n";

    // Header includes Algorithm name to differentiate rows in CSV
    results << "algorithm,n,S,key_comparisons,time_ms,is_sorted\n";

    string filename = "data_10000000.csv";

    // 1. Benchmark Hybrid Sort
    vector<int> data_hybrid = load_csv_dataset(filename);;
    if (!data_hybrid.empty()) {
        auto start = chrono::high_resolution_clock::now();
        int64_t kcomp_hybrid = hybrid_sort(data_hybrid, S);
        auto end = chrono::high_resolution_clock::now();

        double time_ms_hybrid = chrono::duration<double, milli>(end - start).count();
        bool sorted_ok_hybrid = is_sorted(data_hybrid.begin(), data_hybrid.end());

        cout << setw(15) << "Hybrid Sort"
             << setw(20) << kcomp_hybrid
             << setw(15) << time_ms_hybrid
             << setw(10) << (sorted_ok_hybrid ? "Yes" : "NO!") << "\n";

        results << "Hybrid," << n << "," << S << "," << kcomp_hybrid << ","
                << time_ms_hybrid << "," << (sorted_ok_hybrid ? 1 : 0) << "\n";
    }

    // 2. Benchmark Merge Sort
    vector<int> data_merge = load_csv_dataset(filename);
    if (!data_merge.empty()) {
        auto start = chrono::high_resolution_clock::now();
        int64_t kcomp_merge = merge_sort(data_merge);
        auto end = chrono::high_resolution_clock::now();

        double time_ms_merge = chrono::duration<double, milli>(end - start).count();
        bool sorted_ok_merge = is_sorted(data_merge.begin(), data_merge.end());

        cout << setw(15) << "Merge Sort"
             << setw(20) << kcomp_merge
             << setw(15) << time_ms_merge
             << setw(10) << (sorted_ok_merge ? "Yes" : "NO!") << "\n";

        results << "Merge," << n << "," << S << "," << kcomp_merge << ","
                << time_ms_merge << "," << (sorted_ok_merge ? 1 : 0) << "\n";
    }

    results.close();
    cout << "\nResults saved to data/results/10_mil_comp.csv\n";
    return 0;
}

#ifndef SORTING_ALGORITHMS_H
#define SORTING_ALGORITHMS_H

#include <bits/stdc++.h>

// Function declaration
std::int64_t hybrid_sort(std::vector<int>& numArray, int S, int start = 0, int end = -1);
std::int64_t merge_sort(std::vector<int>& numArray, int start = 0, int end = -1);
std::int64_t merge(std::vector<int>& arr, int l, int m, int r);
std::int64_t insertion_sort(std::vector<int>& arr, int l = 0, int r = -1);

#endif
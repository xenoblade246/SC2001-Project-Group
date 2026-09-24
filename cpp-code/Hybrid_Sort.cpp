#include <bits/stdc++.h>
#include "Sorting_Algorithms.h"

using namespace std;

/**
 * In-place hybrid sort that arranges array elements in ascending order.
 *
 * @param numArray Target array to be sorted.
 * @param S The maximum subarray value before recursing.
 * @param start The left bound of values for function to focus on.
 * @param end The right bound of values for function to focus on (-1 defaults to last index).
 * @return The number of key comparisons made in the hybrid sort process.
 */

int64_t hybrid_sort(vector<int>& numArray, int S, int start, int end) {
    // Initialises the start & end values, if they do not exist.
    if (end == -1) {
        if (numArray.empty()) return 0;
        end = numArray.size() - 1;
    }

    // Prematurely ends function if left bound exceeds right.
    if (end <= start) {
        return 0;
    }

    // Runs an insertion sort algorithm for arrays smaller or equal to S.
    if (end - start + 1 <= S){
        return insertion_sort(numArray, start, end);
    }

    // Splits the array into 2 sections and implement merge sort on each section.
    int mid = start + (end - start) / 2;
    int64_t kcomp_l = hybrid_sort(numArray, S, start, mid);
    int64_t kcomp_r = hybrid_sort(numArray, S, mid + 1, end);

    // Sorts every element in the array concurrently in both sections.
    int64_t kcomp_m = merge(numArray, start, mid, end);

    return kcomp_l + kcomp_r + kcomp_m;
}
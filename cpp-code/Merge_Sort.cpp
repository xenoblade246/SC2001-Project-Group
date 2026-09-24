#include <bits/stdc++.h>
#include "Sorting_Algorithms.h"

using namespace std;

// Helper function declaration
int64_t merge(vector<int>& arr, int l, int m, int r);

/**
 * In-place merge sort that arranges array elements in ascending order.
 *
 * @param numArray Target array to be sorted.
 * @param start The left bound of values for function to focus on.
 * @param end The right bound of values for function to focus on (-1 defaults to last index).
 * @return The number of key comparisons made in the merge sort process.
 */

int64_t merge_sort(vector<int>& numArray, int start, int end) {
    // Initialises the start & end values, if they do not exist.
    if (end == -1) {
        if (numArray.empty()) return 0;
        end = numArray.size() - 1;
    }

    // Prematurely ends function if left bound exceeds right.
    if (end <= start) {
        return 0;
    }

    // Splits the array into 2 sections and implement merge sort on each section.
    int mid = start + (end - start) / 2;
    int64_t kcomp_l = merge_sort(numArray, start, mid);
    int64_t kcomp_r = merge_sort(numArray, mid + 1, end);

    // Sorts every element in the array concurrently in both sections.
    int64_t kcomp_m = merge(numArray, start, mid, end);

    return kcomp_l + kcomp_r + kcomp_m;
}

/**
 * Helper function for merge sorting.
 *
 * @param arr Target array to be sorted.
 * @param l The left bound of values for function to focus on.
 * @param m The middle value to split the target array.
 * @param r The right bound of values for function to focus on.
 * @return The number of key comparisons made in the merging process.
 */

int64_t merge(vector<int>& arr, int l, int m, int r) {
    // Initialises a sub-array with the left and right bounds, as well as pointers and 
    // kcomp to track key comparisons.
    vector<int> temp(arr.begin() + l, arr.begin() + r + 1);

    int i = 0;
    int left_end = m - l;
    int j = m + 1 - l;
    int right_end = r - l;

    int k = l;
    int64_t kcomp = 0;

    // Iterates through the temp array, adding elements in ascending order to final array.
    // Overwrites array values in the original array with the next smallest element per loop.
    while (i <= left_end && j <= right_end) {
        kcomp++;
        if (temp[i] <= temp[j]) {
            arr[k] = temp[i];
            i++;
        } else {
            arr[k] = temp[j];
            j++;
        }
        k++;
    }

    // Adds all remaining elements (if any) to the final array.
    while (i <= left_end) {
        arr[k] = temp[i];
        i++;
        k++;
    }
    while (j <= right_end) {
        arr[k] = temp[j];
        j++;
        k++;
    }

    return kcomp;
}
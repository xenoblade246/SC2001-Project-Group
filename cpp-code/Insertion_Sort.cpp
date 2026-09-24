#include <bits/stdc++.h>
#include "Sorting_Algorithms.h"

using namespace std;

/** 
 * Insertion sort to arrange array elements in ascending order.
 * 
 * @param arr Number array to be sorted.
 * @param l Left bound of unsorted elements.
 * @param r Right bound of unsorted elements (-1 defaults to last index).
 * @return Number of key comparisons made.
*/

int64_t insertion_sort(vector<int>& arr, int l, int r){
    int64_t kcomp = 0;

    // Initialises end value if they do not exist and kcomp to track key comparisons.
    if (r == -1) {
        r = arr.size() - 1;
    }

    // Insertion sort main function using shifting (overwriting) instead of swapping.
    for (int i = l + 1; i <= r; i++) {
        int j = i - 1;
        int tmp = arr[i];

        while (j >= l) {
            kcomp++;
            if (arr[j] > tmp) {
                arr[j + 1] = arr[j];
                j--;
            } else {
                break;
            }
        }
        arr[j + 1] = tmp;
    }

    return kcomp;
}
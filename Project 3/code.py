# Part 1:
"""
Recursion definition of P(C):
- Let P(C) be the maximum profit achievable from a set of object types X_1, X_2, ..., X_n under a weight limit C. Since 
the choice depends on how many types are still available, P(C) is more accurately written as P(n, C), where n is the 
number of object types considered.

- Define P(i, C) as the maximal profit achievable using the first i types of objects with weight limit C. 

- Since each type can be chosen indefinitely, taking a copy of type i consumes weight[i - 1] (1-based indexing) capacity 
but does not remove type i from the candidate set — hence the index stays at i in the include branch.

- Formula:
    if weight[i - 1] > C, type i cannot fit, so it is excluded: 
        P(i, C) = P(i - 1, C)

    otherwise:
        include = P(i, C - weight[i - 1]) + profit[i - 1] (1 copy of object type i taken, type i still available) 
        exclude = P(i - 1, C) (0 copies of object type i taken, move to the remaining i - 1 types)
        P(i, C) = max(include, exclude)

    Note that i is 1-based, so values taken from the weights and profits arrays require offsetting by 1.

- The base case is when the object set is empty (P(0, C) = 0) or the maximum capacity is 0 (P(i, 0) = 0).

- Time complexity: O(2^(n + C / min(weights))) since each call branches at most twice and the recursion depth is bounded 
by n + C / min(weights).

Below is the Python implementation:
"""
def knapsack_0_n_rec(n: int, C: int, weights: list[int], profits: list[int]) -> int:
    # Base case: No objects to choose from/no more capacity
    if n == 0 or C == 0:
         return 0
    
    # If object weight surpasses capacity, skip entirely
    if weights[n - 1] > C:
        return knapsack_0_n_rec(n - 1, C, weights, profits)

    # Binary choice: Include/Exclude
    include = profits[n - 1] + knapsack_0_n_rec(n, C - weights[n - 1], weights, profits)
    exclude = knapsack_0_n_rec(n - 1, C, weights, profits)
    return max(include, exclude)

print(f"Test correctness on 2: {knapsack_0_n_rec(3, 15, [4, 5, 8], [7, 6, 9])}")

# Part 2: Draw on paper

# Part 3: Pseudocode or just take part 4's code or write this in CPP
"""
def knapsack_0_n_dp(int n, int C, int weights, int profits):
    init dp = []
    for (int i from 0 to n + 1) {
        init row = []
        for (int j from 0 to C + 1) {
            add 0 into row
        }
        add row into dp
    }

    for (int i from 1 to n + 1){
        for (int j from 1 to C + 1){
            skip = dp[i - 1][j]
            take = dp[i][j - weights[i - 1]] + profits[i - 1]
            if (weights[i - 1] <= j){
                dp[i][j] = max(skip, take)
            }
            else{
                dp[i][j] = skip
            }
        }
    }

    return dp[n][C]   
"""

# Part 4:
def knapsack_0_n_dp(n: int, C: int, weights: list[int], profits: list[int]) -> int:
    dp = [[0 for _ in range(C + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, C + 1):
            if weights[i - 1] <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - weights[i - 1]] + profits[i - 1])
            else:
                dp[i][j] = dp[i - 1][j]
    return dp[n][C]

print(f"Answer to (4a): {knapsack_0_n_dp(3, 16, [5, 6, 7], [7, 6, 9])}")
print(f"Answer to (4b): {knapsack_0_n_dp(3, 12, [5, 6, 7], [7, 6, 9])}")

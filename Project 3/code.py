# Part 1:
"""
- Let us store the weights and profits of the objects in 2 seperate arrays named “weights” and “profits” respectively.
- Since each type can be chosen indefinitely, taking a copy of type i will get profits[i] and consume weights[i], 
but will not remove type i from the candidate set.
- Thus, the recursive definiton for the algorithm is:
P(C) = max(P(C - weights[i]) + profits[i], P(C)) for all objects i.
P(x) = 0 for x < min(weights)
"""

# Part 2: Draw on paper

# Part 3: Pseudocode or just take part 4's code or write this in CPP
"""
- We initialise a 1D array called “dp” with dp[x] storing the maximum profit obtainable with weight x. 
Thus, the value of P(C) will be dp[C].
- Set dp[x] = 0 for all x < min(weights).
- For every object type i that weighs less than or equal to C, go through dp using a varible w from 
weights[i] to C, since all weights lower than weights[i] cannot take weights[i]. Then, update dp[w] 
with the larger value between dp[w - weights[i]] + profits[i] and dp[w].
"""

# Part 4:
def P(C: int) -> int:
    global n, weights, profits
    dp = [0 for _ in range(C + 1)]
    for i in range(n):
        if weights[i] <= C:
            for w in range(weights[i], C + 1):
                dp[w] = max(dp[w - weights[i]] + profits[i], dp[w])
    return dp[C]

n = 3

weights = [4, 5, 8]
profits = [7, 6, 9]
print(P(12))

weights = [4, 5, 8]
profits = [7, 6, 9]
print(P(16))

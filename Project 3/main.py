# Question 3
def P(C: int) -> int:
    """
    Recursive function that finds maximum profit by packing objects into
    knapsack of capacity C.
    """
    # Number of object types, weights & profits respectively
    global n, w, p
    max_profit = 0

    for i in range(n):
        if w[i] <= C:
            max_profit = max(max_profit, P(C - w[i]) + p[i])
    
    return max_profit

# Question 4(a)
n = 3
w = [4, 5, 6]
p = [7, 8, 9]
ans = P(16)

print("Max profit:", ans)

# Question 4(b)
n = 3
w = [5, 6, 7]
p = [7, 6, 9]
ans = P(12)

print("Max profit:", ans)
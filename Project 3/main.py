# Imports

# Classes
class Knapsack:
    def __init__(self, C, n):
        self.C: int = C
        self.n: int = n

class Object:
    def __init__(self, w, p):
        self.w: int = w
        self.p: int = p

# Functions
def P(C):
    """
    Recursive function that finds maximum profit by packing objects into
    knapsack of capacity C.
    """
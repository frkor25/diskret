def C(n, r):
    """Returns how many combinations of n choose r."""
    return (factorial(n)//
            (factorial(r)*factorial(n-r))
            )

def P(n, r):
    """Returns how many permutations with n and r as input."""
    return (factorial(n)//
            factorial(n-r)
            )

def C_rep(n, r):
    """Returns how many combinations with repetition of n choose r.
    Formula: C(n+r-1, r) = (n+r-1)! / (r! * (n-1)!)
    """
    return (factorial(n + r - 1)//
            (factorial(r) * factorial(n - 1))
            )

def P_rep(n, r):
    """Returns how many permutations with repetition of n and r.
    Formula: n^r
    """
    return n ** r

# Auxilary Functions

def factorial(n: int) -> int:
    """Returns the factorial of n."""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

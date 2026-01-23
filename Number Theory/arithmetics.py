# from arithmetics import *


def gcd(m: int, n: int) -> int:
    """Returns greatest common divisor of m and n
    using Euclides' algorithm.
    """
    if n == 0:
        return m
    else:
        return gcd(n,m % n)

def lcm(m: int, n: int) -> int:
    """Returns the least common multiple of m and n."""
    return int(m*(n/gcd(m,n)))

def modular_inverse(x: int, m: int) -> int:
    """Returns modular multiplicative inverse for x
    using naive approach.
    """
    a = 0
    for a in range(1,m):
        if ((x % m)*(a % m)) % m != 1:
            a += 1
        else:
            return a
    print(f"No modular inverse for {x}")

def modular_inverse2(x: int, m: int) -> int | None:
    """Returns modular inverse of x modulo m using Extended Euclidean Algorithm."""
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        else:
            gcd, x1, y1 = extended_gcd(b, a % b)
            x = y1
            y = x1 - (a // b) * y1
            return gcd, x, y

    gcd_val, inv, _ = extended_gcd(x, m)
    if gcd_val != 1:
        return None  # No inverse exists
    else:
        return inv % m

def is_relative_prime(a, b) -> bool:
    """Checks if a and b are realtive primes."""
    return gcd(a,b) == 1

def are_pairwise_prime(numbers: list[int]) -> bool:
    """Checks if the integers in a list are
    pairwise prime.
    """
    if len(numbers) == 2:
        return gcd(numbers[0],numbers[1]) == 1
    else:
        for number in numbers:
            new_numbers = numbers[:]
            new_numbers.remove(number)
            if not are_pairwise_prime(new_numbers):
                return False
    return True

def is_prime(n: int) -> bool:
    """Checks if n is a prime number."""
    if n == 2:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    for k in range(3,int(n**0.5)+1, 2):
        if n % k == 0:
            return False
    return True

def is_congruent(a: int, b: int, n: int) -> bool:
    """Returns True if a ≡ b (mod n)."""
    return (a - b) % n == 0 


def divides(a: int, b: int) -> bool:
    """Checks if a divides b (a | b)."""
    if a == 0:
        return b == 0
    return b % a == 0

def find_divisors(n: int) -> list[int]:
    """Returns all positive divisors of n."""
    if n == 0:
        return []
    divisors = []
    for i in range(1, abs(n) + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors

def find_common_divisors(a: int, b: int) -> list[int]:
    """Returns all common divisors of a and b."""
    divisors_a = set(find_divisors(abs(a)))
    divisors_b = set(find_divisors(abs(b)))
    return sorted(list(divisors_a & divisors_b))

def find_multiples(n: int, limit: int) -> list[int]:
    """Returns all positive multiples of n up to limit."""
    if n == 0:
        return []
    return [i * n for i in range(1, limit // abs(n) + 1)]

def find_common_multiples(a: int, b: int, limit: int) -> list[int]:
    """Returns all common multiples of a and b up to limit."""
    multiples_a = set(find_multiples(abs(a), limit))
    multiples_b = set(find_multiples(abs(b), limit))
    return sorted(list(multiples_a & multiples_b))

def bézout_coefficients(a: int, b: int) -> tuple[int, int, int]:
    """Returns (gcd, x, y) where gcd = a*x + b*y (Bézout's identity)."""
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        else:
            gcd_val, x1, y1 = extended_gcd(b, a % b)
            x = y1
            y = x1 - (a // b) * y1
            return gcd_val, x, y
    
    return extended_gcd(abs(a), abs(b))

def prime_factors(n: int) -> list[int]:
    """Returns the prime factorization of n as a list."""
    if n <= 1:
        return []
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def euler_totient(n: int) -> int:
    """Returns φ(n) - count of integers ≤ n that are coprime with n."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def solve_congruence_system(congruences: list[tuple[int, int]], limit: int = 25000) -> list[int]:
    """
    Solves a system of linear congruences using brute force.
    
    Args:
        congruences: List of (remainder, modulus) tuples
                    Example: [(2, 4), (3, 7)] means x≡2(mod4) and x≡3(mod7)
        limit: Search up to this limit
    
    Returns:
        List of solutions in range [0, limit]
    """
    if not congruences:
        return []
    
    # Calculate LCM of all moduli to find the period
    moduli = [mod for _, mod in congruences]
    period = moduli[0]
    for mod in moduli[1:]:
        period = (period * mod) // gcd(period, mod)
    
    solutions = []
    
    # Search for solutions
    for x in range(limit + 1):
        if all(is_congruent(x, a, n) for a, n in congruences):
            solutions.append(x)
            # If we found one solution and period is reasonable, we can stop early
            if len(solutions) > 0 and period <= limit:
                break  # Found the first solution
    
    return solutions

def count_solutions_unknown_remainders(moduli: list[int], max_x: int) -> int:
    """
    Counts number of solutions in {0,...,max_x} for a system
    x ≡ a_i (mod m_i) with unknown remainders a_i,
    assuming moduli are pairwise coprime.
    """
    # Period given by CRT
    period = 1
    for m in moduli:
        period *= m

    return max_x // period + 1


def check_congruence_solvability(congruences: list[tuple[int, int]]) -> bool:
    """
    Checks if a system of congruences has a solution.
    Uses pairwise compatibility check.
    """
    for i, (a1, n1) in enumerate(congruences):
        for a2, n2 in congruences[i+1:]:
            d = gcd(n1, n2)
            if (a1 - a2) % d != 0:
                return False
    return True
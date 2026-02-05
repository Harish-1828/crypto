import random


def power(a, n, p):
    """Iterative function to calculate (a^n) % p in O(log n)"""
    res = 1
    a = a % p
    
    while n > 0:
        # If n is odd, multiply 'a' with result
        if n & 1:
            res = (res * a) % p
        
        # n must be even now
        n = n >> 1  # n = n / 2
        a = (a * a) % p
    
    return res


def is_prime(n, k):
    """
    Fermat's Primality Test
    If n is prime, then always returns true
    If n is composite, returns false with high probability
    Higher value of k increases probability of correct result
    
    Returns: (result, steps)
    """
    steps = []
    steps.append(f"Testing n = {n} with k = {k} iterations")
    steps.append("")
    
    # Corner cases
    if n <= 1 or n == 4:
        steps.append("n ≤ 1 or n = 4 → Composite")
        return "Composite", steps
    
    if n <= 3:
        steps.append(f"n = {n} ≤ 3 → Prime")
        return "Prime", steps
    
    steps.append("Using Fermat's Little Theorem:")
    steps.append("If n is prime and gcd(a,n) = 1, then a^(n-1) ≡ 1 (mod n)")
    steps.append("")
    
    # Try k times
    for i in range(k):
        # Pick a random number in [2, n-2]
        a = 2 + random.randint(0, n - 5)
        
        steps.append(f"Iteration {i+1}:")
        result = power(a, n - 1, n)
        steps.append(f"{a}^({n}-1) mod {n} = {result}")
        
        # Fermat's little theorem
        if result != 1:
            steps.append(f"Result ≠ 1 → {n} is COMPOSITE")
            return "Composite", steps
        else:
            steps.append(f"Result = 1 ✓")
        
        steps.append("")
    
    steps.append(f"All {k} tests passed → {n} is PROBABLY PRIME")
    return "Probably Prime", steps

def is_prime(n, k=None):
    """
    Fermat's Primality Test using a^p - a method.
    If (a^p - a) is divisible by p for all a from 1 to p-1, then p is prime.
    
    Returns: (result, steps)
    """
    steps = []

    # Corner cases
    if n <= 1:
        steps.append(f"{n} is not prime (n ≤ 1)")
        return "Composite", steps

    if n <= 3:
        steps.append(f"∴ {n} is prime")
        return "Prime", steps

    steps.append("Solution:")
    steps.append("")
    steps.append(f"a^p - a → 'p' is prime if this is a multiple of 'p'")
    steps.append("")

    is_prime_flag = True
    for a in range(1, n):
        power = a ** n
        result = power - a
        steps.append(f"{a}^{n} - {a}    = {power} - {a}    = {result}")

        if result % n != 0:
            is_prime_flag = False
            steps.append(f"{result} is NOT a multiple of {n}")
            steps.append("")
            steps.append(f"∴ {n} is composite")
            return "Composite", steps

    steps.append("")
    steps.append(f"∴ {n} is prime")
    return "Prime", steps

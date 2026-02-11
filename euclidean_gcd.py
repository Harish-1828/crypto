def euclidean_gcd(a, b):
    """
    Calculate the Greatest Common Divisor (GCD) using Euclidean algorithm.
    Returns the GCD and the steps taken.
    """
    steps = []
    original_a, original_b = a, b

    # Ensure a >= b
    if a < b:
        a, b = b, a

    steps.append(f"Here a={a}, b={b}")
    steps.append("")
    steps.append(f"GCD (a, b) = GCD (b, a mod b)")
    steps.append("")

    while b != 0:
        remainder = a % b
        steps.append(f"GCD ({a}, {b})    = GCD ({b}, {a} mod {b})    = GCD({b}, {remainder})")
        a, b = b, remainder

    # last line shows = gcd
    steps[-1] = steps[-1] + f"    = {a}"
    steps.append("")
    steps.append(f"GCD = {a}")

    return a, steps


def extended_euclidean_gcd(a, b):
    """
    Extended Euclidean algorithm.
    Returns gcd, x, y such that ax + by = gcd(a, b)
    """
    steps = []
    original_a, original_b = a, b
    
    steps.append(f"Finding GCD of {original_a} and {original_b} using Extended Euclidean Algorithm")
    
    if b == 0:
        steps.append(f"GCD = {a}, x = 1, y = 0")
        return a, 1, 0, steps
    
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    
    while b != 0:
        quotient = a // b
        remainder = a % b
        steps.append(f"{a} = {b} × {quotient} + {remainder}")
        
        a, b = b, remainder
        x0, x1 = x1, x0 - quotient * x1
        y0, y1 = y1, y0 - quotient * y1
    
    gcd = a
    x = x0
    y = y0
    
    steps.append(f"GCD = {gcd}")
    steps.append(f"{original_a} × {x} + {original_b} × {y} = {gcd}")
    
    return gcd, x, y, steps

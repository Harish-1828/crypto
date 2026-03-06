def power(a, b, p):
    """Power function to return value of a^b mod P"""
    return pow(a, b, p)


def is_prime(n):
    """Simple primality check."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def find_primitive_roots(p):
    """Find primitive roots of p for validation."""
    if not is_prime(p):
        return []
    
    phi = p - 1
    primitive_roots = []
    
    for g in range(2, p):
        # Check if g is a primitive root
        is_primitive = True
        seen = set()
        for i in range(1, phi + 1):
            val = pow(g, i, p)
            if val in seen:
                is_primitive = False
                break
            seen.add(val)
            if val == 1 and i != phi:
                is_primitive = False
                break
        
        if is_primitive and len(seen) == phi:
            primitive_roots.append(g)
    
    return primitive_roots


def diffie_hellman_exchange(P, G, a, b):
    """
    Perform Diffie-Hellman key exchange.
    Returns (result_dict, steps)
    """
    steps = []
    
    # Validate inputs
    steps.append("=" * 50)
    steps.append("DIFFIE-HELLMAN KEY EXCHANGE")
    steps.append("=" * 50)
    steps.append("")
    
    # Step 1: Public Parameters
    steps.append("STEP 1: Public Parameters (Known to Everyone)")
    steps.append("-" * 50)
    steps.append(f"Prime number P = {P}")
    
    if not is_prime(P):
        steps.append(f"⚠ WARNING: {P} is NOT a prime number!")
        steps.append("For security, P should be a large prime.")
        steps.append("")
    else:
        steps.append(f"✓ {P} is prime")
        steps.append("")
    
    steps.append(f"Primitive root G = {G}")
    
    # For small primes, verify G is a primitive root
    if P < 100 and is_prime(P):
        roots = find_primitive_roots(P)
        if G in roots:
            steps.append(f"✓ {G} is a primitive root of {P}")
        else:
            steps.append(f"⚠ WARNING: {G} may not be a primitive root of {P}")
            if roots:
                steps.append(f"Valid primitive roots: {roots[:10]}")  # Show first 10
    steps.append("")
    
    # Step 2: Alice's Private Key and Public Key
    steps.append("STEP 2: Alice's Private and Public Keys")
    steps.append("-" * 50)
    steps.append(f"Alice chooses private key: a = {a}")
    steps.append(f"Alice calculates public key: A = G^a mod P")
    steps.append(f"A = {G}^{a} mod {P}")
    
    A = power(G, a, P)
    steps.append(f"A = {A}")
    steps.append("")
    steps.append(f"✓ Alice sends A = {A} to Bob (publicly)")
    steps.append("")
    
    # Step 3: Bob's Private Key and Public Key
    steps.append("STEP 3: Bob's Private and Public Keys")
    steps.append("-" * 50)
    steps.append(f"Bob chooses private key: b = {b}")
    steps.append(f"Bob calculates public key: B = G^b mod P")
    steps.append(f"B = {G}^{b} mod {P}")
    
    B = power(G, b, P)
    steps.append(f"B = {B}")
    steps.append("")
    steps.append(f"✓ Bob sends B = {B} to Alice (publicly)")
    steps.append("")
    
    # Step 4: Alice Computes Shared Secret
    steps.append("STEP 4: Alice Computes the Shared Secret")
    steps.append("-" * 50)
    steps.append(f"Alice receives Bob's public key B = {B}")
    steps.append(f"Alice calculates: K_A = B^a mod P")
    steps.append(f"K_A = {B}^{a} mod {P}")
    
    K_A = power(B, a, P)
    steps.append(f"K_A = {K_A}")
    steps.append("")
    
    # Step 5: Bob Computes Shared Secret
    steps.append("STEP 5: Bob Computes the Shared Secret")
    steps.append("-" * 50)
    steps.append(f"Bob receives Alice's public key A = {A}")
    steps.append(f"Bob calculates: K_B = A^b mod P")
    steps.append(f"K_B = {A}^{b} mod {P}")
    
    K_B = power(A, b, P)
    steps.append(f"K_B = {K_B}")
    steps.append("")
    
    # Step 6: Verification
    steps.append("STEP 6: Verification")
    steps.append("-" * 50)
    steps.append(f"Alice's shared secret: K_A = {K_A}")
    steps.append(f"Bob's shared secret:   K_B = {K_B}")
    steps.append("")
    
    if K_A == K_B:
        steps.append(f"✓ SUCCESS! Both parties have the same shared secret: {K_A}")
        steps.append("")
        steps.append("This shared secret can now be used for secure communication!")
    else:
        steps.append("✗ ERROR: Shared secrets do not match!")
    
    steps.append("")
    steps.append("=" * 50)
    steps.append("SECURITY NOTE:")
    steps.append("- Private keys (a, b) remain secret")
    steps.append("- Public keys (A, B) are transmitted openly")
    steps.append("- Shared secret is never transmitted")
    steps.append("=" * 50)
    
    result = {
        "P": P,
        "G": G,
        "alice_private": a,
        "bob_private": b,
        "alice_public": A,
        "bob_public": B,
        "shared_secret_alice": K_A,
        "shared_secret_bob": K_B,
        "success": K_A == K_B
    }
    
    return result, steps

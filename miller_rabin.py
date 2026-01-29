number = int(input("Enter a no: "))

def prime(number):
    if number <= 2 or number % 2 == 0:
        print("Composite")
        return

    # STEP 1: n-1 = 2^k * m
    n = number - 1
    i = 1

    while True:
        n2 = pow(2, i)
        m = n / n2
        if not m.is_integer():
            k = i - 1
            m = int(n / pow(2, k))
            break
        i += 1

    # STEP 2: choose base a = 2
    a = 2
    b = pow(a, m, number)

    if b == 1 or b == number - 1:
        print("Probably Prime")
        return

    # STEP 3: square b
    for _ in range(k - 1):
        b = (b * b) % number
        if b == number - 1:
            print("Probably Prime")
            return
        if b == 1:
            print("Composite")
            return

    print("Composite")

prime(number)

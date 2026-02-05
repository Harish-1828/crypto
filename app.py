from flask import Flask, render_template, request
import playfair
import affine
import vigenere
import euclidean_gcd
import fermat

def is_prime(number):
    """Miller-Rabin primality test"""
    steps = []
    
    if number <= 2 or number % 2 == 0:
        return "Composite", ["Number is even or ≤ 2: Composite"]

    steps.append(f"Given n = {number}")
    steps.append("")
    
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
    
    steps.append(f"Step 1:")
    steps.append(f"{n} = 2^{k} × {m}")
    steps.append(f"So k = {k}, and m = {m}")
    steps.append("")

    # STEP 2: choose base a = 2
    a = 2
    b = pow(a, m, number)
    
    steps.append(f"Step 3:")
    steps.append(f"b₀ = {a}^{m} (mod {number}) = {b}")
    steps.append(f"Is b₀ = ±1 (mod {number})? {'YES' if (b == 1 or b == number - 1) else 'NO'}")

    if b == 1 or b == number - 1:
        steps.append("")
        steps.append("→ Probably Prime")
        return "Probably Prime", steps

    # STEP 3: square b
    steps.append("")
    prev_b = b
    for idx in range(k - 1):
        b = (b * b) % number
        steps.append(f"b_{idx+1} = {prev_b}² (mod {number})")
        steps.append(f"b_{idx+1} = {b}")
        steps.append(f"Is b_{idx+1} = ±1 (mod {number})? {'YES' if (b == 1 or b == number - 1) else 'NO'}")
        
        if b == number - 1:
            steps.append("")
            steps.append("→ Probably Prime")
            return "Probably Prime", steps
        if b == 1:
            steps.append("")
            steps.append("→ Composite")
            return "Composite", steps
        steps.append("")
        prev_b = b

    steps.append("→ Composite")
    return "Composite", steps

app = Flask(
    __name__,
    template_folder='.',
    static_folder='.'
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.html")
def index_html():
    # Provide an alias so navigating directly to /index.html works
    return render_template("index.html")

@app.route("/playfair", methods=["GET", "POST"])
def playfair_page():
    result = ""
    matrix = None
    key = ""
    
    if request.method == "POST":
        key = request.form.get("key", "")
        text = request.form.get("text", "")
        mode = request.form.get("mode", "")
        
        if key:
            matrix = playfair.get_key_matrix(key)
        
        if mode in ["encrypt", "decrypt"] and text and key:
            if mode == "encrypt":
                result = playfair.playfair_encrypt(text, key)
            else:
                result = playfair.playfair_decrypt(text, key)

    return render_template("playfair.html", result=result, matrix=matrix, key=key)

@app.route("/affine", methods=["GET", "POST"])
def affine_page():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        mode = request.form["mode"]

        a, b = 3, 7  # fixed values

        if mode == "encrypt":
            result = affine.affine_encrypt(text, a, b)
        else:
            result = affine.affine_decrypt(text, a, b)

    return render_template("affine.html", result=result)

@app.route("/vigenere", methods=["GET", "POST"])
def vigenere_page():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        key = "KEY"  # fixed key
        mode = request.form["mode"]

        if mode == "encrypt":
            result = vigenere.vigenere_encrypt(text, key)
        else:
            result = vigenere.vigenere_decrypt(text, key)

    return render_template("vigenere.html", result=result)

@app.route("/miller_rabin", methods=["GET", "POST"])
def miller_rabin_page():
    result = None
    if request.method == "POST":
        try:
            number = int(request.form.get("number", 0))
            prime_result, steps = is_prime(number)
            result = {
                "status": prime_result,
                "steps": steps
            }
        except ValueError:
            result = {
                "status": "Invalid input",
                "steps": ["Please enter a valid number"]
            }

    return render_template("miller_rabin.html", result=result)

@app.route("/euclidean_gcd", methods=["GET", "POST"])
def euclidean_gcd_page():
    result = None
    if request.method == "POST":
        try:
            num1 = int(request.form.get("num1", 0))
            num2 = int(request.form.get("num2", 0))
            mode = request.form.get("mode", "basic")
            
            if mode == "extended":
                gcd, x, y, steps = euclidean_gcd.extended_euclidean_gcd(num1, num2)
                result = {
                    "gcd_text": f"GCD({num1}, {num2}) = {gcd}",
                    "extended": f"{num1} × ({x}) + {num2} × ({y}) = {gcd}",
                    "steps": steps
                }
            else:
                gcd, steps = euclidean_gcd.euclidean_gcd(num1, num2)
                result = {
                    "gcd_text": f"GCD({num1}, {num2}) = {gcd}",
                    "steps": steps
                }
        except ValueError:
            result = {
                "gcd_text": "Invalid input",
                "steps": ["Please enter valid numbers"]
            }
    
    return render_template("euclidean_gcd.html", result=result)

@app.route("/fermat", methods=["GET", "POST"])
def fermat_page():
    result = None
    if request.method == "POST":
        try:
            n = int(request.form.get("number", 0))
            k = int(request.form.get("iterations", 5))
            
            if k < 1 or k > 20:
                k = 5
            
            prime_result, steps = fermat.is_prime(n, k)
            result = {
                "status": prime_result,
                "steps": steps
            }
        except ValueError:
            result = {
                "status": "Invalid input",
                "steps": ["Please enter valid numbers"]
            }
    
    return render_template("fermat.html", result=result)

if __name__ == "__main__":
    # Run on port 5500 as requested
    app.run(debug=True, port=5500)

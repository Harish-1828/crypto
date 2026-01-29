from flask import Flask, render_template, request
import playfair
import affine
import vigenere

def is_prime(number):
    """Miller-Rabin primality test"""
    if number <= 2 or number % 2 == 0:
        return "Composite"

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
        return "Probably Prime"

    # STEP 3: square b
    for _ in range(k - 1):
        b = (b * b) % number
        if b == number - 1:
            return "Probably Prime"
        if b == 1:
            return "Composite"

    return "Composite"

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
    result = ""
    if request.method == "POST":
        try:
            number = int(request.form.get("number", 0))
            result = is_prime(number)
        except ValueError:
            result = "Invalid input"

    return render_template("miller_rabin.html", result=result)

if __name__ == "__main__":
    # Run on port 5500 as requested
    app.run(debug=True, port=5500)

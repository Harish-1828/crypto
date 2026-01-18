from flask import Flask, render_template, request
import playfair
import affine
import vigenere

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

if __name__ == "__main__":
    # Run on port 5500 as requested
    app.run(debug=True, port=5500)

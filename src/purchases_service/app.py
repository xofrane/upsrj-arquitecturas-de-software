from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "src/purchases_service/purchases.json"

def load_purchases():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_purchases(purchases):
    with open(DATA_FILE, "w") as f:
        json.dump(purchases, f, indent=4)

@app.route("/")
def home():
    purchases = load_purchases()
    return render_template("purchases.html", purchases=purchases)

@app.route("/create", methods=["GET", "POST"])
def create_purchase():
    if request.method == "POST":
        user_id = int(request.form["user_id"])
        product_id = int(request.form["product_id"])

        # Validar existencia de usuario y producto
        user_resp = requests.get(f"http://127.0.0.1:5003/api/users/{user_id}")
        product_resp = requests.get(f"http://127.0.0.1:5005/api/products/{product_id}")

        if user_resp.status_code != 200 or product_resp.status_code != 200:
            return "Usuario o producto no encontrado", 400

        purchases = load_purchases()
        new_purchase = {
            "id": len(purchases) + 1,
            "user_id": user_id,
            "product_id": product_id,
            "timestamp": datetime.now().isoformat()
        }
        purchases.append(new_purchase)
        save_purchases(purchases)
        return redirect(url_for("home"))

    return render_template("create_purchase.html")

if __name__ == "__main__":
    app.run(port=5006, debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import requests
from datetime import datetime
import os

app = Flask(__name__)

USERS_API_URL = "http://127.0.0.1:5003/api/users"
PRODUCTS_API_URL = "http://127.0.0.1:5005/api/products"

DATA_FILE = os.path.join(os.path.dirname(__file__), "purchases.json")

def load_purchases():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_purchases(purchases):
    with open(DATA_FILE, "w") as f:
        json.dump(purchases, f, indent=4)

# 🔹 GET /purchases
@app.route("/purchases")
def get_purchases():
    purchases = load_purchases()
    return render_template("purchases.html", purchases=purchases, title="Compras")

@app.route("/purchases/<int:user_id>")
def get_purchases_by_user(user_id):
    try:
        purchases = [p for p in load_purchases() if p.get("user_id") == user_id]
    except Exception:
        purchases = []

    # Siempre devolver 200 (aunque la lista esté vacía)
    return render_template("purchases.html", purchases=purchases, title="Compras"), 200

# 🔹 POST /purchases
@app.route("/purchases", methods=["POST"])
def create_purchase():
    data = request.get_json() if request.is_json else request.form

    user_id = data.get("user_id")
    product_id = data.get("product_id")

    # Validar campos requeridos
    if not user_id or not product_id:
        return jsonify({"error": "user_id y product_id son requeridos"}), 400

    try:
        user_id = int(user_id)
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": "IDs deben ser enteros"}), 400

    # Validar existencia de usuario y producto
    user_resp = requests.get(f"{USERS_API_URL}/{user_id}")
    product_resp = requests.get(f"{PRODUCTS_API_URL}/{product_id}")

    if user_resp.status_code != 200:
        return jsonify({"error": "Usuario no encontrado"}), 404
    if product_resp.status_code != 200:
        return jsonify({"error": "Producto no encontrado"}), 404

    purchases = load_purchases()
    new_purchase = {
        "id": len(purchases) + 1,
        "user_id": user_id,
        "product_id": product_id,
        "timestamp": datetime.now().isoformat()
    }
    purchases.append(new_purchase)
    save_purchases(purchases)

    # Devolver HTML (para test que busca "purchase-card")
    return render_template("purchases.html", purchases=purchases, title="Compras")

if __name__ == "__main__":
    app.run(port=5006, debug=True)

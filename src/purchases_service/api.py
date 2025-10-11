from flask import Flask, jsonify, request
import json
from datetime import datetime
import os

app = Flask(__name__)
USERS_API_URL = "http://127.0.0.1:5003/api/users"
PRODUCTS_API_URL = "http://127.0.0.1:5005/api/products"


DATA_FILE = os.path.join(os.path.dirname(__file__), "purchases.json")

# -------------------
# Funciones auxiliares
# -------------------
def load_purchases():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_purchases(purchases):
    with open(DATA_FILE, "w") as f:
        json.dump(purchases, f, indent=4)

# -------------------
# Rutas del API
# -------------------

# Obtener todas las compras
@app.route("/api/purchases", methods=["GET"])
def get_all_purchases():
    return jsonify(load_purchases())

# Obtener una compra por ID
@app.route("/api/purchases/<int:purchase_id>", methods=["GET"])
def get_purchase_by_id(purchase_id):
    purchases = load_purchases()
    for p in purchases:
        if p["id"] == purchase_id:
            return jsonify(p)
    return jsonify({"error": "Compra no encontrada"}), 404

# Crear nueva compra
@app.route("/api/purchases", methods=["POST"])
def create_purchase():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    # Verificar que user_id y product_id existan
    user_resp = requests.get(f"{USERS_API_URL}/{user_id}")
    product_resp = requests.get(f"{PRODUCTS_API_URL}/{product_id}")

    if user_resp.status_code != 200:
        return jsonify({"error": f"Usuario {user_id} no encontrado"}), 404
    if product_resp.status_code != 200:
        return jsonify({"error": f"Producto {product_id} no encontrado"}), 404

    purchases = load_purchases()
    new_purchase = {
        "id": len(purchases) + 1,
        "user_id": data["user_id"],
        "product_id": data["product_id"],
        "timestamp": datetime.now().isoformat()
    }
    purchases.append(new_purchase)
    save_purchases(purchases)
    return jsonify(new_purchase), 201

# -------------------
# Iniciar el servidor
# -------------------
if __name__ == "__main__":
    app.run(port=5007, debug=True)

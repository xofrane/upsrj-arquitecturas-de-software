# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: api.py
# Descripción: RESTful API de microservicio
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify
import requests
from common.utils import get_host
from common.vars import GATEWAY_API_URL, USER_API_URL, PRODUCT_API_URL

app = Flask(__name__)

USERS_API_URL = "http://127.0.0.1:5003/api/users"
PRODUCTS_API_URL = "http://127.0.0.1:5005/api/products"
PURCHASES_API_URL = "http://127.0.0.1:5007/api/purchases"


@app.route("/api/all")
def get_all():
    users = requests.get(USERS_API_URL).json()
    products = requests.get(PRODUCTS_API_URL).json()
    purchases = requests.get(PURCHASES_API_URL).json()
    return jsonify({
        "users": users,
        "products": products,
        "purchases": purchases
    })


@app.route("/api/users/<int:user_id>/purchases")
def get_user_purchases(user_id):
    # 1️⃣ Obtener usuario
    user_resp = requests.get(f"{USERS_API_URL}/{user_id}")
    if user_resp.status_code != 200:
        return jsonify({"error": "Usuario no encontrado"}), 404
    user = user_resp.json()

    # 2️⃣ Obtener todas las compras
    purchases_resp = requests.get(PURCHASES_API_URL)
    purchases = purchases_resp.json()

    # 3️⃣ Filtrar las compras de ese usuario
    user_purchases = [p for p in purchases if p["user_id"] == user_id]

    # 4️⃣ Obtener los productos relacionados
    products_resp = requests.get(PRODUCTS_API_URL)
    products = products_resp.json()

    # 5️⃣ Enlazar productos con las compras
    detailed_purchases = []
    for purchase in user_purchases:
        product = next((prod for prod in products if prod["id"] == purchase["product_id"]), None)
        if product:
            detailed_purchases.append({
                "purchase_id": purchase["id"],
                "product_name": product["name"],
            })

    # 6️⃣ Respuesta final
    return jsonify({
        "user": user,
        "purchases": detailed_purchases
    })


if __name__ == "__main__":
    app.run(port=5001, debug=True)
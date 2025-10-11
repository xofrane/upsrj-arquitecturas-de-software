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
from common.utils import load_item, get_host
from common.vars import USERS_FILE, USER_API_URL

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = load_item(USERS_FILE)
    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    users = load_item(USERS_FILE)
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'El campo "name" es obligatorio'}), 400

    users = load_item(USERS_FILE)
    new_user = {
        'id': len(users) + 1,
        'name': name,
        'purchased_products': data.get('purchased_products', [])
    }
    users.append(new_user)
    save_item(USERS_FILE, users)
    return jsonify(new_user), 201

# ==========================================
# PUT: actualizar un usuario existente
# ==========================================
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json() or {}
    users = load_item(USERS_FILE)
    for i, u in enumerate(users):
        if u['id'] == user_id:
            if 'name' in data:
                users[i]['name'] = data['name']
            if 'purchased_products' in data:
                users[i]['purchased_products'] = data['purchased_products']
            save_item(USERS_FILE, users)
            return jsonify(users[i])
    return jsonify({'error': 'Usuario no encontrado'}), 404

# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == '__main__':
    app.run(port=get_host(USER_API_URL), debug=True)

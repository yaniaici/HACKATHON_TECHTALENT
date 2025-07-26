from flask import Blueprint, request, jsonify
from project.server.app.controllers.producto import (
    get_productos_controller, create_producto_controller, update_producto_controller, delete_producto_controller
)

producto_bp = Blueprint('producto', __name__, url_prefix='/producto')

@producto_bp.route('', methods=['GET'])
def get_productos():
    return get_productos_controller()

@producto_bp.route('', methods=['POST', 'OPTIONS'])
def create_producto():
    if request.method == 'OPTIONS':
        # Responder a preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response, 200
    
    return create_producto_controller(request)

@producto_bp.route('/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    return update_producto_controller(producto_id, request)

@producto_bp.route('/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    return delete_producto_controller(producto_id) 
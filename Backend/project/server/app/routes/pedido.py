from flask import Blueprint, request, jsonify
from project.server.app.controllers.pedido import (
    get_pedidos_controller, create_pedido_controller, update_pedido_controller, 
    delete_pedido_controller, get_pedido_by_id_controller
)

pedido_bp = Blueprint('pedido', __name__, url_prefix='/pedido')

@pedido_bp.route('', methods=['GET'])
def get_pedidos():
    return get_pedidos_controller()

@pedido_bp.route('', methods=['POST', 'OPTIONS'])
def create_pedido():
    if request.method == 'OPTIONS':
        # Responder a preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response, 200
    
    return create_pedido_controller(request)

@pedido_bp.route('/<int:pedido_id>', methods=['GET'])
def get_pedido_by_id(pedido_id):
    return get_pedido_by_id_controller(pedido_id)

@pedido_bp.route('/<int:pedido_id>', methods=['PUT'])
def update_pedido(pedido_id):
    return update_pedido_controller(pedido_id, request)

@pedido_bp.route('/<int:pedido_id>', methods=['DELETE'])
def delete_pedido(pedido_id):
    return delete_pedido_controller(pedido_id) 
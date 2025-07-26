from flask import Blueprint, request, jsonify
from project.server.app.controllers.pedido import (
    get_pedidos_controller, create_pedido_controller, update_pedido_controller, delete_pedido_controller
)

pedido_bp = Blueprint('pedido', __name__, url_prefix='/pedido')

@pedido_bp.route('', methods=['GET'])
def get_pedidos():
    return get_pedidos_controller()

@pedido_bp.route('', methods=['POST'])
def create_pedido():
    return create_pedido_controller(request)

@pedido_bp.route('/<int:pedido_id>', methods=['PUT'])
def update_pedido(pedido_id):
    return update_pedido_controller(pedido_id, request)

@pedido_bp.route('/<int:pedido_id>', methods=['DELETE'])
def delete_pedido(pedido_id):
    return delete_pedido_controller(pedido_id) 
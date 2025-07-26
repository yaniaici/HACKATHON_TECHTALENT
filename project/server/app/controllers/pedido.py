from flask import request, jsonify
from project.server.app.services.pedido import (
    get_pedidos_service, create_pedido_service, update_pedido_service, delete_pedido_service
)
from project.server.app.models.pedido import PedidoSchema
from marshmallow import ValidationError

pedido_schema = PedidoSchema()

def get_pedidos_controller():
    pedidos = get_pedidos_service()
    return jsonify(pedidos), 200

def create_pedido_controller(req):
    try:
        data = req.get_json()
        pedido_data = pedido_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    result = create_pedido_service(pedido_data)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result), 201

def update_pedido_controller(pedido_id, req):
    try:
        data = req.get_json()
        pedido_data = pedido_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    result = update_pedido_service(pedido_id, pedido_data)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result), 200

def delete_pedido_controller(pedido_id):
    result = delete_pedido_service(pedido_id)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result), 200 
from flask import request, jsonify
from project.server.app.services.pedido import (
    get_pedidos_service, create_pedido_service, update_pedido_service, 
    delete_pedido_service, get_pedido_by_id_service
)
from project.server.app.models.pedido import PedidoSchema
from marshmallow import ValidationError

pedido_schema = PedidoSchema()

def get_pedidos_controller():
    try:
        pedidos = get_pedidos_service()
        return jsonify(pedidos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_pedido_controller(req):
    try:
        data = req.get_json()
        if not data:
            return jsonify({'error': 'Se requiere un body JSON'}), 400
        
        validated_data = pedido_schema.load(data)
        result = create_pedido_service(validated_data)
        
        if result.get('error'):
            return jsonify(result), 400
        return jsonify(result), 201
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_pedido_controller(pedido_id, req):
    try:
        data = req.get_json()
        if not data:
            return jsonify({'error': 'Se requiere un body JSON'}), 400
        
        # Solo validar campos que se pueden actualizar
        allowed_fields = ['destino', 'estado']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return jsonify({'error': 'No hay campos válidos para actualizar'}), 400
        
        result = update_pedido_service(pedido_id, update_data)
        
        if result.get('error'):
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_pedido_controller(pedido_id):
    try:
        result = delete_pedido_service(pedido_id)
        if result.get('error'):
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_pedido_by_id_controller(pedido_id):
    try:
        pedido = get_pedido_by_id_service(pedido_id)
        if not pedido:
            return jsonify({'error': 'Pedido no encontrado'}), 404
        return jsonify(pedido), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
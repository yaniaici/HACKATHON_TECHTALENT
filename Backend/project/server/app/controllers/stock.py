from flask import request, jsonify
from project.server.app.services.producto import (
    get_producto_stock_service,
    update_producto_stock_service,
    get_productos_stock_bajo_service,
    get_movimientos_stock_service,
    verificar_stock_disponible_service
)
from project.server.app.models.producto import StockUpdateSchema
from marshmallow import ValidationError

stock_update_schema = StockUpdateSchema()

def get_producto_stock_controller(producto_id):
    try:
        stock_info = get_producto_stock_service(producto_id)
        if not stock_info:
            return jsonify({'error': 'Producto no encontrado'}), 404
        return jsonify(stock_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_producto_stock_controller(producto_id, req):
    try:
        data = req.get_json()
        if not data:
            return jsonify({'error': 'Se requiere un body JSON'}), 400
        
        validated_data = stock_update_schema.load(data)
        result = update_producto_stock_service(producto_id, validated_data)
        
        if result.get('error'):
            return jsonify(result), 400
        return jsonify(result), 200
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_productos_stock_bajo_controller():
    try:
        limite = request.args.get('limite', 10, type=int)
        productos = get_productos_stock_bajo_service(limite)
        return jsonify({
            'productos': productos,
            'limite': limite,
            'count': len(productos)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_movimientos_stock_controller():
    try:
        producto_id = request.args.get('producto_id', type=int)
        limit = request.args.get('limit', 50, type=int)
        movimientos = get_movimientos_stock_service(producto_id, limit)
        return jsonify({
            'movimientos': movimientos,
            'count': len(movimientos)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def verificar_stock_disponible_controller(producto_id, req):
    try:
        cantidad = request.args.get('cantidad', type=int)
        if not cantidad:
            return jsonify({'error': 'Se requiere el parámetro cantidad'}), 400
        
        result = verificar_stock_disponible_service(producto_id, cantidad)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
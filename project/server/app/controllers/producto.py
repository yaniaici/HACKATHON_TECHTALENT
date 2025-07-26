from flask import request, jsonify
from project.server.app.services.producto import (
    get_productos_service, create_producto_service, update_producto_service, delete_producto_service
)
from project.server.app.models.producto import ProductoSchema
from marshmallow import ValidationError

producto_schema = ProductoSchema()

def get_productos_controller():
    productos = get_productos_service()
    return jsonify(productos), 200

def create_producto_controller(req):
    try:
        data = req.get_json()
        producto_data = producto_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    result = create_producto_service(producto_data)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result), 201

def update_producto_controller(producto_id, req):
    try:
        data = req.get_json()
        producto_data = producto_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    result = update_producto_service(producto_id, producto_data)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result), 200

def delete_producto_controller(producto_id):
    result = delete_producto_service(producto_id)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result), 200 
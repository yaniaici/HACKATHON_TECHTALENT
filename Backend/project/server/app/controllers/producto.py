from flask import request, jsonify
from project.server.app.services.producto import (
    get_productos_service, create_producto_service, update_producto_service, delete_producto_service
)
from project.server.app.models.producto import ProductoSchema
from marshmallow import ValidationError, EXCLUDE

producto_schema = ProductoSchema(unknown=EXCLUDE)

def get_productos_controller():
    productos = get_productos_service()
    productos_bilingues = []
    for p in productos:
        productos_bilingues.append({
            'id': p['id'],
            'nombre': p['nombre'],
            'name': p['nombre'],
            'tipo': p.get('tipo'),
            'category': p.get('tipo'),
            'alergenos': p.get('alergenos'),
            'allergens': p.get('alergenos'),
            'paradero': p.get('paradero'),
            'provider': p.get('paradero'),
            'origen': p.get('origen'),
            'origin': p.get('origen'),
            'id_vendedor': p.get('id_vendedor'),
            'sellerId': p.get('id_vendedor'),
            'stock': p.get('stock'),
            'image': None,  # Puedes agregar lógica para imágenes si existe
            'precio': p.get('precio', 10.0),
            'price': p.get('precio', 10.0)
        })
    return jsonify({'success': True, 'productos': productos_bilingues}), 200

def create_producto_controller(req):
    try:
        data = req.get_json()
        # Mapear campos del frontend a los del backend
        if 'name' in data:
            data['nombre'] = data.pop('name')
        if 'price' in data:
            data['precio'] = data.pop('price')
        if 'category' in data:
            data['tipo'] = data.pop('category')
        if 'provider' in data:
            data['paradero'] = data.pop('provider')
        if 'origin' in data:
            data['origen'] = data.pop('origin')
        if 'allergens' in data:
            data['alergenos'] = data.pop('allergens')
        data.pop('image', None)
        
        # Asignar valores por defecto para campos requeridos
        if 'stock' not in data:
            data['stock'] = 10  # Stock inicial por defecto
        if 'id_vendedor' not in data:
            data['id_vendedor'] = 1  # Vendedor por defecto (ID 1)
        
        producto_data = producto_schema.load(data)
    except ValidationError as err:
        return jsonify({'success': False, 'error': err.messages}), 400
    result = create_producto_service(producto_data)
    if result.get('error'):
        return jsonify({'success': False, 'error': result.get('error')}), 400
    return jsonify({'success': True, 'message': result.get('message')}), 201

def update_producto_controller(producto_id, req):
    try:
        data = req.get_json()
        # Mapear campos del frontend a los del backend
        if 'name' in data:
            data['nombre'] = data.pop('name')
        if 'price' in data:
            data['precio'] = data.pop('price')
        if 'category' in data:
            data['tipo'] = data.pop('category')
        if 'provider' in data:
            data['paradero'] = data.pop('provider')
        if 'origin' in data:
            data['origen'] = data.pop('origin')
        if 'allergens' in data:
            data['alergenos'] = data.pop('allergens')
        data.pop('image', None)
        
        # Para actualización, no asignamos valores por defecto ya que solo actualizamos los campos enviados
        producto_data = producto_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({'success': False, 'error': err.messages}), 400
    result = update_producto_service(producto_id, producto_data)
    if result.get('error'):
        return jsonify({'success': False, 'error': result.get('error')}), 400
    return jsonify({'success': True, 'message': result.get('message')}), 200

def delete_producto_controller(producto_id):
    result = delete_producto_service(producto_id)
    if result.get('error'):
        return jsonify({'success': False, 'error': result.get('error')}), 400
    return jsonify({'success': True, 'message': result.get('message')}), 200 
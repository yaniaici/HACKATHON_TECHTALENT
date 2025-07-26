from flask import request, jsonify
from project.server.app.services.usuario import (
    get_usuarios_service, create_usuario_service, update_usuario_service, delete_usuario_service
)
from project.server.app.models.usuario import UsuarioSchema
from marshmallow import ValidationError

usuario_schema = UsuarioSchema()


def get_usuarios_controller():
    usuarios = get_usuarios_service()
    return jsonify({'success': True, 'usuarios': usuarios}), 200


def create_usuario_controller(req):
    try:
        data = req.get_json()
        usuario_data = usuario_schema.load(data)
    except ValidationError as err:
        return jsonify({'success': False, 'error': err.messages}), 400
    result = create_usuario_service(usuario_data)
    if result.get('error'):
        return jsonify({'success': False, 'error': result.get('error')}), 400
    return jsonify({'success': True, 'message': 'Usuario creado correctamente', 'id': result.get('id')}), 201


def update_usuario_controller(usuario_id, req):
    try:
        data = req.get_json()
        usuario_data = usuario_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({'success': False, 'error': err.messages}), 400
    result = update_usuario_service(usuario_id, usuario_data)
    if result.get('error'):
        return jsonify({'success': False, 'error': result.get('error')}), 400
    return jsonify({'success': True, 'message': 'Usuario actualizado correctamente'}), 200


def delete_usuario_controller(usuario_id):
    result = delete_usuario_service(usuario_id)
    if result.get('error'):
        return jsonify({'success': False, 'error': result.get('error')}), 400
    return jsonify({'success': True, 'message': 'Usuario eliminado correctamente'}), 200 
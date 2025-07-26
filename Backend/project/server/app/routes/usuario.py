from flask import Blueprint, request, jsonify
from project.server.app.controllers.usuario import (
    get_usuarios_controller, create_usuario_controller, update_usuario_controller, delete_usuario_controller
)

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('', methods=['GET'])
def get_usuarios():
    return get_usuarios_controller()

@usuario_bp.route('', methods=['POST', 'OPTIONS'])
def create_usuario():
    if request.method == 'OPTIONS':
        # Responder a preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response, 200
    
    return create_usuario_controller(request)

@usuario_bp.route('/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    return update_usuario_controller(usuario_id, request)

@usuario_bp.route('/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    return delete_usuario_controller(usuario_id) 
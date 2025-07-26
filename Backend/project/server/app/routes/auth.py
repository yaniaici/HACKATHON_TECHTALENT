from flask import Blueprint, request, jsonify
from project.server.app.controllers.auth import login_controller

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
 
@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Responder a preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response, 200
    
    return login_controller(request) 
from flask import Blueprint, request, jsonify
from project.server.app.controllers.auth import login_controller

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    return login_controller(request) 
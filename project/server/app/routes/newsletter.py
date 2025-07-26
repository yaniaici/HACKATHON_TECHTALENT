from flask import Blueprint, request
from project.server.app.controllers.newsletter import (
    suscribir_newsletter_controller,
    desuscribir_newsletter_controller,
    get_suscriptores_controller,
    enviar_newsletter_controller
)

newsletter_bp = Blueprint('newsletter', __name__)

@newsletter_bp.route('/newsletter/suscribir', methods=['POST'])
def suscribir_newsletter():
    return suscribir_newsletter_controller(request)

@newsletter_bp.route('/newsletter/desuscribir', methods=['POST'])
def desuscribir_newsletter():
    return desuscribir_newsletter_controller(request)

@newsletter_bp.route('/newsletter/suscriptores', methods=['GET'])
def get_suscriptores():
    return get_suscriptores_controller()

@newsletter_bp.route('/newsletter/enviar', methods=['POST'])
def enviar_newsletter():
    return enviar_newsletter_controller(request)
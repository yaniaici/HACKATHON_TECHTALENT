from flask import jsonify
from project.server.app.services.newsletter import (
    suscribir_newsletter_service,
    desuscribir_newsletter_service,
    get_suscriptores_service,
    enviar_newsletter_service
)
import logging

def suscribir_newsletter_controller(request):
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email es requerido'}), 400
        
        result = suscribir_newsletter_service(email)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result), 201
        
    except Exception as e:
        logging.error(f"Error en controlador suscribir newsletter: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

def desuscribir_newsletter_controller(request):
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email es requerido'}), 400
        
        result = desuscribir_newsletter_service(email)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        logging.error(f"Error en controlador desuscribir newsletter: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

def get_suscriptores_controller():
    try:
        result = get_suscriptores_service()
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify({'suscriptores': result}), 200
        
    except Exception as e:
        logging.error(f"Error en controlador obtener suscriptores: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

def enviar_newsletter_controller(request):
    try:
        data = request.get_json()
        asunto = data.get('asunto')
        html_content = data.get('html_content')
        sender_email = data.get('sender_email')
        
        if not all([asunto, html_content, sender_email]):
            return jsonify({'error': 'Asunto, html_content y sender_email son requeridos'}), 400
        
        result = enviar_newsletter_service(asunto, html_content, sender_email)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        logging.error(f"Error en controlador enviar newsletter: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500
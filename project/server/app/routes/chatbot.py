from flask import Blueprint, request, jsonify
from project.server.app.controllers.chatbot import (
    process_chatbot_query_controller,
    search_products_controller,
    create_order_controller,
    get_products_by_type_controller,
    get_products_by_origin_controller,
    get_products_without_allergens_controller,
    get_orders_by_status_controller,
    get_marketplace_stats_controller,
    test_ollama_connection_controller
)

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@chatbot_bp.route('/query', methods=['POST'])
def process_query():
    """
    Endpoint principal del chatbot
    POST /chatbot/query
    Body: {"query": "¿Qué productos tienes disponibles?"}
    """
    return process_chatbot_query_controller()

@chatbot_bp.route('/search', methods=['GET'])
def search_products():
    """
    Buscar productos por nombre o palabra clave
    GET /chatbot/search?q=manzana
    """
    return search_products_controller()

@chatbot_bp.route('/create-order', methods=['POST'])
def create_order():
    """
    Crear pedido desde el chatbot
    POST /chatbot/create-order
    Body: {"id_usuario": 1, "id_producto": 12, "contenido": "2kg de manzanas", "destino": "Calle Mayor 1"}
    """
    return create_order_controller()

@chatbot_bp.route('/products/<product_type>', methods=['GET'])
def get_products_by_type(product_type):
    """
    Obtener productos por tipo
    GET /chatbot/products/fruta
    """
    return get_products_by_type_controller(product_type)

@chatbot_bp.route('/products/origin/<origin>', methods=['GET'])
def get_products_by_origin(origin):
    """
    Obtener productos por origen
    GET /chatbot/products/origin/Tarragona
    """
    return get_products_by_origin_controller(origin)

@chatbot_bp.route('/products/no-allergens', methods=['GET'])
def get_products_without_allergens():
    """
    Obtener productos sin alérgenos
    GET /chatbot/products/no-allergens
    """
    return get_products_without_allergens_controller()

@chatbot_bp.route('/orders/<status>', methods=['GET'])
def get_orders_by_status(status):
    """
    Obtener pedidos por estado
    GET /chatbot/orders/pendiente
    """
    return get_orders_by_status_controller(status)

@chatbot_bp.route('/stats', methods=['GET'])
def get_marketplace_stats():
    """
    Obtener estadísticas del marketplace
    GET /chatbot/stats
    """
    return get_marketplace_stats_controller()

@chatbot_bp.route('/test-connection', methods=['GET'])
def test_ollama_connection():
    """
    Probar conexión con Ollama
    GET /chatbot/test-connection
    """
    return test_ollama_connection_controller() 
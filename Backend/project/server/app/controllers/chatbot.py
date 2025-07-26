from flask import request, jsonify
from project.server.app.services.chatbot import ChatbotService
from marshmallow import Schema, fields, ValidationError

class ChatbotQuerySchema(Schema):
    query = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)

class CreateOrderSchema(Schema):
    id_usuario = fields.Int(required=True)
    id_producto = fields.Int(required=True)
    contenido = fields.Str(required=True)
    destino = fields.Str(required=True)

chatbot_query_schema = ChatbotQuerySchema()
create_order_schema = CreateOrderSchema()
chatbot_service = ChatbotService()

def process_chatbot_query_controller():
    """
    Controlador para procesar consultas del chatbot
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Se requiere un body JSON'}), 400
        
        # Validar datos de entrada
        validated_data = chatbot_query_schema.load(data)
        
        # Procesar consulta
        result = chatbot_service.process_query(validated_data['query'])
        
        return jsonify(result), 200
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def search_products_controller():
    """
    Controlador para buscar productos por nombre o palabra clave
    """
    try:
        search_term = request.args.get('q', '').strip()
        if not search_term:
            return jsonify({'error': 'Se requiere el parámetro de búsqueda "q"'}), 400
        
        products = chatbot_service.search_products_by_name(search_term)
        return jsonify({
            'search_term': search_term,
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_order_controller():
    """
    Controlador para crear pedidos desde el chatbot
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Se requiere un body JSON'}), 400
        
        # Validar datos de entrada
        validated_data = create_order_schema.load(data)
        
        # Crear pedido
        result = chatbot_service.create_order_from_chat(validated_data)
        
        if result.get('error'):
            return jsonify(result), 400
        return jsonify(result), 201
        
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_products_by_origin_controller(origin: str):
    """
    Controlador para obtener productos por origen
    """
    try:
        products = chatbot_service.get_products_by_origin(origin)
        return jsonify({
            'origin': origin,
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_products_without_allergens_controller():
    """
    Controlador para obtener productos sin alérgenos
    """
    try:
        products = chatbot_service.get_products_without_allergens()
        return jsonify({
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_products_by_type_controller(product_type: str):
    """
    Controlador para obtener productos por tipo
    """
    try:
        products = chatbot_service.get_products_by_type(product_type)
        return jsonify({
            'product_type': product_type,
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_orders_by_status_controller(status: str):
    """
    Controlador para obtener pedidos por estado
    """
    try:
        orders = chatbot_service.get_orders_by_status(status)
        return jsonify({
            'status': status,
            'orders': orders,
            'count': len(orders)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_marketplace_stats_controller():
    """
    Controlador para obtener estadísticas del marketplace
    """
    try:
        stats = chatbot_service.get_marketplace_stats()
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def test_ollama_connection_controller():
    """
    Controlador para probar la conexión con Ollama
    """
    try:
        is_connected = chatbot_service.test_ollama_connection()
        return jsonify({
            'connected': is_connected,
            'message': 'Conexión exitosa con Ollama' if is_connected else 'Error de conexión con Ollama'
        }), 200
        
    except Exception as e:
        return jsonify({
            'connected': False,
            'error': str(e)
        }), 500 
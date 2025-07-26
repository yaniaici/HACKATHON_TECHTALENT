from flask import Blueprint, request, jsonify
from project.server.app.controllers.stock import (
    get_producto_stock_controller,
    update_producto_stock_controller,
    get_productos_stock_bajo_controller,
    get_movimientos_stock_controller,
    verificar_stock_disponible_controller
)

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

@stock_bp.route('/producto/<int:producto_id>', methods=['GET'])
def get_producto_stock(producto_id):
    return get_producto_stock_controller(producto_id)

@stock_bp.route('/producto/<int:producto_id>/ajuste', methods=['POST'])
def update_producto_stock(producto_id):
    return update_producto_stock_controller(producto_id, request)

@stock_bp.route('/productos/stock-bajo', methods=['GET'])
def get_productos_stock_bajo():
    return get_productos_stock_bajo_controller()

@stock_bp.route('/movimientos', methods=['GET'])
def get_movimientos_stock():
    return get_movimientos_stock_controller()

@stock_bp.route('/verificar/<int:producto_id>', methods=['GET'])
def verificar_stock_disponible(producto_id):
    return verificar_stock_disponible_controller(producto_id, request) 
from flask import Flask
from project.server.config import DevelopmentConfig
from dotenv import load_dotenv
from project.server.app.routes.usuario import usuario_bp
from project.server.app.routes.producto import producto_bp
from project.server.app.routes.pedido import pedido_bp
from project.server.app.routes.auth import auth_bp
from project.server.app.routes.chatbot import chatbot_bp
from project.server.app.routes.stock import stock_bp
from project.server.app.utils.logging import setup_logging
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    setup_logging()

    # Habilitar CORS para todos los orígenes y métodos (solo desarrollo)
    CORS(app)

    app.register_blueprint(usuario_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(stock_bp)

    return app 
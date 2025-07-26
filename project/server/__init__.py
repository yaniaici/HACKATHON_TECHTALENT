# project/server/__init__.py


#################
#### imports ####
#################

import os
from flask import Flask
from project.server.config import DevelopmentConfig
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Importar y registrar blueprints aquí (se agregarán después)
    # from .app.routes.usuario import usuario_bp
    # app.register_blueprint(usuario_bp)

    return app

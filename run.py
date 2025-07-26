from project.server.app import create_app
from flask_swagger_ui import get_swaggerui_blueprint
import os

app = create_app()

# Configuración de Swagger UI
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Marketplace Tarragona API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Servir el archivo swagger.yaml desde la carpeta docs usando ruta absoluta
from flask import send_from_directory

@app.route('/static/swagger.yaml')
def send_swagger():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'project', 'server', 'app', 'docs')
    return send_from_directory(dir_path, 'swagger.yaml')

if __name__ == '__main__':
    app.run(debug=True) 
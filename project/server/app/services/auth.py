from project.server.app.db.connection import get_db
from flask_bcrypt import Bcrypt
import logging

bcrypt = Bcrypt()

def login_service(login_data):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, correo, contraseña, rol FROM usuario WHERE correo=%s", (login_data['correo'],))
        user = cursor.fetchone()
        if user and bcrypt.check_password_hash(user['contraseña'], login_data['contraseña']):
            return {'id': user['id'], 'correo': user['correo'], 'rol': user['rol']}
        else:
            return {'error': 'Credenciales inválidas'}
    except Exception as e:
        logging.error(f"Error en login: {e}")
        return {'error': str(e)}
    finally:
        cursor.close() 
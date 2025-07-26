from project.server.app.db.connection import get_db
from flask_bcrypt import Bcrypt
import logging

bcrypt = Bcrypt()

def login_service(login_data):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, nombre, apellido1, apellido2, correo, direccion, telefono, rol, contraseña 
            FROM usuario 
            WHERE correo=%s
        """, (login_data['correo'],))
        user = cursor.fetchone()
        if user and bcrypt.check_password_hash(user['contraseña'], login_data['contraseña']):
            return {
                'id': user['id'],
                'nombre': user['nombre'],
                'name': user['nombre'],
                'primer_apellido': user['apellido1'],
                'firstSurname': user['apellido1'],
                'segundo_apellido': user['apellido2'],
                'secondSurname': user['apellido2'],
                'correo': user['correo'],
                'email': user['correo'],
                'direccion': user['direccion'],
                'address': user['direccion'],
                'telefono': user['telefono'],
                'phone': user['telefono'],
                'rol': user['rol'],
                'role': user['rol']
            }
        else:
            return {'error': 'Credenciales inválidas'}
    except Exception as e:
        logging.error(f"Error en login: {e}")
        return {'error': str(e)}
    finally:
        cursor.close() 
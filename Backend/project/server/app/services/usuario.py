from project.server.app.db.connection import get_db
from flask_bcrypt import Bcrypt
from flask import current_app
import logging

bcrypt = Bcrypt()

def get_usuarios_service():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, apellido1, apellido2, correo, direccion, telefono, rol FROM usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    return usuarios


def create_usuario_service(usuario_data):
    db = get_db()
    cursor = db.cursor()
    try:
        hashed_password = bcrypt.generate_password_hash(usuario_data['contraseña']).decode('utf-8')
        cursor.execute("""
            INSERT INTO usuario (nombre, apellido1, apellido2, correo, contraseña, direccion, telefono, rol)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            usuario_data['nombre'], usuario_data['apellido1'], usuario_data.get('apellido2'),
            usuario_data['correo'], hashed_password, usuario_data['direccion'], usuario_data['telefono'], usuario_data['rol']
        ))
        db.commit()
        usuario_id = cursor.lastrowid
        cursor.close()
        return {'id': usuario_id, 'correo': usuario_data['correo']}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al crear usuario: {e}")
        return {'error': str(e)}


def update_usuario_service(usuario_id, usuario_data):
    db = get_db()
    cursor = db.cursor()
    try:
        campos = []
        valores = []
        for key, value in usuario_data.items():
            if key == 'contraseña':
                value = bcrypt.generate_password_hash(value).decode('utf-8')
            campos.append(f"{key}=%s")
            valores.append(value)
        valores.append(usuario_id)
        sql = f"UPDATE usuario SET {', '.join(campos)} WHERE id=%s"
        cursor.execute(sql, valores)
        db.commit()
        cursor.close()
        return {'id': usuario_id}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar usuario: {e}")
        return {'error': str(e)}


def delete_usuario_service(usuario_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM usuario WHERE id=%s", (usuario_id,))
        db.commit()
        cursor.close()
        return {'id': usuario_id}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al eliminar usuario: {e}")
        return {'error': str(e)} 
from project.server.app.db.connection import get_db
import logging

def get_productos_service():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, tipo, alergenos, paradero, origen, id_vendedor FROM producto")
    productos = cursor.fetchall()
    cursor.close()
    return productos

def create_producto_service(producto_data):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO producto (nombre, tipo, alergenos, paradero, origen, id_vendedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            producto_data['nombre'], producto_data['tipo'], producto_data.get('alergenos'), producto_data['paradero'],
            producto_data['origen'], producto_data['id_vendedor']
        ))
        db.commit()
        producto_id = cursor.lastrowid
        cursor.close()
        return {'id': producto_id}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al crear producto: {e}")
        return {'error': str(e)}

def update_producto_service(producto_id, producto_data):
    db = get_db()
    cursor = db.cursor()
    try:
        campos = []
        valores = []
        for key, value in producto_data.items():
            campos.append(f"{key}=%s")
            valores.append(value)
        valores.append(producto_id)
        sql = f"UPDATE producto SET {', '.join(campos)} WHERE id=%s"
        cursor.execute(sql, valores)
        db.commit()
        cursor.close()
        return {'id': producto_id}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar producto: {e}")
        return {'error': str(e)}

def delete_producto_service(producto_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM producto WHERE id=%s", (producto_id,))
        db.commit()
        cursor.close()
        return {'id': producto_id}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al eliminar producto: {e}")
        return {'error': str(e)} 
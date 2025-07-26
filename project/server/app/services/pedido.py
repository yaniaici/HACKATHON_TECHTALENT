from project.server.app.db.connection import get_db
import logging

def get_pedidos_service():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, id_usuario, id_producto, contenido, destino, estado FROM pedido")
    pedidos = cursor.fetchall()
    cursor.close()
    return pedidos

def create_pedido_service(pedido_data):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO pedido (id_usuario, id_producto, contenido, destino, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            pedido_data['id_usuario'], pedido_data['id_producto'], pedido_data['contenido'],
            pedido_data['destino'], pedido_data['estado']
        ))
        db.commit()
        pedido_id = cursor.lastrowid
        cursor.close()
        return {'id': pedido_id}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al crear pedido: {e}")
        return {'error': str(e)}

def update_pedido_service(pedido_id, pedido_data):
    db = get_db()
    cursor = db.cursor()
    try:
        campos = []
        valores = []
        for key, value in pedido_data.items():
            campos.append(f"{key}=%s")
            valores.append(value)
        valores.append(pedido_id)
        sql = f"UPDATE pedido SET {', '.join(campos)} WHERE id=%s"
        cursor.execute(sql, valores)
        db.commit()
        cursor.close()
        return {'id': pedido_id}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar pedido: {e}")
        return {'error': str(e)}

def delete_pedido_service(pedido_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM pedido WHERE id=%s", (pedido_id,))
        db.commit()
        cursor.close()
        return {'id': pedido_id}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al eliminar pedido: {e}")
        return {'error': str(e)} 
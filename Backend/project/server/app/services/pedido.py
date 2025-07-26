from project.server.app.db.connection import get_db
from project.server.app.services.producto import verificar_stock_disponible_service, update_producto_stock_service
import logging

def get_pedidos_service():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id, p.id_usuario, p.fecha_pedido, p.destino, p.estado,
                   u.nombre as cliente_nombre, u.correo as cliente_email
            FROM pedido p
            JOIN usuario u ON p.id_usuario = u.id
            ORDER BY p.fecha_pedido DESC
        """)
        pedidos = cursor.fetchall()
        
        # Obtener detalles de cada pedido
        for pedido in pedidos:
            cursor.execute("""
                SELECT dp.id_producto, dp.cantidad, pr.nombre as producto_nombre, pr.tipo
                FROM detalle_pedido dp
                JOIN producto pr ON dp.id_producto = pr.id
                WHERE dp.id_pedido = %s
            """, (pedido['id'],))
            pedido['detalles'] = cursor.fetchall()
        
        cursor.close()
        return pedidos
    except Exception as e:
        logging.error(f"Error al obtener pedidos: {e}")
        return []

def create_pedido_service(pedido_data):
    db = get_db()
    cursor = db.cursor()
    try:
        # Validar stock de todos los productos
        detalles = pedido_data['detalles']
        for detalle in detalles:
            stock_check = verificar_stock_disponible_service(
                detalle['id_producto'], 
                detalle['cantidad']
            )
            if not stock_check['disponible']:
                return {
                    'error': f"Stock insuficiente para el producto ID {detalle['id_producto']}. "
                             f"Disponible: {stock_check['stock_actual']}, "
                             f"Solicitado: {stock_check['cantidad_solicitada']}"
                }
        
        # Crear el pedido
        cursor.execute("""
            INSERT INTO pedido (id_usuario, destino, estado)
            VALUES (%s, %s, %s)
        """, (pedido_data['id_usuario'], pedido_data['destino'], pedido_data['estado']))
        
        pedido_id = cursor.lastrowid
        
        # Crear detalles del pedido y actualizar stock
        for detalle in detalles:
            # Insertar detalle
            cursor.execute("""
                INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
                VALUES (%s, %s, %s)
            """, (pedido_id, detalle['id_producto'], detalle['cantidad']))
            
            # Actualizar stock (venta)
            stock_update = update_producto_stock_service(detalle['id_producto'], {
                'cantidad': detalle['cantidad'],
                'tipo_movimiento': 'venta',
                'id_usuario': pedido_data['id_usuario']
            })
            
            if stock_update.get('error'):
                db.rollback()
                return {'error': f"Error al actualizar stock: {stock_update['error']}"}
        
        db.commit()
        cursor.close()
        return {'id': pedido_id, 'message': 'Pedido creado correctamente'}
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error al crear pedido: {e}")
        return {'error': str(e)}

def update_pedido_service(pedido_id, pedido_data):
    db = get_db()
    cursor = db.cursor()
    try:
        # Actualizar pedido principal
        if 'destino' in pedido_data or 'estado' in pedido_data:
            fields = []
            values = []
            for key, value in pedido_data.items():
                if key in ['destino', 'estado']:
                    fields.append(f"{key} = %s")
                    values.append(value)
            values.append(pedido_id)
            
            query = f"UPDATE pedido SET {', '.join(fields)} WHERE id = %s"
            cursor.execute(query, values)
        
        # Si se actualiza el estado a cancelado, devolver stock
        if pedido_data.get('estado') == 'cancelado':
            cursor.execute("""
                SELECT dp.id_producto, dp.cantidad
                FROM detalle_pedido dp
                WHERE dp.id_pedido = %s
            """, (pedido_id,))
            detalles = cursor.fetchall()
            
            for detalle in detalles:
                # Devolver stock (devolución)
                stock_update = update_producto_stock_service(detalle[0], {
                    'cantidad': detalle[1],
                    'tipo_movimiento': 'devolucion',
                    'id_usuario': pedido_data.get('id_usuario')
                })
                
                if stock_update.get('error'):
                    logging.error(f"Error al devolver stock: {stock_update['error']}")
        
        db.commit()
        cursor.close()
        return {'message': 'Pedido actualizado correctamente'}
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar pedido: {e}")
        return {'error': str(e)}

def delete_pedido_service(pedido_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # Obtener detalles antes de eliminar para devolver stock
        cursor.execute("""
            SELECT dp.id_producto, dp.cantidad
            FROM detalle_pedido dp
            WHERE dp.id_pedido = %s
        """, (pedido_id,))
        detalles = cursor.fetchall()
        
        # Devolver stock de cada producto
        for detalle in detalles:
            stock_update = update_producto_stock_service(detalle[0], {
                'cantidad': detalle[1],
                'tipo_movimiento': 'devolucion'
            })
            
            if stock_update.get('error'):
                logging.error(f"Error al devolver stock: {stock_update['error']}")
        
        # Eliminar detalles primero
        cursor.execute("DELETE FROM detalle_pedido WHERE id_pedido = %s", (pedido_id,))
        
        # Eliminar pedido
        cursor.execute("DELETE FROM pedido WHERE id = %s", (pedido_id,))
        
        db.commit()
        cursor.close()
        return {'message': 'Pedido eliminado correctamente'}
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error al eliminar pedido: {e}")
        return {'error': str(e)}

def get_pedido_by_id_service(pedido_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id, p.id_usuario, p.fecha_pedido, p.destino, p.estado,
                   u.nombre as cliente_nombre, u.correo as cliente_email
            FROM pedido p
            JOIN usuario u ON p.id_usuario = u.id
            WHERE p.id = %s
        """, (pedido_id,))
        pedido = cursor.fetchone()
        
        if pedido:
            cursor.execute("""
                SELECT dp.id_producto, dp.cantidad, pr.nombre as producto_nombre, pr.tipo, pr.stock
                FROM detalle_pedido dp
                JOIN producto pr ON dp.id_producto = pr.id
                WHERE dp.id_pedido = %s
            """, (pedido_id,))
            pedido['detalles'] = cursor.fetchall()
        
        cursor.close()
        return pedido
        
    except Exception as e:
        logging.error(f"Error al obtener pedido: {e}")
        return None
from project.server.app.db.connection import get_db
import logging

def get_productos_service():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, tipo, alergenos, paradero, origen, stock, id_vendedor FROM producto")
    productos = cursor.fetchall()
    cursor.close()
    return productos

def create_producto_service(producto_data):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO producto (nombre, tipo, alergenos, paradero, origen, stock, id_vendedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            producto_data['nombre'], producto_data['tipo'], producto_data.get('alergenos'),
            producto_data['paradero'], producto_data['origen'], producto_data.get('stock', 0),
            producto_data['id_vendedor']
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
        # Construir query dinámica
        fields = []
        values = []
        for key, value in producto_data.items():
            if key != 'id':
                fields.append(f"{key} = %s")
                values.append(value)
        values.append(producto_id)
        
        query = f"UPDATE producto SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        return {'message': 'Producto actualizado correctamente'}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar producto: {e}")
        return {'error': str(e)}

def delete_producto_service(producto_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM producto WHERE id = %s", (producto_id,))
        db.commit()
        cursor.close()
        return {'message': 'Producto eliminado correctamente'}
    except Exception as e:
        db.rollback()
        logging.error(f"Error al eliminar producto: {e}")
        return {'error': str(e)}

def get_producto_stock_service(producto_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id, p.nombre, p.stock, p.id_vendedor, u.nombre as vendedor_nombre
            FROM producto p
            JOIN usuario u ON p.id_vendedor = u.id
            WHERE p.id = %s
        """, (producto_id,))
        producto = cursor.fetchone()
        cursor.close()
        return producto
    except Exception as e:
        logging.error(f"Error al obtener stock del producto: {e}")
        return None

def update_producto_stock_service(producto_id, stock_data):
    db = get_db()
    cursor = db.cursor()
    try:
        # Obtener información del producto
        cursor.execute("SELECT stock, id_vendedor FROM producto WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        if not producto:
            return {'error': 'Producto no encontrado'}
        
        stock_actual = producto[0]
        id_vendedor = producto[1]
        nueva_cantidad = stock_data['cantidad']
        tipo_movimiento = stock_data['tipo_movimiento']
        
        # Calcular nuevo stock según tipo de movimiento
        if tipo_movimiento == 'venta':
            nuevo_stock = stock_actual - nueva_cantidad
            if nuevo_stock < 0:
                return {'error': 'Stock insuficiente'}
        elif tipo_movimiento == 'ajuste':
            nuevo_stock = nueva_cantidad
        elif tipo_movimiento == 'devolucion':
            nuevo_stock = stock_actual + nueva_cantidad
        else:
            return {'error': 'Tipo de movimiento no válido'}
        
        # Actualizar stock del producto
        cursor.execute("UPDATE producto SET stock = %s WHERE id = %s", (nuevo_stock, producto_id))
        
        # Registrar movimiento de stock
        cursor.execute("""
            INSERT INTO movimiento_stock (id_producto, id_vendedor, cantidad, tipo_movimiento, id_usuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (producto_id, id_vendedor, nueva_cantidad, tipo_movimiento, stock_data.get('id_usuario')))
        
        db.commit()
        cursor.close()
        return {
            'producto_id': producto_id,
            'stock_anterior': stock_actual,
            'stock_nuevo': nuevo_stock,
            'movimiento': tipo_movimiento
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar stock: {e}")
        return {'error': str(e)}

def get_productos_stock_bajo_service(limite=10):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id, p.nombre, p.tipo, p.stock, p.paradero, p.origen, u.nombre as vendedor
            FROM producto p
            JOIN usuario u ON p.id_vendedor = u.id
            WHERE p.stock <= %s
            ORDER BY p.stock ASC
        """, (limite,))
        productos = cursor.fetchall()
        cursor.close()
        return productos
    except Exception as e:
        logging.error(f"Error al obtener productos con stock bajo: {e}")
        return []

def get_movimientos_stock_service(producto_id=None, limit=50):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        if producto_id:
            cursor.execute("""
                SELECT ms.*, p.nombre as producto_nombre, u.nombre as vendedor_nombre
                FROM movimiento_stock ms
                JOIN producto p ON ms.id_producto = p.id
                JOIN usuario u ON ms.id_vendedor = u.id
                WHERE ms.id_producto = %s
                ORDER BY ms.fecha DESC
                LIMIT %s
            """, (producto_id, limit))
        else:
            cursor.execute("""
                SELECT ms.*, p.nombre as producto_nombre, u.nombre as vendedor_nombre
                FROM movimiento_stock ms
                JOIN producto p ON ms.id_producto = p.id
                JOIN usuario u ON ms.id_vendedor = u.id
                ORDER BY ms.fecha DESC
                LIMIT %s
            """, (limit,))
        movimientos = cursor.fetchall()
        cursor.close()
        return movimientos
    except Exception as e:
        logging.error(f"Error al obtener movimientos de stock: {e}")
        return []

def verificar_stock_disponible_service(producto_id, cantidad):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT stock FROM producto WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        cursor.close()
        
        if not producto:
            return {'disponible': False, 'error': 'Producto no encontrado'}
        
        stock_disponible = producto['stock']
        return {
            'disponible': stock_disponible >= cantidad,
            'stock_actual': stock_disponible,
            'cantidad_solicitada': cantidad,
            'stock_restante': stock_disponible - cantidad if stock_disponible >= cantidad else 0
        }
    except Exception as e:
        logging.error(f"Error al verificar stock: {e}")
        return {'disponible': False, 'error': str(e)} 
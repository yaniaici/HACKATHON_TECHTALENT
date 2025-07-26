from project.server.app.db.connection import get_db
import logging

def get_pedidos_service():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        # Obtener pedidos con sus detalles
        cursor.execute("""
            SELECT p.id, p.id_usuario, p.fecha_pedido, p.destino, p.estado,
                   dp.id as detalle_id, dp.id_producto, dp.cantidad,
                   pr.nombre as producto_nombre
            FROM pedido p
            LEFT JOIN detalle_pedido dp ON p.id = dp.id_pedido
            LEFT JOIN producto pr ON dp.id_producto = pr.id
            ORDER BY p.id, dp.id
        """)
        results = cursor.fetchall()
        
        # Agrupar pedidos con sus detalles
        pedidos = {}
        for row in results:
            pedido_id = row['id']
            if pedido_id not in pedidos:
                pedidos[pedido_id] = {
                    'id': row['id'],
                    'id_usuario': row['id_usuario'],
                    'fecha_pedido': row['fecha_pedido'],
                    'destino': row['destino'],
                    'estado': row['estado'],
                    'detalles': []
                }
            
            if row['detalle_id']:  # Si tiene detalles
                pedidos[pedido_id]['detalles'].append({
                    'id': row['detalle_id'],
                    'id_producto': row['id_producto'],
                    'cantidad': row['cantidad'],
                    'producto_nombre': row['producto_nombre']
                })
        
        cursor.close()
        return list(pedidos.values())
    except Exception as e:
        cursor.close()
        logging.error(f"Error al obtener pedidos: {e}")
        return {'error': str(e)}

def verificar_stock_disponible(cursor, detalles):
    """Verifica si hay stock suficiente para todos los productos del pedido"""
    productos_sin_stock = []
    
    for detalle in detalles:
        cursor.execute("""
            SELECT id, nombre, stock 
            FROM producto 
            WHERE id = %s
        """, (detalle['id_producto'],))
        
        producto = cursor.fetchone()
        if not producto:
            productos_sin_stock.append(f"Producto ID {detalle['id_producto']} no existe")
        elif producto[2] < detalle['cantidad']:  # stock < cantidad solicitada
            productos_sin_stock.append(f"{producto[1]}: stock disponible {producto[2]}, solicitado {detalle['cantidad']}")
    
    return productos_sin_stock

def actualizar_stock_productos(cursor, detalles, operacion='restar'):
    """Actualiza el stock de los productos (restar o sumar)"""
    for detalle in detalles:
        if operacion == 'restar':
            cursor.execute("""
                UPDATE producto 
                SET stock = stock - %s 
                WHERE id = %s
            """, (detalle['cantidad'], detalle['id_producto']))
        elif operacion == 'sumar':
            cursor.execute("""
                UPDATE producto 
                SET stock = stock + %s 
                WHERE id = %s
            """, (detalle['cantidad'], detalle['id_producto']))

def registrar_movimiento_stock(cursor, id_producto, id_vendedor, id_pedido, cantidad, tipo, id_usuario):
    """Registra un movimiento de stock para métricas de PowerBI"""
    cursor.execute("""
        INSERT INTO movimiento_stock (id_producto, id_vendedor, id_pedido, cantidad, tipo_movimiento, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_producto, id_vendedor, id_pedido, cantidad, tipo, id_usuario))

def obtener_vendedor_producto(cursor, id_producto):
    """Obtiene el id_vendedor de un producto"""
    cursor.execute("SELECT id_vendedor FROM producto WHERE id = %s", (id_producto,))
    result = cursor.fetchone()
    return result[0] if result else None

def create_pedido_service(pedido_data):
    db = get_db()
    cursor = db.cursor()
    try:
        # 1. Verificar stock disponible
        productos_sin_stock = verificar_stock_disponible(cursor, pedido_data['detalles'])
        if productos_sin_stock:
            cursor.close()
            return {'error': f"Stock insuficiente: {', '.join(productos_sin_stock)}"}
        
        # 2. Crear el pedido (encabezado)
        cursor.execute("""
            INSERT INTO pedido (id_usuario, destino, estado)
            VALUES (%s, %s, %s)
        """, (
            pedido_data['id_usuario'],
            pedido_data['destino'], 
            pedido_data['estado']
        ))
        
        pedido_id = cursor.lastrowid
        
        # 3. Insertar detalles del pedido y registrar movimientos
        for detalle in pedido_data['detalles']:
            # Insertar detalle del pedido
            cursor.execute("""
                INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
                VALUES (%s, %s, %s)
            """, (pedido_id, detalle['id_producto'], detalle['cantidad']))
            
            # Obtener el vendedor del producto
            id_vendedor = obtener_vendedor_producto(cursor, detalle['id_producto'])
            
            # Registrar el movimiento solo si el estado no es 'cancelado'
            if pedido_data['estado'] != 'cancelado' and id_vendedor:
                registrar_movimiento_stock(
                    cursor, 
                    detalle['id_producto'], 
                    id_vendedor, 
                    pedido_id, 
                    detalle['cantidad'], 
                    'venta', 
                    pedido_data['id_usuario']
                )
        
        # 4. Actualizar stock (solo si el estado no es 'cancelado')
        if pedido_data['estado'] != 'cancelado':
            actualizar_stock_productos(cursor, pedido_data['detalles'], 'restar')
        
        db.commit()
        cursor.close()
        return {'id': pedido_id, 'mensaje': 'Pedido creado exitosamente'}
        
    except Exception as e:
        db.rollback()
        cursor.close()
        logging.error(f"Error al crear pedido: {e}")
        return {'error': str(e)}

def update_pedido_service(pedido_id, pedido_data):
    db = get_db()
    cursor = db.cursor()
    try:
        # 1. Obtener estado actual del pedido
        cursor.execute("SELECT estado FROM pedido WHERE id = %s", (pedido_id,))
        pedido_actual = cursor.fetchone()
        if not pedido_actual:
            cursor.close()
            return {'error': 'Pedido no encontrado'}
        
        estado_anterior = pedido_actual[0]
        estado_nuevo = pedido_data.get('estado', estado_anterior)
        
        # 2. Obtener detalles actuales del pedido para gestión de stock
        cursor.execute("""
            SELECT dp.id_producto, dp.cantidad, p.id_vendedor
            FROM detalle_pedido dp
            JOIN producto p ON dp.id_producto = p.id
            WHERE dp.id_pedido = %s
        """, (pedido_id,))
        detalles_anteriores = [
            {
                'id_producto': row[0], 
                'cantidad': row[1], 
                'id_vendedor': row[2]
            } for row in cursor.fetchall()
        ]
        
        # 3. Gestionar cambios de stock según cambio de estado
        if estado_anterior != 'cancelado' and estado_nuevo == 'cancelado':
            # Devolver stock si se cancela el pedido
            actualizar_stock_productos(cursor, detalles_anteriores, 'sumar')
            # Registrar devolución
            for detalle in detalles_anteriores:
                registrar_movimiento_stock(
                    cursor, 
                    detalle['id_producto'], 
                    detalle['id_vendedor'], 
                    pedido_id, 
                    detalle['cantidad'], 
                    'devolucion', 
                    None  # No hay usuario específico en cancelación
                )
                
        elif estado_anterior == 'cancelado' and estado_nuevo != 'cancelado':
            # Verificar y restar stock si se reactiva el pedido
            productos_sin_stock = verificar_stock_disponible(cursor, detalles_anteriores)
            if productos_sin_stock:
                cursor.close()
                return {'error': f"No se puede reactivar. Stock insuficiente: {', '.join(productos_sin_stock)}"}
            actualizar_stock_productos(cursor, detalles_anteriores, 'restar')
            # Registrar nueva venta
            cursor.execute("SELECT id_usuario FROM pedido WHERE id = %s", (pedido_id,))
            id_usuario = cursor.fetchone()[0]
            for detalle in detalles_anteriores:
                registrar_movimiento_stock(
                    cursor, 
                    detalle['id_producto'], 
                    detalle['id_vendedor'], 
                    pedido_id, 
                    detalle['cantidad'], 
                    'venta', 
                    id_usuario
                )
        
        # 4. Actualizar campos del pedido
        campos = []
        valores = []
        for key, value in pedido_data.items():
            if key != 'detalles':  # Los detalles se manejan por separado
                campos.append(f"{key}=%s")
                valores.append(value)
        
        if campos:
            valores.append(pedido_id)
            sql = f"UPDATE pedido SET {', '.join(campos)} WHERE id=%s"
            cursor.execute(sql, valores)
        
        db.commit()
        cursor.close()
        return {'id': pedido_id, 'mensaje': 'Pedido actualizado exitosamente'}
        
    except Exception as e:
        db.rollback()
        cursor.close()
        logging.error(f"Error al actualizar pedido: {e}")
        return {'error': str(e)}

def delete_pedido_service(pedido_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # 1. Obtener detalles del pedido y estado antes de eliminar
        cursor.execute("""
            SELECT p.estado, p.id_usuario, dp.id_producto, dp.cantidad, pr.id_vendedor
            FROM pedido p
            LEFT JOIN detalle_pedido dp ON p.id = dp.id_pedido
            LEFT JOIN producto pr ON dp.id_producto = pr.id
            WHERE p.id = %s
        """, (pedido_id,))
        
        results = cursor.fetchall()
        if not results:
            cursor.close()
            return {'error': 'Pedido no encontrado'}
        
        estado = results[0][0]
        id_usuario = results[0][1]
        detalles = [
            {
                'id_producto': row[2], 
                'cantidad': row[3], 
                'id_vendedor': row[4]
            } for row in results if row[2]
        ]
        
        # 2. Devolver stock si el pedido no estaba cancelado
        if estado != 'cancelado' and detalles:
            actualizar_stock_productos(cursor, detalles, 'sumar')
            # Registrar devolución por eliminación
            for detalle in detalles:
                registrar_movimiento_stock(
                    cursor, 
                    detalle['id_producto'], 
                    detalle['id_vendedor'], 
                    pedido_id, 
                    detalle['cantidad'], 
                    'devolucion', 
                    id_usuario
                )
        
        # 3. Eliminar pedido (los detalles se eliminan automáticamente por CASCADE)
        cursor.execute("DELETE FROM pedido WHERE id = %s", (pedido_id,))
        
        db.commit()
        cursor.close()
        return {'id': pedido_id, 'mensaje': 'Pedido eliminado exitosamente'}
        
    except Exception as e:
        db.rollback()
        cursor.close()
        logging.error(f"Error al eliminar pedido: {e}")
        return {'error': str(e)}

def get_stock_producto_service(producto_id):
    """Servicio auxiliar para consultar stock de un producto específico"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, nombre, stock 
            FROM producto 
            WHERE id = %s
        """, (producto_id,))
        
        producto = cursor.fetchone()
        cursor.close()
        return producto if producto else {'error': 'Producto no encontrado'}
        
    except Exception as e:
        cursor.close()
        logging.error(f"Error al obtener stock: {e}")
        return {'error': str(e)}
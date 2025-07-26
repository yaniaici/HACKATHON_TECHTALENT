from project.server.app.db.connection import get_db
from project.server.app.utils.ollama_client import OllamaClient
import logging
import json

class ChatbotService:
    def __init__(self):
        self.ollama_client = OllamaClient()
    
    def process_query(self, user_query: str) -> dict:
        # 1. Detectar intención básica
        query_lower = user_query.lower()
        productos = []
        contexto_extra = ""
        
        # Detectar preguntas sobre stock
        if any(word in query_lower for word in ["stock", "disponible", "cantidad", "cuánto", "cuanto", "hay", "tienes"]):
            # Buscar productos mencionados en la pregunta
            productos_mentados = []
            for palabra in query_lower.split():
                if palabra in ["manzana", "naranja", "pera", "leche", "pan", "queso", "tomate", "aceite", "huevo", "miel"]:
                    productos_mentados.append(palabra)
            
            if productos_mentados:
                for producto in productos_mentados:
                    productos_encontrados = self.search_products_by_name(producto)
                    productos.extend(productos_encontrados)
                if productos:
                    contexto_extra = "Stock disponible: " + ", ".join([f"{p['nombre']}({p.get('stock', 0)})" for p in productos])
        
        # Detectar productos por tipo
        if not productos and ("producto" in query_lower or "fruta" in query_lower or "lácteo" in query_lower or "pan" in query_lower or "verdura" in query_lower or "aceite" in query_lower or "huevo" in query_lower or "miel" in query_lower or "carne" in query_lower):
            tipos = ["fruta", "lácteo", "panadería", "verdura", "aceite", "huevos", "miel", "carne de ternera"]
            for tipo in tipos:
                if tipo in query_lower:
                    productos = self.get_products_by_type(tipo)
                    contexto_extra = f"Productos de tipo {tipo}: " + ", ".join([f"{p['nombre']}({p.get('stock', 0)})" for p in productos])
                    break
        
        # Detectar productos por origen
        if not productos and ("tarragona" in query_lower or "origen" in query_lower):
            productos = self.get_products_by_origin("Tarragona")
            contexto_extra = "Productos de Tarragona: " + ", ".join([f"{p['nombre']}({p.get('stock', 0)})" for p in productos])
        
        # Detectar productos sin alérgenos
        if not productos and ("sin alérgenos" in query_lower or "no alérgenos" in query_lower):
            productos = self.get_products_without_allergens()
            contexto_extra = "Productos sin alérgenos: " + ", ".join([f"{p['nombre']}({p.get('stock', 0)})" for p in productos])
        
        # Detectar búsqueda por nombre
        if not productos and ("manzana" in query_lower or "naranja" in query_lower or "pera" in query_lower or "leche" in query_lower or "pan" in query_lower):
            palabras = ["manzana", "naranja", "pera", "leche", "pan"]
            for palabra in palabras:
                if palabra in query_lower:
                    productos = self.search_products_by_name(palabra)
                    contexto_extra = f"Productos que coinciden con '{palabra}': " + ", ".join([f"{p['nombre']}({p.get('stock', 0)})" for p in productos])
                    break
        
        # Detectar productos con stock bajo
        if "stock bajo" in query_lower or "poco stock" in query_lower or "agotándose" in query_lower:
            productos_stock_bajo = self.get_productos_stock_bajo()
            if productos_stock_bajo:
                productos = productos_stock_bajo
                contexto_extra = "Productos con stock bajo: " + ", ".join([f"{p['nombre']}({p['stock']})" for p in productos])
        
        # Si encontró productos, pasar la lista al LLM
        if productos:
            nombres = ", ".join([f"{p['nombre']}(stock:{p.get('stock', 0)})" for p in productos])
            contexto = self._get_marketplace_context() + f" | {contexto_extra}"
            prompt = f"{user_query}\nLista de productos encontrados: {nombres}"
            respuesta = self.ollama_client.generate_response(prompt, contexto)
            return {
                "productos": productos,
                "response": respuesta
            }
        
        # Si no es sobre productos, usar el flujo actual
        contexto = self._get_marketplace_context()
        respuesta = self.ollama_client.generate_response(user_query, contexto)
        return {
            "context": contexto,
            "query": user_query,
            "response": respuesta
        }
    
    def search_products_by_name(self, search_term: str) -> list:
        """
        Busca productos por nombre o palabra clave
        Args:
            search_term: Término de búsqueda
        Returns:
            Lista de productos que coinciden con la búsqueda
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        try:
            cursor.execute(
                "SELECT id, nombre, tipo, paradero, origen, alergenos, stock FROM producto WHERE nombre LIKE %s OR tipo LIKE %s OR origen LIKE %s",
                (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
            )
            products = cursor.fetchall()
            cursor.close()
            return products
            
        except Exception as e:
            logging.error(f"Error al buscar productos: {e}")
            return []
    
    def create_order_from_chat(self, order_data: dict) -> dict:
        """
        Crea un pedido desde el chatbot
        Args:
            order_data: Datos del pedido (id_usuario, id_producto, contenido, destino)
        Returns:
            Resultado de la creación del pedido
        """
        db = get_db()
        cursor = db.cursor()
        
        try:
            # Validar que el usuario y producto existan
            cursor.execute("SELECT id FROM usuario WHERE id = %s", (order_data['id_usuario'],))
            if not cursor.fetchone():
                return {'error': 'Usuario no encontrado'}
            
            cursor.execute("SELECT id, nombre FROM producto WHERE id = %s", (order_data['id_producto'],))
            producto = cursor.fetchone()
            if not producto:
                return {'error': 'Producto no encontrado'}
            
            # Crear el pedido
            cursor.execute("""
                INSERT INTO pedido (id_usuario, id_producto, contenido, destino, estado)
                VALUES (%s, %s, %s, %s, 'pendiente')
            """, (
                order_data['id_usuario'], order_data['id_producto'], 
                order_data['contenido'], order_data['destino']
            ))
            
            db.commit()
            pedido_id = cursor.lastrowid
            cursor.close()
            
            return {
                'pedido_id': pedido_id,
                'producto_nombre': producto[1],
                'contenido': order_data['contenido'],
                'estado': 'pendiente'
            }
            
        except Exception as e:
            db.rollback()
            logging.error(f"Error al crear pedido desde chatbot: {e}")
            return {'error': str(e)}
    
    def get_products_by_origin(self, origin: str) -> list:
        """
        Obtiene productos filtrados por origen
        Args:
            origin: Origen del producto
        Returns:
            Lista de productos del origen especificado
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        try:
            cursor.execute(
                "SELECT id, nombre, tipo, paradero, origen, stock FROM producto WHERE origen LIKE %s",
                (f"%{origin}%",)
            )
            products = cursor.fetchall()
            cursor.close()
            return products
            
        except Exception as e:
            logging.error(f"Error al obtener productos por origen: {e}")
            return []
    
    def get_products_without_allergens(self) -> list:
        """
        Obtiene productos sin alérgenos
        Returns:
            Lista de productos sin alérgenos
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        try:
            cursor.execute(
                "SELECT id, nombre, tipo, paradero, origen, stock FROM producto WHERE alergenos = '' OR alergenos IS NULL"
            )
            products = cursor.fetchall()
            cursor.close()
            return products
            
        except Exception as e:
            logging.error(f"Error al obtener productos sin alérgenos: {e}")
            return []
    
    def get_products_by_type(self, product_type: str) -> list:
        """
        Obtiene productos filtrados por tipo
        Args:
            product_type: Tipo de producto (fruta, carne, lácteo, etc.)
        Returns:
            Lista de productos del tipo especificado
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        try:
            cursor.execute(
                "SELECT id, nombre, tipo, paradero, origen, stock FROM producto WHERE tipo LIKE %s",
                (f"%{product_type}%",)
            )
            products = cursor.fetchall()
            cursor.close()
            return products
            
        except Exception as e:
            logging.error(f"Error al obtener productos por tipo: {e}")
            return []
    
    def get_orders_by_status(self, status: str) -> list:
        """
        Obtiene pedidos filtrados por estado
        Args:
            status: Estado del pedido (pendiente, enviado, entregado, cancelado)
        Returns:
            Lista de pedidos con el estado especificado
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        try:
            cursor.execute(
                "SELECT id, id_usuario, id_producto, contenido, destino, estado FROM pedido WHERE estado = %s",
                (status,)
            )
            orders = cursor.fetchall()
            cursor.close()
            return orders
            
        except Exception as e:
            logging.error(f"Error al obtener pedidos por estado: {e}")
            return []
    
    def get_marketplace_stats(self) -> dict:
        """
        Obtiene estadísticas del marketplace
        Returns:
            Diccionario con estadísticas
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        try:
            # Contar usuarios
            cursor.execute("SELECT COUNT(*) as total FROM usuario")
            total_users = cursor.fetchone()['total']
            
            # Contar productos
            cursor.execute("SELECT COUNT(*) as total FROM producto")
            total_products = cursor.fetchone()['total']
            
            # Contar pedidos
            cursor.execute("SELECT COUNT(*) as total FROM pedido")
            total_orders = cursor.fetchone()['total']
            
            # Contar pedidos por estado
            cursor.execute("SELECT estado, COUNT(*) as count FROM pedido GROUP BY estado")
            orders_by_status = cursor.fetchall()
            
            # Productos por tipo
            cursor.execute("SELECT tipo, COUNT(*) as count FROM producto GROUP BY tipo")
            products_by_type = cursor.fetchall()
            
            cursor.close()
            
            return {
                "total_users": total_users,
                "total_products": total_products,
                "total_orders": total_orders,
                "orders_by_status": orders_by_status,
                "products_by_type": products_by_type
            }
            
        except Exception as e:
            logging.error(f"Error al obtener estadísticas: {e}")
            return {}
    
    def _get_marketplace_context(self) -> str:
        """
        Obtiene información contextual del marketplace para el chatbot
        Returns:
            String con información del marketplace
        """
        try:
            stats = self.get_marketplace_stats()
            products_by_type = stats.get('products_by_type', [])
            types_info = ", ".join([f"{item['tipo']}({item['count']})" for item in products_by_type])

            context = f"Usuarios:{stats.get('total_users', 0)} Productos:{stats.get('total_products', 0)} Pedidos:{stats.get('total_orders', 0)} Tipos:{types_info}"
            return context
        except Exception as e:
            logging.error(f"Error al obtener contexto del marketplace: {e}")
            return "Marketplace disponible."
    
    def test_ollama_connection(self) -> bool:
        """
        Prueba la conexión con Ollama
        Returns:
            True si la conexión es exitosa
        """
        return self.ollama_client.test_connection() 

    def get_productos_stock_bajo(self, limite=10):
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
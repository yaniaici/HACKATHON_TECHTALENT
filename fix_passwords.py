#!/usr/bin/env python3
"""
Script para arreglar las contraseñas en la base de datos
Genera hashes válidos de bcrypt para todos los usuarios
"""

import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def fix_passwords():
    """Arregla todas las contraseñas en la base de datos"""
    
    # Configuración de la base de datos
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASS', ''),
        'database': os.getenv('DB_NAME', 'marketplace'),
        'port': int(os.getenv('DB_PORT', 3306))
    }
    
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Generar hash válido para '123456'
        password = '123456'
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        print(f"Hash generado para '{password}': {hashed_password.decode('utf-8')}")
        
        # Actualizar todas las contraseñas en la tabla usuario
        update_query = "UPDATE usuario SET contraseña = %s"
        cursor.execute(update_query, (hashed_password.decode('utf-8'),))
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar cuántos usuarios fueron actualizados
        cursor.execute("SELECT COUNT(*) FROM usuario")
        count = cursor.fetchone()[0]
        
        print(f"✅ {count} usuarios actualizados con contraseña '{password}'")
        print("🔑 Ahora puedes hacer login con cualquier usuario usando:")
        print(f"   Email: cualquier correo de la base de datos")
        print(f"   Contraseña: {password}")
        
        # Mostrar algunos usuarios para referencia
        cursor.execute("SELECT id, nombre, correo FROM usuario LIMIT 5")
        users = cursor.fetchall()
        
        print("\n📋 Usuarios disponibles para login:")
        for user in users:
            print(f"   ID: {user[0]} | Nombre: {user[1]} | Email: {user[2]}")
        
    except mysql.connector.Error as err:
        print(f"❌ Error de MySQL: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    print("🔧 Arreglando contraseñas en la base de datos...")
    fix_passwords()
    print("✅ Proceso completado") 
import mysql.connector
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

def fix_passwords():
    # Conectar a la base de datos
    db = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASS', ''),
        database=os.getenv('DB_NAME', 'marketplace'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    
    cursor = db.cursor()
    bcrypt = Bcrypt()
    
    # Generar hash válido para '123456'
    valid_hash = bcrypt.generate_password_hash('123456').decode('utf-8')
    print(f"Hash válido generado: {valid_hash}")
    
    # Actualizar todas las contraseñas
    update_query = "UPDATE usuario SET contraseña = %s"
    cursor.execute(update_query, (valid_hash,))
    db.commit()
    
    print(f"Se actualizaron {cursor.rowcount} usuarios")
    
    # Verificar que se actualizaron
    cursor.execute("SELECT id, correo FROM usuario")
    users = cursor.fetchall()
    print("Usuarios actualizados:")
    for user in users:
        print(f"ID: {user[0]}, Email: {user[1]}")
    
    cursor.close()
    db.close()
    print("¡Contraseñas actualizadas correctamente!")

if __name__ == "__main__":
    fix_passwords() 
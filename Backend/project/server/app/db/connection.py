import mysql.connector
from mysql.connector import Error
from flask import current_app, g
import logging

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB'],
                port=current_app.config['MYSQL_PORT']
            )
        except Error as e:
            logging.error(f"Error de conexión a MySQL: {e}")
            g.db = None
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close() 
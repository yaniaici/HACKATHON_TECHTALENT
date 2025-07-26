from project.server.app.db.connection import get_db
import logging
import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes para Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def suscribir_newsletter_service(email):
    """Suscribe un email a la newsletter"""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT IGNORE INTO newsletter_suscriptor (email) VALUES (%s)", (email,))
        db.commit()
        cursor.close()
        return {'mensaje': '¡Suscripción exitosa!'}
    except Exception as e:
        db.rollback()
        cursor.close()
        logging.error(f"Error al suscribir newsletter: {e}")
        return {'error': str(e)}

def desuscribir_newsletter_service(email):
    """Desuscribe un email de la newsletter"""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE newsletter_suscriptor SET activo = FALSE WHERE email = %s", (email,))
        db.commit()
        cursor.close()
        return {'mensaje': 'Desuscripción exitosa'}
    except Exception as e:
        db.rollback()
        cursor.close()
        logging.error(f"Error al desuscribir newsletter: {e}")
        return {'error': str(e)}

def get_suscriptores_service():
    """Obtiene todos los suscriptores activos"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT email, fecha_suscripcion FROM newsletter_suscriptor WHERE activo = TRUE")
        suscriptores = cursor.fetchall()
        cursor.close()
        return suscriptores
    except Exception as e:
        cursor.close()
        logging.error(f"Error al obtener suscriptores: {e}")
        return {'error': str(e)}

def get_gmail_service():
    """Configura y devuelve el servicio de Gmail API"""
    # Obtener la ruta del directorio actual del script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, 'credentials.json')
    token_path = os.path.join(current_dir, 'token.json')
    
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"No se encontró el archivo credentials.json en: {credentials_path}")
            
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(sender, to, subject, html_content):
    """Crea un mensaje de email en formato Gmail API"""
    message = MIMEText(html_content, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def enviar_newsletter_service(asunto, html_content, sender_email):
    """Envía newsletter a todos los suscriptores activos"""
    try:
        # Obtener suscriptores
        suscriptores = get_suscriptores_service()
        if isinstance(suscriptores, dict) and 'error' in suscriptores:
            return suscriptores
        
        if not suscriptores:
            return {'mensaje': 'No hay suscriptores activos'}
        
        # Configurar Gmail API
        service = get_gmail_service()
        
        enviados = 0
        errores = []
        
        # Enviar a cada suscriptor
        for suscriptor in suscriptores:
            try:
                message = create_message(sender_email, suscriptor['email'], asunto, html_content)
                service.users().messages().send(userId="me", body=message).execute()
                enviados += 1
                logging.info(f"Newsletter enviado a: {suscriptor['email']}")
            except Exception as e:
                error_msg = f"Error enviando a {suscriptor['email']}: {str(e)}"
                errores.append(error_msg)
                logging.error(error_msg)
        
        return {
            'mensaje': f'Newsletter enviado exitosamente',
            'enviados': enviados,
            'total_suscriptores': len(suscriptores),
            'errores': errores
        }
        
    except Exception as e:
        logging.error(f"Error general enviando newsletter: {e}")
        return {'error': str(e)}
from flask import jsonify
from project.server.app.services.auth import login_service
from marshmallow import Schema, fields, ValidationError

class LoginSchema(Schema):
    correo = fields.Email(required=True)
    contraseña = fields.Str(required=True)

login_schema = LoginSchema()

def login_controller(req):
    try:
        data = req.get_json()
        login_data = login_schema.load(data)
    except ValidationError as err:
        return jsonify({'success': False, 'error': err.messages}), 400
    
    result = login_service(login_data)
    
    if result.get('error'):
        return jsonify({'success': False, 'error': result.get('error')}), 401
    
    # Devolver formato estándar que espera el frontend
    return jsonify({
        'success': True,
        'user': result
    }), 200 
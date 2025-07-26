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
        return jsonify({'error': err.messages}), 400
    result = login_service(login_data)
    if result.get('error'):
        return jsonify(result), 401
    return jsonify(result), 200 
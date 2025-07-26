from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1))
    apellido1 = fields.Str(required=True, validate=validate.Length(min=1))
    apellido2 = fields.Str(required=False, allow_none=True)
    correo = fields.Email(required=True)
    contraseña = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    direccion = fields.Str(required=True)
    telefono = fields.Str(required=True, validate=validate.Length(min=7))
    rol = fields.Str(required=True, validate=validate.OneOf(["cliente", "vendedor"])) 
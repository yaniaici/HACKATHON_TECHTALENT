from marshmallow import Schema, fields, validate

class ProductoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1))
    tipo = fields.Str(required=True, validate=validate.Length(min=1))
    alergenos = fields.Str(required=False, allow_none=True)
    paradero = fields.Str(required=True)
    origen = fields.Str(required=True)
    id_vendedor = fields.Int(required=True) 
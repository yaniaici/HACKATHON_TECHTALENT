from marshmallow import Schema, fields, validate

class PedidoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_usuario = fields.Int(required=True)
    id_producto = fields.Int(required=True)
    contenido = fields.Str(required=True)
    destino = fields.Str(required=True)
    estado = fields.Str(required=True, validate=validate.OneOf(["pendiente", "enviado", "entregado", "cancelado"])) 
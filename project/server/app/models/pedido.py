from marshmallow import Schema, fields, validate

class DetallePedidoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_producto = fields.Int(required=True)
    cantidad = fields.Int(required=True, validate=validate.Range(min=1))

class PedidoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_usuario = fields.Int(required=True)
    fecha_pedido = fields.DateTime(dump_only=True)
    destino = fields.Str(required=True)
    estado = fields.Str(required=True, validate=validate.OneOf(["pendiente", "enviado", "entregado", "cancelado"]))
    detalles = fields.List(fields.Nested(DetallePedidoSchema), required=True)
from marshmallow import Schema, fields, validate

class PedidoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_usuario = fields.Int(required=True)
    fecha_pedido = fields.DateTime(dump_only=True)
    destino = fields.Str(required=True)
    estado = fields.Str(required=True, validate=validate.OneOf(["pendiente", "enviado", "entregado", "cancelado"]))
    detalles = fields.List(fields.Dict(), required=True)  # Lista de productos con cantidades

class DetallePedidoSchema(Schema):
    id_producto = fields.Int(required=True)
    cantidad = fields.Int(required=True, validate=validate.Range(min=1))

class MovimientoStockSchema(Schema):
    id = fields.Int(dump_only=True)
    id_producto = fields.Int(required=True)
    id_vendedor = fields.Int(required=True)
    id_pedido = fields.Int(allow_none=True)
    cantidad = fields.Int(required=True)
    tipo_movimiento = fields.Str(required=True, validate=validate.OneOf(["venta", "ajuste", "devolucion"]))
    fecha = fields.DateTime(dump_only=True)
    id_usuario = fields.Int(allow_none=True)

    
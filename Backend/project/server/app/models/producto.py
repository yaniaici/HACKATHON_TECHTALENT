from marshmallow import Schema, fields, validate

class ProductoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1))
    precio = fields.Decimal(required=True, validate=validate.Range(min=0))
    tipo = fields.Str(required=True, validate=validate.Length(min=1))
    alergenos = fields.Str(required=False, allow_none=True)
    paradero = fields.Str(required=True)
    origen = fields.Str(required=True)
    stock = fields.Int(required=True, validate=validate.Range(min=0))
    id_vendedor = fields.Int(required=True)

class StockUpdateSchema(Schema):
    cantidad = fields.Int(required=True)
    tipo_movimiento = fields.Str(required=True, validate=validate.OneOf(["venta", "ajuste", "devolucion"]))
    motivo = fields.Str(required=False, allow_none=True) 
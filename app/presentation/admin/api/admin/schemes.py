from marshmallow import Schema, fields


class AdminRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class AdminResponseSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)

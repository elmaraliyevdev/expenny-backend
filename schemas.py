from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=False)
    password = fields.Str(required=True, load_only=True)

from marshmallow import Schema, fields

class PlainItemSchema(Schema): 
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    tag_description = fields.Str()

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class PlainRoleSchema(Schema):
    id = fields.Int(dump_only=True)
    role = fields.Str(required=True)
    
    
class ItemUpdateSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)
    # store_update = fields.Bool(required=False)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    description = fields.Str(required=False)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(ItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema())
    tag = fields.Nested(PlainTagSchema())




class UserSchema(PlainUserSchema):
    roles = fields.List(fields.Nested(PlainRoleSchema), dump_only=True)
    #roles = fields.Str(load_default="user")
    #roles = fields.List(fields.Str(load_default="user"), dump_only=True)

class UserRegisterSchema(UserSchema):
    email = fields.Email(required=True)

class RoleSchema(PlainRoleSchema):
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class UserRoleSchema(Schema):
    message = fields.Str()
    user  = fields.Nested(UserSchema())
    role = fields.Nested(RoleSchema())

class BlacklistSchema(Schema):
    id = fields.Int(dump_only=True)
    token = fields.Str(required=False)
    blacklisted_on = fields.DateTime(dump_only=True)


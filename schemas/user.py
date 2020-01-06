from ma import ma
from models.user import UserModel
from flask_marshmallow import fields





class UserSchema(ma.ModelSchema):

    class Meta:
        model = UserModel
        load_only = ("password",)

    email = fields.Str(missing=None, required=True)
    password = fields.Str(missing=None, required=True)
    login = fields.Str(missing=None, required=True)



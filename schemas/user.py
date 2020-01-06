from ma import ma
from models.user import UserModel
from marshmallow import fields





class UserSchema(ma.ModelSchema):

    class Meta:
        model = UserModel
        load_only = ("password",)


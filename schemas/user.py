from ma import ma
from models.user import UserModel




class UserSchema(ma.ModelSchema):

    class Meta:
        model = UserModel
        load_only = ("password",)

    email = ma.fields.Email(missing=None, required=True)
    password = ma.fields.Email(missing=None, required=True)
    login = ma.fields.Email(missing=None, required=True)



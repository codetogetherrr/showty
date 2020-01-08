from ma import ma
from models.user import UserModel






class UserSchema(ma.ModelSchema):

    class Meta:
        model = UserModel
        load_only = ("password", "id", "image_id", "image_width", "image_height", "activated")
        dump_only = ("id", "activated")
        update_fields = ("description",)


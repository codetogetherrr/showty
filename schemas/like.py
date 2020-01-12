from ma import ma
from models.like import LikeModel


class LikeSchema(ma.ModelSchema):

    class Meta:
        model = LikeModel
        dump_only = ("user_id",)
        exclude = ("likes_id",)
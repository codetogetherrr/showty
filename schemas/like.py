from ma import ma
from models.like import LikeModel


class LikeSchema(ma.SQLAlchemySchema):

    class Meta:
        model = LikeModel
        dump_only = ("login",)
        exclude = ("likes_id",)

from ma import ma
from models.follow import FollowModel


class FollowSchema(ma.ModelSchema):

    class Meta:
        model = FollowModel
        dump_only = ("follower_id",)
        exclude = ("follow_id",)


class FollowGetSchema(ma.ModelSchema):

    class Meta:
        model = FollowModel

        exclude = ("follow_id",)
from ma import ma
from models.follow import FollowModel


class FollowSchema(ma.Schema):

    class Meta:
        model = FollowModel
        dump_only = ("follower_id",)
        exclude = ("follow_id",)


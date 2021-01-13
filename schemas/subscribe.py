from ma import ma
from models.subscribe import SubscribeModel


class SubscribeSchema(ma.Schema):

    class Meta:
        model = SubscribeModel
        dump_only = ("subscription_id",)
        exclude = ("subscription_id",)
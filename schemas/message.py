from ma import ma
from models.message import MessageModel


class MessageSchema(ma.ModelSchema):

    class Meta:
        model = MessageModel
        dump_only = ("sender", "receiver", "text", "createdAt")


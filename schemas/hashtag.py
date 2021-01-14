from ma import ma
from models.hashtag import HashtagModel


class HashtagSchema(ma.SQLAlchemySchema):

    class Meta:
        model = HashtagModel
        exclude = ("hashtag_id",)

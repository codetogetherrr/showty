from ma import ma
from models.hashtag import HashtagModel


class HashtagSchema(ma.ModelSchema):

    class Meta:
        model = HashtagModel
        exclude = ("hashtag_id",)

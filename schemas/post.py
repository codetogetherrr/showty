from ma import ma
from models.post import PostModel

class PostSchema(ma.SQLAlchemySchema):

    class Meta:
        model = PostModel
        dump_only = ("post_id","login", "date")


class PostUpdateSchema(ma.SQLAlchemySchema):

    class Meta:
        model = PostModel
        exclude = ("post_id", "login", "image_id", "image_width", "image_height", "date")

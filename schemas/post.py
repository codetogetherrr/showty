from ma import ma
from models.post import PostModel

class PostSchema(ma.ModelSchema):

class Meta:
    model = PostModel
    load_only = ("post_id",)
    dump_only = ("post_id",)

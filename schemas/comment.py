from ma import ma
from models.comment import CommentModel


class CommentSchema(ma.ModelSchema):

    class Meta:
        model = CommentModel
        dump_only = ("comment_date", "comment_id", "user_id")



class CommentUpdateSchema(ma.ModelSchema):

    class Meta:
        model = CommentModel
        exclude = ("comment_date", "comment_id", "user_id", "post_id")

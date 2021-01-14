from ma import ma
from models.comment import CommentModel


class CommentSchema(ma.SQLAlchemySchema):

    class Meta:
        model = CommentModel
        dump_only = ("comment_date", "comment_id", "login")



class CommentUpdateSchema(ma.SQLAlchemySchema):

    class Meta:
        model = CommentModel
        exclude = ("comment_date", "comment_id", "login", "post_id")

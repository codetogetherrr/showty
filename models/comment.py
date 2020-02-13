from db import db


class CommentModel(db.Model):

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    login = db.Column(db.String(80))
    comment = db.Column(db.String(500), nullable=False)
    comment_date = db.Column(db.DateTime)


    @classmethod
    def find_by_post_id(cls, post_id):
        all_comments = cls.query.filter_by(post_id=post_id).order_by(CommentModel.comment_date.asc())
        return all_comments

    @classmethod
    def find_by_comment_id(cls, comment_id):
        return cls.query.filter_by(comment_id=comment_id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

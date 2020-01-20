from db import db
import re


class HashtagModel(db.Model):

    __tablename__ = 'hashtags'

    hashtag_id = db.Column(db.Integer,primary_key=True)
    hashtag = db.Column(db.String(80), nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    comment_id = db.Column(db.Integer)

    @classmethod
    def find_hashtags_in_text(cls, text):
        hashtags = re.findall(r"#(\w+)", text)
        return hashtags

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

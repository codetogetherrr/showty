from db import db
from flask import jsonify
from flask_sqlalchemy import BaseQuery

class LikesModel(db.Model):

    __tablename__ = 'likes'

    likes_id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.String(80))
    
 
    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id
        

    @classmethod
    def find_by(cls, post_id, user_login):
        all_likes= cls.query.filter_by(post_id=post_id, user_id = user_login)
        return all_likes

    @classmethod
    def count_likes_post_id(cls, post_id):
        count_likes = cls.query.filter_by(post_id=post_id)
        return count_likes
    
    def json(self):
        return {'post_id' : self.post_id, \
                'user_id' : self.user_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


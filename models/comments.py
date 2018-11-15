from db import db
from flask import jsonify
from flask_sqlalchemy import BaseQuery
from flask_paginate import Pagination

class CommentsModel(db.Model):

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    comment = db.Column(db.String(200))
    comment_date = db.Column(db.DateTime)

    def __init__(self, post_id, user_id, comment, comment_date):
        self.post_id = post_id
        self.user_id = user_id
        self.comment = comment
        self.comment_date = comment_date

    @classmethod
    def find_by_post_id(cls, post_id):
        all_comments = cls.query.filter_by(post_id=post_id).order_by(CommentsModel.comment_date.asc())
        return all_comments

    @classmethod
    def find_by_comment_id(cls, comment_id):
        return cls.query.filter_by(comment_id=comment_id).first()
     
    def json(self):
        return {'comment_id' : self.comment_id, \
                'post_id' : self.post_id,\
                'user_id': self.user_id,\
                'comment' : self.comment
                #,\
                #'comment_date' : self.comment_date
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

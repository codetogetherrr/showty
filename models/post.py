from db import db


class PostModel(db.Model):

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer,primary_key=True)
    image_id = db.Column(db.String(200), nullable=False)
    image_width = db.Column(db.Integer, nullable=False)
    image_height = db.Column(db.Integer, nullable=False)
    login = db.Column(db.String(80))
    description = db.Column(db.String(80))
    date = db.Column(db.DateTime)

    @classmethod
    def get_paginated_posts(cls, login, page):
        user_list = cls.query.filter_by(login=login).order_by(PostModel.date.desc()).paginate(page=page, per_page=9, error_out=False)
        return user_list

    @classmethod
    def find_by_post_id(cls, post_id):

        return cls.query.filter_by(post_id=post_id).first()

    @classmethod
    def get_last_post(cls, login):
        login_user_post = cls.query.filter_by(login=login).order_by(PostModel.date.desc()).first()
        return login_user_post
    
    @classmethod
    def count_posts(cls, login):
        count_post = cls.query.filter_by(login=login).count()
        return count_post

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

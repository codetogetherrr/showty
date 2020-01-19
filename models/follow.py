from db import db


class FollowModel(db.Model):

    __tablename__ = 'follows'

    follow_id = db.Column(db.Integer,primary_key=True)
    follower_login = db.Column(db.String(80), nullable=False)
    followee_login = db.Column(db.String(80), nullable=False)

        
    @classmethod
    def find_followers_of_user(cls, user_login):
        followers = cls.query.filter_by(followee_login=user_login)
        return followers
        
    @classmethod
    def find_who_user_follows(cls, user_login):
        followees = cls.query.filter_by(follower_login=user_login)
        return followees

    @classmethod
    def count_followers_of_user(cls, user_login):
        no_of_followers = cls.query.filter_by(followee_login=user_login).count()
        return no_of_followers

    @classmethod
    def count_followees_user_follows(cls, user_login):
        no_of_followees = cls.query.filter_by(follower_login=user_login).count()
        return no_of_followees
    
    @classmethod
    def find_specific_follow(cls, follower_login, followee_login):
        follow = cls.query.filter_by(follower_login=follower_login, followee_login=followee_login).first()
        return follow

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

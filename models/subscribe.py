from db import db


class SubscribeModel(db.Model):

    __tablename__ = 'subscriptions'

    subscription_id = db.Column(db.Integer,primary_key=True)
    subscriber = db.Column(db.String(80), nullable=False)
    hashtag = db.Column(db.String(80), nullable=False)

    @classmethod
    def count_subscribers(cls, hashtag):
        no_of_subscribers = cls.query.filter_by(hashtag=hashtag).count()
        return no_of_subscribers

    @classmethod
    def find_by_hashtag(cls, hashtag):
        return cls.query.filter_by(hashtag=hashtag).first()

    @classmethod
    def find_specific_subscription(cls, subscriber, hashtag):
        subscription = cls.query.filter_by(subscriber=subscriber, hashtag=hashtag).first()
        return subscription

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
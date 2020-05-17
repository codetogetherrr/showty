from db import db
from sqlalchemy import and_, or_

class MessageModel(db.Model):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(640), nullable=False)
    createdAt = db.Column(db.String(80), nullable=False)
    updatedAt = db.Column(db.String(80), nullable=False)


    @classmethod
    def find_by_pair(cls, loginA, loginB):
        messages = cls.query.filter_by(or_(and_(sender=loginA, receiver=loginB), and_(sender=loginB, receiver=loginA))).order_by(MessageModel.createdAt.asc())
        return messages

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
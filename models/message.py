from db import db
from sqlalchemy import and_, or_, func, case

class MessageModel(db.Model):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(640), nullable=False)
    sentAt = db.Column(db.String(80), nullable=False)



    @classmethod
    def find_by_pair(cls, loginA, loginB):
        messages = cls.query.filter(or_(and_(cls.sender == loginA, cls.receiver == loginB), and_(cls.sender == loginB, cls.receiver == loginA))).order_by(MessageModel.sentAt.desc())
        return messages

    @classmethod
    def find_conversation_addressees(cls, login):
        #query1 = cls.query.with_entities(cls.receiver, cls.sentAt).filter_by(sender=login)
        #query2 = cls.query.with_entities(cls.sender, cls.sentAt).filter_by(receiver=login)

        query_base = cls.query(cls.receiver).with_entities(case([cls.receiver == login, cls.sender], cls.receiver), func.max(cls.sentAt)).filter_by(or_(receiver=login, sender=login)).group_by(
            cls.receiver).order_by(func.max(cls.sentAt).desc()).all()

        #addressees = query1.union(query2)

        return query_base

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
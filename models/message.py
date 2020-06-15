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
        messages = cls.query.filter(or_(and_(cls.sender == loginA, cls.receiver == loginB), and_(cls.sender == loginB, cls.receiver == loginA))).order_by(MessageModel.sentAt.asc())
        return messages

    @classmethod
    def get_latest_for_pair(cls, loginA, loginB):
        message = cls.query.filter(or_(and_(cls.sender == loginA, cls.receiver == loginB),
                                        and_(cls.sender == loginB, cls.receiver == loginA))).order_by(
            MessageModel.sentAt.desc()).first()
        return message


    @classmethod
    def find_conversation_addressees(cls, login):

        query_base = cls.query.filter(or_(cls.receiver==login, cls.sender==login)).with_entities(case([(cls.receiver == login, cls.sender)], else_ = cls.receiver).label("receiver"), func.max(cls.sentAt)).group_by(case([(cls.receiver == login, cls.sender)], else_ = cls.receiver)).order_by(func.max(cls.sentAt).desc()).all()

        return query_base

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

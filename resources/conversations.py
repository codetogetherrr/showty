from flask_restful import Resource
from models.message import MessageModel
from schemas.message import MessageSchema


message_schema = MessageSchema()


class Conversations(Resource):
    def get(self, login):
        return {'conversation_addressees': [x.receiver for x in MessageModel.find_conversation_addressees(login)]}
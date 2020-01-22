
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.hashtag import HashtagModel
from models.user import UserModel
from schemas.hashtag import HashtagSchema


hashtag_schema = HashtagSchema()


class Hashtags(Resource):

    @jwt_required
    def get(self, hashtag):

        login = get_jwt_identity()
        user = UserModel.find_by_username(login)
        if user:
            return {'items': [hashtag_schema.dump(x) for x in HashtagModel.get_items_with_hashtag(hashtag)]}

        else:
            return {"message": "User not found" }, 404
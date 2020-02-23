
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.hashtag import HashtagModel
from models.user import UserModel
from schemas.hashtag import HashtagSchema


hashtag_schema = HashtagSchema()


class Hashtags(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('hashtag', required=True, type=str, help="You have to provide hashtag")
    parser.add_argument('page', required=True, type=int, help="You have to provide page of posts with hashtag")

    @jwt_required
    def post(self):

        login = get_jwt_identity()
        user = UserModel.find_by_username(login)
        args = self.parser.parse_args()
        if user:
            return {'items': [hashtag_schema.dump(x) for x in HashtagModel.get_paginated_posts_for_hashtag(args['hashtag'], args['page'])]}

        else:
            return {"message": "User not found" }, 404
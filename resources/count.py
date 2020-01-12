
from flask_restful import Resource, reqparse
from models.post import PostModel
from flask_jwt_extended import jwt_required, get_jwt_identity


class Count(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('login', type=str, required=True, help="This field cannot be left blank!")

    @jwt_required
    def post(self):
        data = Count.parser.parse_args()
        #login = get_jwt_identity()
        posts_user=PostModel.count_post_login(data['login'])
        return {'post_count': posts_user}

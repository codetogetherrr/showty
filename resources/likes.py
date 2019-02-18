from flask_restful import Resource, reqparse
from models.comments import CommentsModel
from models.post import PostModel
from models.user import UserModel
from models.likes import LikesModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, json
from sqlalchemy.sql import func

class Likes(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('post_id', type=int, required=True, help="This field cannot be left blank!")
    
    @jwt_required
    def post(self):
        data = Likes.parser.parse_args()
        user_login = get_jwt_identity()
        user_id=UserModel.find_by_username(user_login).login
        
        like=LikesModel(data['post_id'], user_id,)
        already_like=LikesModel.find_by_user_id(user_id, data['post_id'])
        
        if like.user_id == already_like.user_id and like.post_id == already_like.post_id:
            already_like.delete_from_db()
            return {'message': 'unliked'}, 200
        else:
            like.save_to_db()
            return {"message": "liked"}, 201


        
class Likes_All(Resource):
 
    parser = reqparse.RequestParser()
    parser.add_argument('post_id', type=int, required=True, help="This field cannot be left blank!")
    
    #@jwt_required
    def post(self):
        data = Likes_All.parser.parse_args()
     
        #likes_count = LikesModel.count_likes_post_id(data['post_id']).sum(status)
        return {'likes': [x["user_id"].json() for x in LikesModel.find_by_post_id(data['post_id'])]}
    

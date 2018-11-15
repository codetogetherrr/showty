from flask_restful import Resource, reqparse
from models.comments import CommentsModel
from models.post import PostModel
from models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, json
from sqlalchemy.sql import func

class Comments(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('comment', type=str, required=False, help="This field cannot be left blank!")
    parser.add_argument('post_id', type=int, required=False, help="This field cannot be left blank!")
    parser.add_argument('comment_id', type=str, required=False, help="This field cannot be left blank!")
    
    @jwt_required
    def post(self):
        data = Comments.parser.parse_args()
        user_login = get_jwt_identity()
        date =func.now()
        user_id=UserModel.find_by_username(user_login).id

        comment_data=CommentsModel(data['post_id'],\
                        user_id,\
                        data['comment'],\
                        date)
        comment_data.save_to_db()
        return {"message": "Comment added successfully."}, 201

    @jwt_required
    def put(self):
        data = Comments.parser.parse_args()
        comment_updated=CommentsModel.find_by_comment_id(data['comment_id'])
        user_login = get_jwt_identity()
        user_id=UserModel.find_by_username(user_login).id
        current_time=func.now()

        if comment_updated.user_id == user_id:
            for key, value in data.items():
                if data[key] is not None:
                    setattr(comment_updated, key, value)
                    comment_updated.save_to_db()
            return {"message": "Comment updated successfully."}, 200
        else:
            return {'message':'It is not a comment of user logged in.'}, 404

    @jwt_required
    def delete(self):
        data = Comments.parser.parse_args()
        comment_deleted=CommentsModel.find_by_comment_id(data['comment_id'])
        user_login = get_jwt_identity()
        user=UserModel.find_by_username(user_login).id
        if comment_deleted.user_id == user:
            comment_deleted.delete_from_db()
            return {'message': 'Comment deleted'}, 200
        else:
            return {'message':'It is not a post of user logged in.'}, 404
        
class Comments_All(Resource):
 
    parser = reqparse.RequestParser()
    parser.add_argument('post_id', type=int, required=True, help="This field cannot be left blank!")
    
    @jwt_required
    def post(self):
        data = Comments_All.parser.parse_args()     
        return {'all_comments_post_id': [x.json() for x in CommentsModel.find_by_post_id(data['post_id'])]}
        #comments = CommentsModel.find_by_post_id(data['post_id'])
        #return comments.json()

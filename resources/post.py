from flask_restful import Resource, reqparse
from models.post import PostModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, json
from sqlalchemy.sql import func

class AllPostsUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('page', type=int, required=True, help="This field cannot be left blank!")
    #parser.add_argument('login', type=str, required=True, help="This field cannot be left blank!")

    @jwt_required
    def post(self):
        login = get_jwt_identity()
        data = AllPostsUser.parser.parse_args()
        return {'posts_user': [x.json() for x in PostModel.find_by_username(login, data['page']).items]}
    
    @jwt_required
    def get(self):
        login = get_jwt_identity()
        last_post=PostModel.find_last_post_login_user(login)
        return last_post.json()
    
class Posts(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('image_id', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('image_width', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('image_height', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('description', type=str, required=False, help="Optional")

    @jwt_required
    def post(self):
        data = Posts.parser.parse_args()
        user_login = get_jwt_identity()
        current_time=func.now()

        post=PostModel(data['image_id'],\
                        data['image_width'],\
                        data['image_height'],\
                        user_login,\
                        data['description'],\
                        current_time
                      )
        post.save_to_db()
        return {"message": "Post added successfully."}, 201

    @jwt_required
    def put(self, post_id):
        post_updated=PostModel.find_by_post_id(post_id)
        data = Posts.parser.parse_args()
        current_time=func.now()

        if post_updated.login == get_jwt_identity():
            for key, value in data.items():
                if data[key] is not None:
                    setattr(post_updated, key, value)
                    post_updated.save_to_db()
            return {"message": "Post updated successfully."}, 200
        else:
            return {'message':'It is not a post of user logged in.'}, 404

    @jwt_required
    def delete(self,post_id):
        post_delete=PostModel.find_by_post_id(post_id)
        if post_delete.login == get_jwt_identity():
            post_delete.delete_from_db()
            return {'message': 'Post deleted'}, 200
        else:
            return {'message':'It is not a post of user logged in.'}, 404


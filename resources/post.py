from flask_restful import Resource
from flask import request
from models.post import PostModel
from schemas.post import PostSchema, PostUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.sql import func
from marshmallow import ValidationError

post_schema = PostSchema()
post_update_schema = PostUpdateSchema()


class Post(Resource):

    @jwt_required
    def get(self):
        login = get_jwt_identity()
        last_post = PostModel.find_last_post_login_user(login)
        return post_schema.dump(last_post)

    @jwt_required
    def post(self):
        user_login = get_jwt_identity()
        try:
            post = post_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        post.login = user_login
        post.date = func.now()
        post.save_to_db()
        return {"message": "Post added successfully."}, 201

    @jwt_required
    def put(self, post_id):
        post = PostModel.find_by_post_id(post_id)
        if post:

            if post.login == get_jwt_identity():
                try:
                    post_to_update = post_update_schema.load(request.get_json(), partial=True, instance=post)
                except ValidationError as err:
                    return err.messages, 400

                post_to_update.save_to_db()
                return {"message": "Post updated successfully."}, 200
        else:
            return {'message': 'It is not a post of logged in user'}, 404

    @jwt_required
    def delete(self, post_id):
        post_delete = PostModel.find_by_post_id(post_id)
        if post_delete.login == get_jwt_identity():
            post_delete.delete_from_db()
            return {'message': 'Post deleted'}, 200
        else:
            return {'message': 'It is not a post of user logged in.'}, 404


class Posts(Resource):

    @jwt_required
    def get(self, page):
        login = get_jwt_identity()
        return {'posts_user': [post_schema.dump(x) for x in PostModel.find_by_username(login, page).items]}



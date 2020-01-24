from flask_restful import Resource
from flask import request
from models.comment import CommentModel
from models.user import UserModel
from schemas.comment import CommentSchema, CommentUpdateSchema
from schemas.hashtag import HashtagSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.sql import func
from marshmallow import ValidationError

comment_schema = CommentSchema()
comment_update_schema = CommentUpdateSchema()
hashtag_schema = HashtagSchema()


class Comment(Resource):

    @jwt_required
    def post(self):

        login = get_jwt_identity()
        user = UserModel.find_by_username(login)
        if user:
            try:
                new_comment = comment_schema.load(request.get_json())
            except ValidationError as err:
                return err.messages, 400
            new_comment.login_id = user.id
            new_comment.comment_date = func.now()
            new_comment.save_to_db()
            return {"message": "Comment added successfully."}, 201
        else:
            return {"message": "User not found"}, 404



    @jwt_required
    def put(self, comment_id):

        login = get_jwt_identity()
        user = UserModel.find_by_username(login)

        if user:
            existing_comment = CommentModel.find_by_comment_id(comment_id)
            if existing_comment:
                if existing_comment.user_id == user.id:
                    try:
                        comment_to_update = comment_update_schema.load(request.get_json(), partial=True, instance=existing_comment)
                    except ValidationError as err:
                        return err.messages, 400
                    comment_to_update.save_to_db()
                    return {"message": "Comment updated successfully."}, 200
                else:
                    return {'message': 'It is not a comment of user logged in.'}, 404
        else:
            return {"message": "User not found"}, 404


    @jwt_required
    def delete(self, comment_id):

        login = get_jwt_identity()
        user = UserModel.find_by_username(login)

        if user:
            comment_to_be_deleted = CommentModel.find_by_comment_id(comment_id)
            if comment_to_be_deleted:
                if comment_to_be_deleted.user_id == user.id:
                    comment_to_be_deleted.delete_from_db()
                    return {'message': 'Comment deleted'}, 200
                else:
                    return {'message': 'It is not a comment of user logged in.'}, 404
        else:
            return {"message": "User not found"}, 404


class Comments(Resource):


    @jwt_required
    def get(self, post_id):

        return {'comments': [comment_schema.dump(x) for x in CommentModel.find_by_post_id(post_id)]}

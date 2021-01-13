from flask_restful import Resource
from flask import request
from models.subscribe import SubscribeModel
from models.user import UserModel
from models.hashtag import HashtagModel
from schemas.subscribe import SubscribeSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError


subscribe_schema = SubscribeSchema(many=True)


class Subscribe(Resource):

    @jwt_required
    def get(self, subscriber, hashtag):

        login = get_jwt_identity()
        user = UserModel.find_by_username(login)

        if user:
            user_to_check = UserModel.find_by_username(subscriber)
            if user_to_check:

                existing_subscription = SubscribeModel.find_specific_subscription(subscriber, hashtag)

                if existing_subscription:

                    return {'message': 'hashtag subscribed'}, 200
                else:

                    return {"message": "hashtag unsubscribed"}, 200
            else:
                return {"message": "User to follow not found"}, 404

        else:
            return {"message": "User not found"}, 404

    @jwt_required
    def post(self):

        login = get_jwt_identity()
        user = UserModel.find_by_username(login)

        if user:
            try:
                new_subscription = subscribe_schema.load(request.get_json(), partial=True)
            except ValidationError as err:
                return err.messages, 400
            hashtag_to_subscribe = HashtagModel.find_if_hashtag_exist(new_subscription.hashtag)
            if hashtag_to_subscribe:

                existing_subscription = SubscribeModel.find_specific_subscription(user.login, new_subscription.hashtag)

                if existing_subscription:

                    existing_subscription.delete_from_db()

                    return {'message': 'hashtag unsubscribed'}, 200
                else:
                    new_subscription.subscriber = user.login
                    new_subscription.save_to_db()
                    return {"message": "hashtag subscribed"}, 201
            else:
                return {"message": "hashtag to subscribe not found"}, 404

        else:
            return {"message": "User not found"}, 404

class Subscriptions(Resource):

    @jwt_required
    def get(self, hashtag):

        login = get_jwt_identity()
        user = UserModel.find_by_username(login)
        if user:
            no_of_subscribers = SubscribeModel.count_subscribers(hashtag)

            return {'subscribers_count': no_of_subscribers}
        else:
            return {"message": "User not found"}, 404
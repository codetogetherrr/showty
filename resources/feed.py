from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.hashtag import HashtagModel
from models.follow import  FollowModel
from models.user import UserModel
from models.post import PostModel
from models.subscribe import SubscribeModel


from schemas.post import PostSchema

post_schema = PostSchema()


class Feed(Resource):

    @jwt_required
    def get(self):

        login = get_jwt_identity()
        user = UserModel.find_by_username(login)

        if user:
            posts_of_feed = PostModel.query\
                .join(HashtagModel, PostModel.post_id == HashtagModel.post_id)\
                .join(SubscribeModel, SubscribeModel.hashtag == HashtagModel.hashtag)\
                .join(FollowModel, FollowModel.follower == SubscribeModel.subscriber)\
                .filter_by(subscriber=login)\
                .order_by(PostModel.date.desc())

            return {'posts_of_feed': [post_schema.dump(x) for x in posts_of_feed.items]}

        else:

            return {"message": "User not found"}, 404
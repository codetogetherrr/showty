import os

from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,jwt_refresh_token_required, create_refresh_token, get_jwt_identity)
from datetime import timedelta
import requests
from werkzeug.security import check_password_hash
from resources.user import UserRegister, UserProfile, UserConfirm
from models.user import UserModel
from resources.user import UsersList
from resources.post import Posts, AllPostsUser
from resources.counts import Counts
from resources.comments import Comments
from resources.comments import Comments_All
from resources.likes import Likes
from resources.likes import Likes_All

#Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLAlchemy_Track_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get('JWT_SECRET_KEY', '')
api = Api(app)

jwt = JWTManager(app)


@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({'message': 'The token has expired'}), 401

#API Endpoint Login

@app.route('/facebooklogin', methods=['POST'])
def facebooklogin():
    facebook_access_token = request.json.get('facebook_access_token', None)
    response = requests.get('https://graph.facebook.com/me?fields=id&access_token=' + facebook_access_token)
    data = response.json()
    ret = {'facebook_profile_id':data['id']}
    return jsonify(ret), 200

@app.route('/login', methods = ['POST'])
def login():
    login = request.json.get('login', None)
    password = request.json.get('password', None)
    user = UserModel.find_by_username(login)
    if user and check_password_hash(user.password, password):
        if user.activated:
            ret = {'access_token': create_access_token(identity=login,expires_delta=timedelta(seconds=120)),
                'refresh_token': create_refresh_token(identity=login)}
            return jsonify(ret), 200
        return jsonify({'message':'Account not active. Please activate via link sent to {}'.format(user.email)}), 400
    return jsonify({'message':'Login or password is not correct.'}), 404

#API Endpoint Refresh
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    ret = {'access_token': new_token}
    return jsonify(ret), 200

#API Endpoint Protected
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(login=current_user), 200

#Oher API Endpoints required Resources
api.add_resource(UserRegister, '/register')
api.add_resource(UserConfirm, '/userconfirm/<int:user_id>')
api.add_resource(UserProfile, '/users/')
api.add_resource(UsersList, '/userslist')
api.add_resource(Posts, '/posts', endpoint = 'post')
api.add_resource(Posts, '/posts/<post_id>')
api.add_resource(AllPostsUser, '/userposts')
api.add_resource(Counts, '/counts')
api.add_resource(Comments, '/comment')
api.add_resource(Comments_All, '/comments_all')
api.add_resource(Likes, '/like')
api.add_resource(Likes_All, '/likes_all')

#blablabla
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)

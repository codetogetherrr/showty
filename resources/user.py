from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request, make_response, render_template, redirect
from werkzeug.security import generate_password_hash
import requests

#Resource Register/Login Facebook
class UserFacebookRegisterLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('facebook_access_token', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        data = UserFacebookRegisterLogin.parser.parse_args()
        facebook_access_token = data['facebook_access_token']
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer' + facebook_access_token}
        payload = {'fields': 'email, name'}
        url = 'https://graph.facebook.com/me'
        response = requests.get(url, headers=headers, params=payload)
        data = response.json()
        if response.status_code == 200:
            data = response.json()
            if UserModel.find_by_username(data['email']):
                return data, 200
                #return {'access_token': create_access_token(identity=login,expires_delta=timedelta(seconds=120)),
                #'refresh_token': create_refresh_token(identity=login)}, 200
            return {'message' : 'user does not exis yet'}, 200
        elif response.status_code == 400:
            data = response.json()
            if data['error']['code'] == 190:
                return {'message': data['error']['message']}, 401

        return data, 200

#Resource Register
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('login', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('fullname', type=str, required=False, help="Optional!")
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('telephone', type=str, required=False, help="Optional")
    parser.add_argument('description',type=str,required=False,help="Optional")
    parser.add_argument('gender',type=str,required=False,help="Optional")
    parser.add_argument('image_id',type=str,required=False,help="Optional")
    parser.add_argument('image_height',type=int,required=False,help="Optional")
    parser.add_argument('image_width',type=int,required=False,help="Optional")

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['login']):
            return {"message": "User with that login already exists."}, 200
        if UserModel.find_by_email(data['email']):
            return {"message": "Email is already in use."}, 200
        user=UserModel(data['login'],\
                        generate_password_hash(data['password']),\
                        data['fullname'],\
                        data['email'],\
                        data['telephone'],\
                        data['description'],\
                        data['gender'],\
                        data['image_id'],\
                        data['image_height'],\
                        data['image_width'])
        user.save_to_db()
        user.send_conf_email()
        return {"message": "User created successfully. Activation link sent to email provided"}, 201

#Resource Users Information
class UserProfile(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('login', type=str, required=False, help="Optional!")
    parser.add_argument('fullname', type=str, required=False, help="Optional!")
    parser.add_argument('email', type=str, required=False, help="Optional")
    parser.add_argument('telephone', type=str, required=False, help="Optional")
    parser.add_argument('description',type=str,required=False,help="Optional")
    parser.add_argument('gender',type=str,required=False,help="Optional")
    parser.add_argument('image_id',type=str,required=False,help="Optional")
    parser.add_argument('image_height',type=int,required=False,help="Optional")
    parser.add_argument('image_width',type=int,required=False,help="Optional")

    @jwt_required
    def get(self):
        login = get_jwt_identity()
        user=UserModel.find_by_username(login)
        if user:
            return user.json()
        else:
            return {"message":"User not found"}, 404

    @jwt_required
    def put(self):
        login = get_jwt_identity()
        data = UserProfile.parser.parse_args()
        user=UserModel.find_by_username(login)
        if user:
            for key, value in data.items():
                if data[key] is not None:
                    setattr(user, key, value)
                    user.save_to_db()
            return {"message": "User profile updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

    @jwt_required
    def delete(self):
        login = get_jwt_identity()
        user=UserModel.find_by_username(login)
        if user:
            user.delete_from_db()
            return {"message": "User deleted"}, 200



class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id:int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.activated = True
        user.save_to_db()
        #return redirect("http://localhost:3000", code=302)
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("confirmation_page.html", email=user.email), 200, headers)


        

class UsersList(Resource):
    def get(self):
        return {'users': [x.json() for x in UserModel.query.all()]}


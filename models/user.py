import os
from db import db
from flask import request, url_for
from requests import Response, post

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    login=db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True, nullable=False)
    telephone = db.Column(db.String(80))
    description = db.Column(db.String(150))
    gender = db.Column(db.String(80))
    image_id = db.Column(db.String(80))
    image_height = db.Column(db.Integer)
    image_width = db.Column(db.Integer)
    activated = db.Column(db.Boolean, default=False)

    def __init__(self, login, password, fullname, email, telephone, description, gender, image_id, image_height,image_width):
        self.login = login
        self.password = password
        self.fullname = fullname
        self.email = email
        self.telephone = telephone
        self.description = description
        self.gender = gender
        self.image_id = image_id
        self.image_height = image_height
        self.image_width = image_width

    @classmethod
    def list_all_logins(cls):
        logins = []
        users = cls.query.all()
        for user in users:
            logins.append(user.login)
        return logins
    @classmethod
    def find_by_username(cls, login):
        return cls.query.filter_by(login=login).first()
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'login': self.login,\
                'password': self.password,\
                'fullname': self.fullname,\
                'email': self.email, \
                'description': self.description,\
                'image_id' : self.image_id,\
                'image_height' : self.image_height,\
                'image_width' : self.image_width,\
                'gender' : self.gender,\
                'telephone' : self.telephone
                }
    def send_conf_email(self) -> Response:
        link = request.url_root[0:-1] + url_for("userconfirm", user_id=self.id)

        return post(
            f"{os.environ.get('MAILGUN_BASE_URL','')}/messages",
            auth=("api", f"{os.environ.get('MAILGUN_API_KEY','')}"),
            data={"from": f"{os.environ.get('MAILGUN_EMAIL','')}",
                "to": self.email,
                "subject": "Registration confirmation",
                "text": f"Please click the link to confirm your registration: {link}",
            },
        )

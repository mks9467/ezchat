# ~\AppData\Local\Programs\Python\Python38\python.exe
# models.py
__author__ = 'Makias Chaudhary'
__version__ = '1.1'

"""Outlines the database models"""

from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time

#######################
# User Database Model #
#######################
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sender = db.relationship('Message', backref='sender', lazy='dynamic', foreign_keys='Message.sender_id')
    receiver = db.relationship('Message', backref='receiver', lazy='dynamic', foreign_keys='Message.receiver_id')

    # Sets and hashed the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks password with password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

##########################
# Message Database Model #
##########################

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.Integer, index=True, default=time)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Message: {self.body}>'

# Loads logged in user from user ID

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# ~\AppData\Local\Programs\Python\Python38\python.exe
# routes.py
__author__ = 'Makias Chaudhary'
__version__ = '1.1'

"""Main file for all subpages"""

from app import app
from flask import render_template, flash, redirect, request, url_for
from app import forms
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message
from werkzeug.urls import url_parse
from app import db
from time import time
from sqlalchemy import or_

###########
# Routes! #
###########

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')                   # Returns home html page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:                                    # Checks if user already logged in
        return redirect(url_for('index'))
    form = forms.Login()                                                 # Creates form object for login
    if form.validate_on_submit():                                        # When the form is submitted and validated
        user = User.query.filter_by(username=form.username.data).first() # Checks for username in database
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')                        # Makes notification of invalid credentials
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')                      ######################################################
        if not next_page or url_parse(next_page).netloc != '':    # Determines if next argument is in url for redirect #
            next_page = '/index'                                  ######################################################
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return render_template('index.html', title='Home')
    form = forms.Signup()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data) # Creates user object
        user.set_password(form.password.data)                           # Sets and hashes the password
        db.session.add(user)
        db.session.commit()                                             # Adds user to database
        flash('You have successfully signed up!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    form = forms.SearchUser()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.search.data) # Checks if username is valid
        if user is not None:
            return redirect('/chat/' + form.search.data)
        flash('Invalid username check your spelling')
    return render_template('chat.html', title='Chat', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

##########################
# Private messaging page #
##########################
@app.route('/chat/<username>', methods=['GET', 'POST'])
@login_required
def chat_user(username):
    if username == current_user.username:
        flash('You cannot chat with yourself')
        return redirect(url_for('index'))
    form = forms.SendMessage()
    user = User.query.filter_by(username=username).first_or_404() # Finds user object with same username
    title = 'Chatting with ' + user.username
    if form.validate_on_submit():
        # Creates message object
        message = Message(body=form.body.data, timestamp=int(time()), sender_id=current_user.id, receiver_id=user.id)
        db.session.add(message)
        db.session.commit()
        flash('Message Sent!')
        return redirect('/chat/' + username)
    messages = Message.query.filter(or_(Message.sender_id == user.id, Message.sender_id == current_user.id))\
        .filter(or_(Message.receiver_id == current_user.id, Message.receiver_id == user.id)).all()              # Displays all message history
    return render_template('chat_user.html', user=user, messages=messages, form=form, title=title)

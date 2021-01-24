# ~\AppData\Local\Programs\Python\Python38\python.exe
# config.py
__author__ = 'Makias Chaudhary'
__version__ = '1.1'

"""Creates environment variables for later usage"""

import os

basedir = os.path.abspath(os.path.dirname(__file__)) # Gets current folder

class Config(object):
    # Creates environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-an-example-password'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# ~\AppData\Local\Programs\Python\Python38\python.exe
# __init__.py
__author__ = 'Makias Chaudhary'
__version__ = '1.1'

"""Main configuration file for flask and flask plugins"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

###########################
# Main configuration file #
###########################

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

from app import routes, models

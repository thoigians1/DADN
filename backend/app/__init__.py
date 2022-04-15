# Import flask
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import Login manager
from flask_login import LoginManager

# Import Flask_Migrate
from flask_migrate import Migrate

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Define Flask_login's Login Manager
login_manager = LoginManager(app)

# Define Flask_Migrate
migrate = Migrate(app, db)

# Homepage
@app.route("/")
def home():
    return '<h1>Hello World</h1>'

from .model import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Import a module / component using its blueprint handler variable
from app.api import api
from app.auth import auth

# Register blueprint(s)
app.register_blueprint(api)
app.register_blueprint(auth)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .model import *

auth = Blueprint("auth",__name__, url_prefix='/ ')


@auth.route("/register", methods=["POST"])
def register_account():
    form = request.form
    email = form.get('email')
    name = form.get('name')
    pw = form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        return {'error' : 406, 'message' : 'Your mail have already been registered.'}

    new_user = User(
        email=email,
        name=name,
        pw_hash=generate_password_hash(pw, method='sha256')
    )
    db.session.add(new_user)
    db.session.commit()
    return 'User created'


@auth.route("/login", methods=["POST"])
def login():
    form = request.form
    email = form.get('email')
    pw = form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user and not check_password_hash(user.pw_hash, pw):
        return {'error' : 401, 'message' : 'Your email or password are incorrect. Please check again.'}
    
    login_user(user, remember=True)
    return 'Login successgul'

@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return 'Logout successful'
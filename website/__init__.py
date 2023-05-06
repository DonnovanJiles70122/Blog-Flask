from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "notagoodsecret"
    # tell flask where database is and initialize the DB with the flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    from .models import User, Post, Comment, Like

    create_DB(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # this function allows us to access info related to the user from the DB
    # given the id of a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_DB(app):
    # check is path exist and if it doesnt we create it and make the DB file for us
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database')

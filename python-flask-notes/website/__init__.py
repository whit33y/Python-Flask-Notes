from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


#database
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thissecretisweak'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth 

    app.register_blueprint(views, url_prefidx='/')
    app.register_blueprint(auth, url_prefidx='/')

    from .models import User, Note #import modeli

    create_database(app)

    login_menager = LoginManager()
    login_menager.login_view = 'auth.login'
    login_menager.init_app(app)

    @login_menager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    return app

#tworzenie db jezeli jej nie ma
def create_database(app):
    if not path.exists('website/ '+ DB_NAME):
        db.create_all(app=app)
        print('Created Database')

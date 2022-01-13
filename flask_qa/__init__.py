from flask import Flask 
from flask_recaptcha import ReCaptcha # Import ReCaptcha object

from flask_qa import variables

from .commands import create_tables
from .extensions import db, login_manager
from .models import User
from .routes.auth import auth
from .routes.main import main

a = 5

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    #Captcha
    app.config['RECAPTCHA_SITE_KEY'] = '6LfZxwQeAAAAACTqQxzUtn1TivDQih5ercrfuH-7' # <-- Add your site key
    app.config['RECAPTCHA_SECRET_KEY'] = '6LfZxwQeAAAAAODw2VBJ1zIxAtj8qWSCX3KFm8aX' # <-- Add your secret key

    #global recaptcha
    variables.recaptcha = ReCaptcha(app) # Create a ReCaptcha object by passing in 'app' as parameter

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    app.cli.add_command(create_tables)

    return app
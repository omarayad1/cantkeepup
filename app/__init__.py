import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from app.models import command, user, group

from app.users.views import users_blueprint
from app.home.views import home_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)

from app.models import User

login_manager.login_view = "users.login"
@login_manager.user_loader
def load_user(user_id):
	return User.query.filter(User.id == int(user_id)).first()

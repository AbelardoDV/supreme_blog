from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)


from app import routes, models, errors

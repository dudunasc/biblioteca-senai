from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from typing import Final

DB_CONNECTION: Final[str] = 'mysql+pymysql'
DB_USER:       Final[str] = 'root'
DB_PASSWORD:   Final[str] = '123'
DB_HOST:       Final[str] = 'localhost'
DB_PORT:       Final[str] = '3306'
DB_NAME:       Final[str] = 'biblioteca_senai'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"{DB_CONNECTION}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'biblioteca-senai-secret-key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)

login_manager.login_view = 'index'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

bcrypt = Bcrypt(app)

from app.routes import *
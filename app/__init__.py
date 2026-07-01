from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from typing import Final

DB_CONNECTION: Final[str] = 'mysql+pymysql'
DB_USER:       Final[str] = 'root'
DB_PASSWORD:   Final[str] = ''
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
from app.models import Usuario
from app.models import Livro
from app.models import Categoria
from app.models import Emprestimo
from app.models import Solicitacao

with app.app_context():

    categorias_padrao = [
        ("Romance", "Livros de romance e literatura"),
        ("Terror", "Livros de terror e suspense"),
        ("Autoajuda", "Livros de desenvolvimento pessoal"),
        ("Programação", "Livros sobre desenvolvimento de software"),
        ("Banco de Dados", "Livros sobre SQL, MySQL e modelagem"),
        ("Redes", "Livros sobre redes de computadores"),
        ("Administração", "Livros sobre gestão e negócios"),
        ("Matemática", "Livros de matemática e raciocínio lógico"),
        ("História", "Livros de história geral"),
        ("Outros", "Categoria geral para livros diversos")
    ]

    for nome, descricao in categorias_padrao:

        categoria_existente = Categoria.query.filter_by(
            nome=nome
        ).first()

        if not categoria_existente:

            categoria = Categoria(
                nome=nome,
                descricao=descricao
            )

            db.session.add(categoria)

    db.session.commit()
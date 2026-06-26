from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    IntegerField,
    SelectField,
    TextAreaField,
    SubmitField,
    DateField
)

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    NumberRange
)

from app.models import (
    Usuario,
    Livro
)

from app import db, bcrypt

#LOGIN
class LoginForm(FlaskForm):

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    senha = PasswordField(
        'Senha',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Entrar')

    def login(self):

        user = Usuario.query.filter_by(
            email=self.email.data
        ).first()

        if user and bcrypt.check_password_hash(
            user.senha,
            self.senha.data
        ):
            return user

        return None


#USUÁRIO
class UsuarioForm(FlaskForm):

    nome = StringField(
        'Nome',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    senha = PasswordField(
        'Senha',
        validators=[
            DataRequired()
        ]
    )

    perfil = SelectField(
        'Perfil',
        choices=[
            ('ADMIN', 'Administrador'),
            ('PROFESSOR', 'Professor'),
            ('ALUNO', 'Aluno')
        ]
    )

    submit = SubmitField('Salvar')

    def saveUser(self):

        user = Usuario(
            nome=self.nome.data,
            email=self.email.data,
            senha=bcrypt.generate_password_hash(
                self.senha.data
            ).decode('utf-8'),
            perfil=self.perfil.data
        )

        db.session.add(user)
        db.session.commit()

        return user


#LIVRO
class LivroForm(FlaskForm):

    isbn = StringField(
        'ISBN',
        validators=[
            DataRequired()
        ]
    )

    titulo = StringField(
        'Título',
        validators=[
            DataRequired()
        ]
    )

    autor = StringField(
        'Autor',
        validators=[
            DataRequired()
        ]
    )

    categoria = StringField(
        'Categoria',
        validators=[
            DataRequired()
        ]
    )

    editora = StringField(
        'Editora',
        validators=[
            DataRequired()
        ]
    )

    ano = IntegerField('Ano')

    quantidade_total = IntegerField(
        'Quantidade Total',
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    quantidade_disponivel = IntegerField(
        'Quantidade Disponível',
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    submit = SubmitField('Salvar')

    def saveBook(self):

        livro = Livro(
            isbn=self.isbn.data,
            titulo=self.titulo.data,
            autor=self.autor.data,
            categoria=self.categoria.data,
            editora=self.editora.data,
            ano=self.ano.data,
            quantidade_total=self.quantidade_total.data,
            quantidade_disponivel=self.quantidade_disponivel.data
        )

        db.session.add(livro)
        db.session.commit()

        return livro


#EMPRÉSTIMO
class EmprestimoForm(FlaskForm):

    usuario_id = SelectField(
        'Usuário',
        coerce=int,
        validators=[DataRequired()]
    )

    livro_id = SelectField(
        'Livro',
        coerce=int,
        validators=[DataRequired()]
    )

    submit = SubmitField(
        'Realizar Empréstimo'
    )


#SOLICITAÇÃO
class SolicitacaoForm(FlaskForm):

    titulo_livro = StringField(
        'Título do Livro',
        validators=[
            DataRequired()
        ]
    )

    autor = StringField(
        'Autor'
    )

    observacao = TextAreaField(
        'Observação'
    )

    submit = SubmitField(
        'Enviar Solicitação'
    )
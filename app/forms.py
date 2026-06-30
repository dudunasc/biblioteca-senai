from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import (
    StringField,
    PasswordField,
    IntegerField,
    SelectField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    NumberRange
)

from app.models import (
    Usuario,
    Livro,
    Categoria
)

from app import db, bcrypt


# LOGIN
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


# USUÁRIO
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

    cpf = StringField(
        'CPF',
        validators=[
            DataRequired(),
            Length(min=14, max=14)
        ]
    )

    telefone = StringField(
        'Telefone',
        validators=[
            DataRequired(),
            Length(min=14, max=15)
        ]
    )

    matricula = StringField(
        'Matrícula',
        validators=[
            DataRequired(),
            Length(max=20)
        ]
    )

    perfil = SelectField(
        'Perfil',
        choices=[
            ('ADMIN', 'Administrador'),
            ('PROFESSOR', 'Professor'),
            ('ALUNO', 'Aluno')
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Salvar')

    def saveUser(self):

        user = Usuario(
            nome=self.nome.data,
            email=self.email.data,
            cpf=self.cpf.data,
            telefone=self.telefone.data,
            matricula=self.matricula.data,
            senha=bcrypt.generate_password_hash(
                self.matricula.data
            ).decode('utf-8'),
            perfil=self.perfil.data,
            primeiro_acesso=True
        )

        db.session.add(user)
        db.session.commit()

        return user


# CATEGORIA
class CategoriaForm(FlaskForm):

    nome = StringField(
        'Nome da categoria',
        validators=[
            DataRequired(),
            Length(max=80)
        ]
    )

    descricao = TextAreaField(
        'Descrição',
        validators=[
            Length(max=200)
        ]
    )

    submit = SubmitField('Salvar')


# LIVRO
class LivroForm(FlaskForm):

    isbn = StringField(
        'ISBN',
        validators=[
            DataRequired(),
            Length(max=20)
        ]
    )

    titulo = StringField(
        'Título',
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    autor = StringField(
        'Autor',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )

    categoria = SelectField(
        'Categoria',
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    editora = StringField(
        'Editora',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )

    ano = IntegerField(
        'Ano'
    )

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

    resumo = TextAreaField(
        'Resumo'
    )

    imagem = FileField(
        'Capa do Livro',
        validators=[
            FileAllowed(
                ['jpg', 'jpeg', 'png'],
                'Apenas imagens JPG, JPEG ou PNG.'
            )
        ]
    )

    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(LivroForm, self).__init__(*args, **kwargs)

        self.categoria.choices = [
            (categoria.id, categoria.nome)
            for categoria in Categoria.query.order_by(Categoria.nome).all()
        ]

    def saveBook(self):

        livro = Livro(
            isbn=self.isbn.data,
            titulo=self.titulo.data,
            autor=self.autor.data,
            categoria_id=self.categoria.data,
            editora=self.editora.data,
            ano=self.ano.data,
            quantidade_total=self.quantidade_total.data,
            quantidade_disponivel=self.quantidade_disponivel.data,
            resumo=self.resumo.data
        )

        db.session.add(livro)
        db.session.commit()

        return livro


# EMPRÉSTIMO
class EmprestimoForm(FlaskForm):

    usuario_id = SelectField(
        'Usuário',
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    livro_id = SelectField(
        'Livro',
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        'Realizar Empréstimo'
    )


# SOLICITAÇÃO
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
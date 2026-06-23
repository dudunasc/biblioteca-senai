from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class LivroForm(FlaskForm):
    isbn = StringField('ISBN', validators=[
        DataRequired(message='ISBN é obrigatório'),
        Length(min=10, max=20, message='ISBN deve ter entre 10 e 20 caracteres')
    ])
    titulo = StringField('Título', validators=[
        DataRequired(message='Título é obrigatório'),
        Length(min=3, max=100, message='Título deve ter entre 3 e 100 caracteres')
    ])
    autor = StringField('Autor', validators=[
        DataRequired(message='Autor é obrigatório'),
        Length(min=3, max=50, message='Autor deve ter entre 3 e 50 caracteres')
    ])
    categoria = StringField('Categoria', validators=[
        DataRequired(message='Categoria é obrigatória'),
        Length(min=3, max=50, message='Categoria deve ter entre 3 e 50 caracteres')
    ])
    editora = StringField('Editora', validators=[
        DataRequired(message='Editora é obrigatória'),
        Length(min=3, max=50, message='Editora deve ter entre 3 e 50 caracteres')
    ])
    ano = IntegerField('Ano de Publicação', validators=[Optional()])
    quantidade_total = IntegerField('Quantidade Total', validators=[
        DataRequired(message='Quantidade total é obrigatória')
    ])
    submit = SubmitField('Cadastrar Livro')


class EmpretimoForm(FlaskForm):
    usuario_id = SelectField('Usuário', coerce=int, validators=[
        DataRequired(message='Selecione um usuário')
    ])
    livro_id = SelectField('Livro', coerce=int, validators=[
        DataRequired(message='Selecione um livro')
    ])
    submit = SubmitField('Registrar Empréstimo')


class SolicitacaoForm(FlaskForm):
    titulo_livro = StringField('Título do Livro', validators=[
        DataRequired(message='Título é obrigatório'),
        Length(min=3, max=100, message='Título deve ter entre 3 e 100 caracteres')
    ])
    autor = StringField('Autor', validators=[
        Optional(),
        Length(max=50, message='Autor deve ter no máximo 50 caracteres')
    ])
    observacao = TextAreaField('Observação', validators=[
        Optional(),
        Length(max=500, message='Observação deve ter no máximo 500 caracteres')
    ])
    submit = SubmitField('Solicitar Livro')


class UsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=50, message='Nome deve ter entre 3 e 50 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = StringField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Senha deve ter no mínimo 6 caracteres')
    ])
    perfil = SelectField('Perfil', choices=[
        ('Aluno', 'Aluno'),
        ('Professor', 'Professor'),
        ('Administrador', 'Administrador')
    ], validators=[DataRequired(message='Selecione um perfil')])
    submit = SubmitField('Cadastrar Usuário')

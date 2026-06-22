from app            import db, login_manager
from datetime       import datetime
from flask_login    import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(50), nullable=False, unique=True)
    senha      = db.Column(db.String(300), nullable=False)
    perfil     = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Livro(db.Model):
    id                     = db.Column(db.Integer, primary_key=True)
    isbn                   = db.Column(db.String(20), nullable=False, unique=True)
    titulo                 = db.Column(db.String(100), nullable=False)
    autor                  = db.Column(db.String(50), nullable=False)
    categoria              = db.Column(db.String(50), nullable=False)
    editora                = db.Column(db.String(50), nullable=False)
    ano                    = db.Column(db.Integer)
    quantidade_total       = db.Column(db.Integer, nullable=False)
    quantidade_disponivel  = db.Column(db.Integer, nullable=False)

    emprestimos = db.relationship(
        'Emprestimo',
        backref='livro',
        lazy=True
    )

class Emprestimo(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    data_emprestimo  = db.Column(db.Date, nullable=False)
    data_prevista    = db.Column(db.Date, nullable=False)
    data_devolucao   = db.Column(db.Date)
    status           = db.Column(db.String(20), nullable=False, default='ATIVO')
    usuario_id       = db.Column(db.Integer, db.ForeignKey('usuario.id'),
        nullable=False)
    livro_id         = db.Column(db.Integer, db.ForeignKey('livro.id'),
        nullable=False)

class Solicitacao(db.Model):
    id                = db.Column(db.Integer, primary_key=True)
    titulo_livro      = db.Column(db.String(100), nullable=False)
    autor             = db.Column(db.String(50))
    observacao        = db.Column(db.Text)
    status            = db.Column(db.String(20), nullable=False,
        default='PENDENTE')
    data_solicitacao  = db.Column(db.DateTime,
        default=datetime.utcnow)
    professor_id      = db.Column(db.Integer, db.ForeignKey('usuario.id'),
        nullable=False)
from app.models import Solicitacao
from app import db


class ControllerSolicitacao:

    @staticmethod
    def listarSolicitacoes():

        return Solicitacao.query.all()

    @staticmethod
    def salvarSolicitacao(form, professor_id):

        solicitacao = Solicitacao(
            titulo_livro=form.titulo_livro.data,
            autor=form.autor.data,
            observacao=form.observacao.data,
            professor_id=professor_id
        )

        db.session.add(solicitacao)
        db.session.commit()

        return solicitacao

    @staticmethod
    def aprovarSolicitacao(id):

        solicitacao = Solicitacao.query.get(id)

        solicitacao.status = 'APROVADA'

        db.session.commit()

    @staticmethod
    def rejeitarSolicitacao(id):

        solicitacao = Solicitacao.query.get(id)

        solicitacao.status = 'REJEITADA'

        db.session.commit()
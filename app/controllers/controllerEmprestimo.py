from app import db

from app.models import (
    Usuario,
    Livro,
    Emprestimo
)

from datetime import (
    date,
    timedelta
)


class ControllerEmprestimo:

    @staticmethod
    def calcularPrazo(usuario):

        if usuario.perfil == 'ALUNO':
            return date.today() + timedelta(days=7)

        if usuario.perfil == 'PROFESSOR':
            return date.today() + timedelta(days=15)

        return date.today() + timedelta(days=7)

    @staticmethod
    def verificarLimite(usuario):

        emprestimos = Emprestimo.query.filter_by(
            usuario_id=usuario.id,
            status='ATIVO'
        ).count()

        if usuario.perfil == 'ALUNO':
            return emprestimos < 3

        if usuario.perfil == 'PROFESSOR':
            return emprestimos < 5

        return True

    @staticmethod
    def verificarDisponibilidade(livro):

        return livro.quantidade_disponivel > 0

    @staticmethod
    def realizarEmprestimo(form):

        usuario = Usuario.query.get(form.usuario_id.data)
        livro = Livro.query.get(form.livro_id.data)

        if not usuario or not livro:
            return False

        if not ControllerEmprestimo.verificarLimite(usuario):
            return False

        if not ControllerEmprestimo.verificarDisponibilidade(livro):
            return False

        emprestimo = Emprestimo(
            usuario_id=usuario.id,
            livro_id=livro.id,
            data_emprestimo=date.today(),
            data_prevista=ControllerEmprestimo.calcularPrazo(usuario),
            status='ATIVO'
        )

        livro.quantidade_disponivel -= 1

        db.session.add(emprestimo)
        db.session.commit()

        return True

    @staticmethod
    def listarEmprestimosAtivos():

        return Emprestimo.query.filter_by(
            status='ATIVO'
        ).all()
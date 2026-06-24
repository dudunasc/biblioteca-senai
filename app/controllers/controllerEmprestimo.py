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

        return date.today()

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
    def listarEmprestimosAtivos():

        return Emprestimo.query.filter_by(
            status='ATIVO'
        ).all()
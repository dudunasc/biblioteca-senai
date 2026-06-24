from app.models import Livro


class ControllerLivro:

    @staticmethod
    def getAllBooks():
        return Livro.query.all()

    @staticmethod
    def getBookById(id):
        return Livro.query.get(id)

    @staticmethod
    def filtrarLivros(titulo='', categoria=''):

        query = Livro.query

        if titulo:
            query = query.filter(
                Livro.titulo.contains(titulo)
            )

        if categoria:
            query = query.filter(
                Livro.categoria.contains(categoria)
            )

        return query.all()

    @staticmethod
    def deleteBook(id):

        livro = Livro.query.get(id)

        if livro:
            from app import db

            db.session.delete(livro)
            db.session.commit()

            return livro.titulo

        return None
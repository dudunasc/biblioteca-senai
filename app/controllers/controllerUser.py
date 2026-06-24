from app.models import Usuario
from flask_login import current_user


class ControllerUser:

    @staticmethod
    def isLoged():
        return current_user.is_authenticated

    @staticmethod
    def checkAdminPermission():

        if not current_user.is_authenticated:
            return False

        return current_user.perfil == 'ADMIN'

    @staticmethod
    def getUserById(id):
        return Usuario.query.get(id)

    @staticmethod
    def getAllUsers():
        return Usuario.query.all()
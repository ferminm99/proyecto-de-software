from app.models.role import Role
from app.db import db

class RoleDao:

    @classmethod
    def getAll(cls):
        """Devuelve todos los roles que hay en la BD

        Returns:
            List: roles que existen en la base de datos
        """
        roles = Role.query.all()
        db.engine.dispose()
        return roles
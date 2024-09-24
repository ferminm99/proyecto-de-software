from app.models.category import Category
from app.db import db
from sqlalchemy.exc import InvalidRequestError
class CategoryDao:
    
    @classmethod
    def get(cls, id):
        """Devuelve la categoria que corresponda con el id dado

        Args:
            id (int): id del usuario en la base de datos

        Returns:
            Category: categoria de la Base de datos.
        """
        category = Category.query.get(id)
        db.engine.dispose()
        return category
    
    @classmethod
    def getAll(cls):
        return Category.query.all()
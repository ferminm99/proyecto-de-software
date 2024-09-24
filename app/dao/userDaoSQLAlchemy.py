from app.models.user import User
from app.db import db
from sqlalchemy.exc import InvalidRequestError
class UserDao:
    
    @classmethod
    def get(cls, id):
        """Devuelve un usuario

        Args:
            id (int): id del usuario en la base de datos

        Returns:
            User: Usuario en la Base de datos.
        """
        user = User.query.filter_by(id=id).first()
        db.engine.dispose()
        return user
    
    @classmethod
    def getCount(cls):
        return User.query.count()
    
    @classmethod
    def getAdminCount(cls):
        users = User.query.all()
        count = 0
        for user in users:
            if(user.isAdmin()):
                count += 1
        return count
    
    @classmethod
    def getAllByOrder(cls,  orderBy ):
        """Trae todos los usuarios de la BD ordenado
            por algun criterio especifico
        Args:
            orderBy (string): tipo de orden 

        Returns:
            List: los usuarios que hay cargados en la base de datos
        """
        users = User.query.with_entities(
            User.username, User.first_name, User.last_name, User.email, User.id).order_by(orderBy)
        db.engine.dispose()
        return users

    @classmethod
    def getAll(cls):
        """Retorna todos los usuarios 
        Returns:
            Any: una lista de usuarios
        """
        users = User.query.with_entities(
            User.username, User.first_name, User.last_name, User.email, User.active, User.approved, User.id, User.id)
        db.engine.dispose()
        return users

    @classmethod
    def getAllWithoutInactives(cls):
        """Retorna todos los usuarios activos"""

        users = User.query.with_entities(
            User.username, User.first_name, User.last_name, User.email, User.active, User.approved, User.id, User.id)
        users = users.filter_by(active=1)
        #users = users.order_by(User.id.desc)
        return users

    @classmethod
    def getAllWithoutMe(cls, id):
        """Retorna todos los usuarios excepto del que se pasa id
        Returns:
            Any: una lista de usuarios
        """
        users = User.query.with_entities(
            User.username, User.first_name, User.last_name, 
            User.email, User.active, User.id, User.id).filter(User.id != id)
        #users = users.filter(User.id == id).delete()
        db.engine.dispose()
        return users
    
    @classmethod
    def update(cls, id, roles=None, last_name=None, first_name=None, password=None, email=None, username=None, active=None, approved = None):
        """Actualiza un usuario"""
        user = db.session.query(User).filter_by(id=id).first()
        if(roles != None):
            if len(roles) > 0:
                user.roles = roles
        if(last_name != None):   
            user.last_name = last_name
        if(first_name != None):
            user.first_name = first_name
        if((password != None)):
            user.password = password
        if(email != None):
            user.email = email
        if(username != None):
            user.username = username
        if(active != None):
            user.active = active
        if(approved != None):
            user.approved = approved
        db.session.commit()
        
    @classmethod
    def insert(cls, newUser):
        """Crea un nuevo usuario en la base de datos

        Args:
            newUser (User): usuario nuevo
        """
        db.session.add(newUser)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        """Elimina un usuario de la base de datos

        Args:
            id (int): id del usuario que se quiere eliminar
        """
        User.query.filter(User.id == id).delete()
        db.session.commit()
    
    @classmethod
    def getBy(cls, criterion, value):
        criteria = {
            'email': User.query.filter_by(email=value).first(),
            'last_name': User.query.filter_by(last_name=value).first(),
            'first_name': User.query.filter_by(first_name=value).first()
        }

        return criteria.get(criterion)
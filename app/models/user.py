from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql.expression import true
from app.db import db

class User(db.Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String(30), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    active = Column(String(1), nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    roles = db.relationship('Role', secondary='users_role', lazy='subquery',
                           backref=db.backref('users', lazy='subquery'))
    approved = Column(String(1), nullable=False)

    def __init__(self, email, username, password, first_name, last_name, active, approved="1"):
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.active = active
        self.approved = approved

    def havePermission(self, permisos):

        permisos_usuario = list()
        for role in self.roles:
            permisos_usuario.extend(
                list(map(lambda permiso: permiso.name, role.permissions)))
        return (all(item in permisos_usuario for item in permisos))
    
    def isAdmin(self):
        aux = False
        for role in self.roles:
            if (role.getName() == "Administrador"):
                aux = True
        return aux

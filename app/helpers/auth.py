from flask import session, abort, render_template
from app.models.setting import Setting
from app.models.user import User
from functools import wraps
from app.dao.userDaoSQLAlchemy import UserDao


def authenticated(session):
    return session.get("user")


def isAdmin(user):
    return 'Administrador' in list(map(lambda role: role.name, user.roles))

def required_login(f):
    """Redirecciona a una pagina de error si no hay una sesion iniciada"""
    @wraps(f)
    def wrap():
        # try:
        if not authenticated(session):
            abort(401)
        else:
            return f()
        # except:
            # abort(401)
    return wrap

def have_permission(permisos):
    return session.get("user").havePermission(permisos)


def getUser(user_id):
    return UserDao.get(user_id)

def wrap_have_permission(permisos):
    """Te deja pasar si tenes permisos"""
    def wrap1(func):
        @wraps(func)
        def wrap2(*args, **kwargs):
            if (have_permission(permisos)):
                return func(*args, **kwargs)
            else:
                abort(401)
        return wrap2
    return wrap1
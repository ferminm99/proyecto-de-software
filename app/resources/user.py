from flask import redirect, render_template, request, url_for, session, abort, flash
from flask.templating import render_template_string
from flask import jsonify
#-----Helpers----#
from app.helpers.auth import required_login, wrap_have_permission
from app.helpers.validator import isValidEmail,  isValidText
import json
from datatables import ColumnDT, DataTables
#-----DAO-----#
from app.dao.userDaoSQLAlchemy import UserDao
from app.dao.roleDaoSQLAlchemy import RoleDao
from app.dao.settingDaoSQLAlchemy import SettingDao
from app.dao.encriptPassDao import encrypt, verify
#-----Models-----#
from app.models.user import User

#---se van pronto----#
from app.db import db

@required_login
@wrap_have_permission(permisos=['user_index'])
def index():
    idUsuario = session['user'].id
    settings = SettingDao.getByType("rowsCant")
    settingsOrder = SettingDao.getByType("orderBy")
    return render_template("user/index.html", activo="2", rows=settings.element, orderCriterion=settingsOrder.element, id=idUsuario)


@required_login
@wrap_have_permission(permisos=['user_new'])
def new():
    return render_template("user/new.html", roles=RoleDao.getAll(), title="Crear Usuario")


@required_login
@wrap_have_permission(permisos=['user_new'])
def create():
    body = request.form.to_dict()

    if(list(filter(lambda user: (user.email == body['email']) or (user.username == body['username']), UserDao.getAll()))):
        return "mailExistente"

    if(isValidEmail(request.form['email'])==False):
        return "emailInvalido"
    
    if(isValidText(request.form['first_name'])==False):
        return "nombreInvalido"
    
    if(isValidText(request.form['last_name'])==False):
        return "apellidoInvalido"

    roles = request.form.getlist('roles[]')

    # active se setea a mano porque si no está marcado el checkbox no se puede acceder a request.form['active']

    if 'active' not in body.keys():
        active = 0
    else:
        active = 1

    newUser = User(request.form['email'], request.form['username'], encrypt(
        request.form['password']), request.form['first_name'], request.form['last_name'], active)
    # me quedo con los roles que coinciden con el vector de roles que me llega, se pasa todo a int para no tener problemas de tipos
    for role in list(filter(lambda role: int(role.id) in map(lambda role2: int(role2), roles), RoleDao.getAll())):
        newUser.roles.append(role)

    UserDao.insert(newUser)

    return "correcto"


@required_login
@wrap_have_permission(permisos=['user_index'])
def getUsers():

    active = request.args.get("activo")
  
    users = UserDao.getAll()
    
    if (active != "2"):
        users = users.filter_by(active=active)

    columns = [
        ColumnDT(User.username),
        ColumnDT(User.first_name),
        ColumnDT(User.last_name),
        ColumnDT(User.email),
        ColumnDT(User.active),
        ColumnDT(User.approved),
        ColumnDT(User.id),
        ColumnDT(User.id)
    ]

    rowTable = DataTables(request.args.to_dict(), users, columns)

    return jsonify(rowTable.output_result())


@required_login
@wrap_have_permission(permisos=['user_destroy'])
def delete():
    idUsuario = request.args.get("idUsuario")
    idUsuarioActual = session['user'].id
    settings = SettingDao.getByType("rowsCant")
    settingsOrder = SettingDao.getByType("orderBy")
    #if(int(idUsuarioActual) == int(idUsuario)):
    #    return render_template("user/index.html", activo="2", rows=settings.element, orderCriterion=settingsOrder.element, id=idUsuarioActual,error="No se puede eliminar a tu propio usuario")
    
    UserDao.delete(idUsuario)
    
    return render_template("user/index.html", activo="2", rows=settings.element, orderCriterion=settingsOrder.element, id=idUsuarioActual)

@required_login
#@wrap_have_permission(permisos=['user_update'])
def editMyUser():

    idUsuario = session.get("user").id
    myid = session.get("user").id
    roles = RoleDao.getAll()
    user = UserDao.get(idUsuario)

    return render_template('user/update.html', myid=myid, user=user, roles=roles)

@required_login
@wrap_have_permission(permisos=['user_manage'])
def editUser():
    idUsuario = request.args.get("idUsuario")
    myid = session.get("user").id
    roles = RoleDao.getAll()
    user = UserDao.get(idUsuario)
    
    return render_template('user/update.html', myid=myid, user=user, roles=roles)

#@wrap_have_permission(permisos=['user_update'])
def updateMyUser():
    idUser = session.get("user").id
    user = UserDao.get(idUser)
    if(isValidEmail(request.form['email']) == False):
        return "wrongEmailUsername"
    if(isValidText(request.form['first_name']) == False):
        return "nombreInvalido"
    if(isValidText(request.form['last_name']) == False):
        return "apellidoInvalido"
    UserDao.update(id = idUser, last_name = request.form['last_name'], 
        first_name = request.form['first_name'], email=request.form['email'], 
        username=request.form['username'])
    return "Actualizado"

@wrap_have_permission(permisos=['user_update'])
def updateUser():
    idUser = request.form["idUsuario"]
    user = UserDao.get(idUser)
    roles = request.form.getlist('roles[]')
    if(list(filter(lambda user: (user.email == request.form['email']) or 
        (user.username == request.form['username']), UserDao.getAllWithoutMe(idUser)))):
        return "mailExistente"
    if(isValidEmail(request.form['email']) == False):
        return "emailInvalido"
    if(isValidText(request.form['first_name']) == False):
        return "nombreInvalido"
    if(isValidText(request.form['last_name']) == False):
        return "nombreInvalido"
    if len(roles) > 0:
        roles = list(filter(lambda role: int(role.id) in map(
            lambda role2: int(role2), request.form.getlist('roles[]')), RoleDao.getAll()))
    active = None        
    if 'active' not in request.form.keys():
        active = 0
    else:
        active = 1
    approved = None
    if 'approved' not in request.form.keys():
        approved = 0
    else:
        approved = 1
    if approved is None:
        UserDao.update(id = idUser, roles = roles, last_name = request.form['last_name'], 
            first_name = request.form['first_name'], email=request.form['email'], 
            username=request.form['username'], active=active, approved = 1)
    else:
        if approved == 1:
            if len(roles) > 0:
                UserDao.update(id = idUser, roles = roles, last_name = request.form['last_name'], 
                    first_name = request.form['first_name'], email=request.form['email'], 
                    username=request.form['username'], active=active, approved = approved)
            else:
                return "SinRol"
 
    return "Actualizado"

@required_login
@wrap_have_permission(permisos=['user_manage'])
def editPassword():
    myid = session.get("user").id
    user = UserDao.get(request.args.get("idUsuario"))
    return render_template('user/updatePassword.html', user=user, myid=myid)

@required_login
def editMyPassword():
    myid = session.get("user").id
    user = UserDao.get(myid)
    return render_template('user/updatePassword.html', user=user, myid=myid)

@required_login
@wrap_have_permission(permisos=['user_update'])
def updatePassword():
    idUser = request.form["idUsuario"]
    pas = request.form['newpassword']
    if ( pas == ""):
        return "campoVacio"
    pas = encrypt(pas)
    UserDao.update(id = idUser, password = pas)
    return "Actualizado"

@required_login
def updateMyPassword():
    idUser = request.form["idUsuario"]
    user = UserDao.get(idUser)
    actPas = request.form['actpassword']
    pas = request.form['newpassword']
    if(actPas == ""):
        return "campoVacio"
    if(not verify(actPas, user.password)):
        return "contrIncorrecta"
    pas = encrypt(pas)
    UserDao.update(id = idUser, password = pas)
    return "Actualizado"
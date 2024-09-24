from flask import redirect, render_template, request, url_for, session
from app.models import category
from app.models.followup import FollowUp
from app.models.category import Category
from app.models.complaint import Complaint
from app.helpers.auth import required_login, wrap_have_permission
import json
from flask import jsonify
from datatables import ColumnDT, DataTables
from app.db import db
from app.helpers.validator import isValidEmail,  isValidText
#------DAO-------#
from app.dao.settingDaoSQLAlchemy import SettingDao
from app.dao.userDaoSQLAlchemy import UserDao
from app.dao.complaintDaoSQLAlchemy import ComplaintDao 
from app.dao.categoryDaoSQLAlchemy import CategoryDao


def new():
    categories = CategoryDao.getAll()
    return render_template("complaint/new.html", categories = categories)
    

@required_login
#poner permiso indicado
@wrap_have_permission(permisos=['complaint_index'])
def index():
    idUsuario = session['user'].id
    user = session['user']
    settings = SettingDao.getByType("rowsCant")
    return render_template("complaint/index.html", state="10", rows=settings.element, user = user, id=idUsuario, title="Denuncias")

@required_login
@wrap_have_permission(permisos=['complaint_index'])
def getComplaints():

    state = request.args.get("state")
    complaint = ComplaintDao.getAllByState(state)

    columns = [
        ColumnDT(Complaint.title),
        ColumnDT(Complaint.telephone),
        ColumnDT(Complaint.email),
        ColumnDT(Complaint.created_at),
        ColumnDT(Complaint.latitude),
        ColumnDT(Complaint.length),
        ColumnDT(Complaint.id_state),
        ColumnDT(Complaint.id),
        ColumnDT(Complaint.id)
    ]
  
    rowTable = DataTables(request.args.to_dict(), complaint, columns)

    return jsonify(rowTable.output_result())


@required_login
@wrap_have_permission(permisos=['complaint_index'])
def getComplaintsOperators():

    state = request.args.get("state")
    idUsuario = session['user'].id

    complaint = ComplaintDao.getAllByStateOperator(state, idUsuario)

    columns = [
        ColumnDT(Complaint.title),
        ColumnDT(Complaint.telephone),
        ColumnDT(Complaint.email),
        ColumnDT(Complaint.created_at),
        ColumnDT(Complaint.latitude),
        ColumnDT(Complaint.length),
        ColumnDT(Complaint.id_state),
        ColumnDT(Complaint.id),
        ColumnDT(Complaint.id)
    ]
  
    rowTable = DataTables(request.args.to_dict(), complaint, columns)

    return jsonify(rowTable.output_result())


@required_login
@wrap_have_permission(permisos=['complaint_destroy'])
def delete():
    idComplaint = request.args.get("idComplaint")
    user = session['user']
    ComplaintDao.delete(idComplaint)
    settings = SettingDao.getByType("rowsCant")
    idUsuario = session['user'].id
    return render_template("complaint/index.html", state="10", user = user, rows=settings.element, id=idUsuario)

@required_login
@wrap_have_permission(permisos=['complaint_update'])
def edit():
    idUsuario = session['user'].id
    user = session['user']
    allUsers = UserDao.getAll()
    users = UserDao.getAllWithoutInactives()

    idComplaint = request.args.get("idComplaint")
    complaint = ComplaintDao.getById(idComplaint)
    followUp = ComplaintDao.getFollowUpById(complaint.id_user_assigned)
    categories = CategoryDao.getAll()


    followsUp = ComplaintDao.getFollowsUp(idComplaint)

    db.engine.dispose()

    return render_template('complaint/editComplaint.html', complaint=complaint, id=idUsuario, allUsers = allUsers,
     users = users, followUp = followUp, user = user, followsUp = followsUp, categories = categories)


@required_login
@wrap_have_permission(permisos=['complaint_update'])
def update():
    id = session['user'].id
    id_complaint = request.form["idComplaint"]
    id_user_assigned = request.form["id_user_assigned"]
    id_category = request.form["category"]
    description = request.form["description"]

    ComplaintDao.update(id_complaint, request.form['state'], id_user_assigned, description,id, id_category)
    
    return "Actualizado"

@required_login
@wrap_have_permission(permisos=['complaint_update'])
def updateOperator():
    id = session['user'].id
    id_complaint = request.form["idComplaint"]
    description = request.form["description"]
    id_category = request.form["category"]

    ComplaintDao.updateOperator(id_complaint, request.form['state'], description, id, id_category)
    
    return "Actualizado"

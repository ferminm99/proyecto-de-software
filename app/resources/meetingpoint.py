from flask import redirect, render_template, request, url_for, session
from app.models.meetingpoint import MeetingPoint
from app.helpers.auth import required_login, wrap_have_permission
import json
from flask import jsonify
from datatables import ColumnDT, DataTables
from app.db import db
from app.helpers.validator import isValidEmail,  isValidText
#------DAO-------#
from app.dao.settingDaoSQLAlchemy import SettingDao
from app.dao.meetingpointDaoSQLAlchemy import MeetingPointDao

@required_login
@wrap_have_permission(permisos=['meetingpoint_index'])
def index():
    idUsuario = session['user'].id
    settings = SettingDao.getByType("rowsCant")
    settingsOrder = SettingDao.getByType("orderByMP")
    return render_template("meetingPoints/index.html", state="2", rows=settings.element, orderCriterion=settingsOrder.element, id=idUsuario, title="Gestion Puntos de Encuentros")



def showMeetingPoints():
    settings = SettingDao.getByType("rowsCant")
    settingsOrder = SettingDao.getByType("orderByMP")
    meeting_point = MeetingPointDao.getAllPublics()
    return render_template("meetingPoints/showMeetingPoints.html", state="2", rows=settings.element, orderCriterion=settingsOrder.element, meeting_point=meeting_point)


def addMeetingPoint():
    idUsuario = session['user'].id
    settings = SettingDao.getByType("rowsCant")
    settingsOrder = SettingDao.getByType("orderByMP")
    meeting_point = MeetingPointDao.getAll()
    return render_template("meetingPoints/addMeetingPoint.html", state="2", rows=settings.element, orderCriterion=settingsOrder.element, id=idUsuario,  meeting_point=meeting_point)

def createMeetPoint():
    params = request.form.to_dict()
    coord=params['coordenadas']
    coord=coord.replace("LatLng(", "")
    coord=coord.replace(")", "")
    coord=coord.split(',') 
    new_meetpoint= MeetingPoint( params['nombre'], params['address'], params['estado'], params['telefono'], params['email'], coord[0], coord[1])
    MeetingPointDao.insert(new_meetpoint)

    return redirect(url_for("add_meetingPoint"))

@required_login
@wrap_have_permission(permisos=['meetingpoint_destroy'])
def delete():
    idMeetingPoint = request.args.get("idMeetingPoint")
    MeetingPointDao.delete(idMeetingPoint)
    idUsuario = session['user'].id
    settings = SettingDao.getByType("rowsCant")
    settingsOrder = SettingDao.getByType("orderByMP")
    return render_template("meetingPoints/index.html", state="2", rows=settings.element, orderCriterion=settingsOrder.element, id=idUsuario)

@required_login
@wrap_have_permission(permisos=['meetingpoint_index'])
def getMeetingPoints():

    state = request.args.get("state")
    meetingPoint = MeetingPointDao.getAllByState(state)

    columns = [
        ColumnDT(MeetingPoint.name),
        ColumnDT(MeetingPoint.address),
        ColumnDT(MeetingPoint.telephone),
        ColumnDT(MeetingPoint.email),
        ColumnDT(MeetingPoint.latitude),
        ColumnDT(MeetingPoint.length),
        ColumnDT(MeetingPoint.state),
        ColumnDT(MeetingPoint.id),
        ColumnDT(MeetingPoint.id)
    ]

    rowTable = DataTables(request.args.to_dict(), meetingPoint, columns)

    return jsonify(rowTable.output_result())

@required_login
@wrap_have_permission(permisos=['meetingpoint_update'])
def edit():

    idMeetingPoint = request.args.get("idMeetingPoint")
    meet_point = MeetingPointDao.getById(idMeetingPoint)
    db.engine.dispose()

    return render_template('meetingPoints/editMeetingPoint.html', meet_point=meet_point)

@required_login
@wrap_have_permission(permisos=['meetingpoint_update'])
def update():

    idMeetingPoint = request.form["idMeetingPoint"]
    meetPoint = MeetingPointDao.getById(idMeetingPoint)

    if(list(filter(lambda meetPoint: (meetPoint.email == request.form['email']) or 
        (meetPoint.name == request.form['name']), MeetingPointDao.getAllWithoutMe(id=idMeetingPoint)))):
        return "mailExistente"
    if(isValidEmail(request.form['email']) == False):
        return "emailInvalido"
    if(request.form['name'] == ""):
        return "campoVacio"
    if(request.form['telephone'] == ""):
        return "campoVacio"
    if(request.form['address'] == ""):
        return "campoVacio" 
    

    if 'state' not in request.form.keys():
        state = 0
    else:
        state = 1 

    
    MeetingPointDao.update(idMeetingPoint,request.form['name'],  request.form['address'], state, request.form['telephone'],
        request.form['email'], request.form['latitude'], request.form['length']  )
    
    return "Actualizado"
    




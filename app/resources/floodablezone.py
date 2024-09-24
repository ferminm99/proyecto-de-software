from flask import redirect, render_template, request, url_for, session, make_response
from app.models.floodablezone import FloodableZone
from app.helpers.auth import required_login, wrap_have_permission
import json
from flask import jsonify
from datatables import ColumnDT, DataTables
from app.db import db
from app.helpers.validator import isValidEmail,  isValidText
#------DAO-------#
from app.dao.settingDaoSQLAlchemy import SettingDao
from app.dao.floodablezoneDaoSQLAlchemy import FloodableZoneDao

#csv
import csv
import io


@required_login
@wrap_have_permission(permisos=['floodablezone_index'])
def index():
    idUsuario = session['user'].id
    settings = SettingDao.getByType("rowsCant")
    settingsOrder = SettingDao.getByType("orderByMP")
    # mofificacion sin consulta ajax
    floodableAreas = FloodableZoneDao.getAll()
    return render_template("floodableZone/index.html", state="10", rows=settings.element, orderCriterion=settingsOrder.element, id=idUsuario, title="Gestion Areas Inundables", floodableAreas=floodableAreas)


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")

@required_login
@wrap_have_permission(permisos=['floodablezone_import'])
def upload():
    data = None
    if request.method == "POST":
        f = request.files['file']

        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)

        for row in csv_input:
            if (row[0] != 'name'):
                if FloodableZoneDao.isRepetead(row[0]):
                    new_floodableZone = FloodableZone(row[0], row[1])
                    FloodableZoneDao.replace(new_floodableZone)
                else: 
                    new_floodableZone = FloodableZone(row[0], row[1])
                    FloodableZoneDao.insert(new_floodableZone)

        stream.seek(0)

        return redirect(url_for("floodablezone_index"))
        
    
@required_login
@wrap_have_permission(permisos=['floodablezone_index'])
def getflooadableAreas():

    state = request.args.get("state")
    floodableAreas = FloodableZoneDao.getAllByState(state)
    columns = [
        ColumnDT(FloodableZone.name),
        ColumnDT(FloodableZone.state),
        ColumnDT(FloodableZone.id),
        ColumnDT(FloodableZone.id),
        ColumnDT(FloodableZone.id)
    ]
  
    rowTable = DataTables(request.args.to_dict(), floodableAreas, columns)

    return jsonify(rowTable.output_result())

@required_login
@wrap_have_permission(permisos=['floodablezone_index'])
def checkinfo():
    idArea= request.args['zone_id']
    floodableArea = FloodableZoneDao.returnwithID(idArea)
    idUsuario = session['user'].id
    return render_template("floodableZone/zoneInfo.html", id=idUsuario, title="Informacion de zona", floodableArea=floodableArea)

@required_login
@wrap_have_permission(permisos=['floodablezone_destroy'])
def destroy():
    idArea= request.args['zone_id']
    FloodableZoneDao.delete(idArea)
    return redirect(url_for('floodablezone_index'))

@required_login
def edit():
    idArea= request.args['zone_id']
    floodableArea = FloodableZoneDao.returnwithID(idArea)
    idUsuario = session['user'].id
    return render_template("floodableZone/update.html", id=idUsuario, title="Actualizacion de zona", floodableArea=floodableArea)

@required_login
def update():
    idArea= request.form['idzone']
    color = request.form['colorpick']
    state = request.form['state']
    floodableArea = FloodableZoneDao.returnwithID(idArea)
    idUsuario = session['user'].id
    FloodableZoneDao.update(idArea, color, state)

    return "Actualizado"
    #return render_template("floodableZone/update.html", id=idUsuario, title="Actualizacion de zona", floodableArea=floodableArea)

def getAllZones():
    zonas = FloodableZoneDao.getAll()

    zonas_json=[]

    for zona in zonas:

            if (zona.state == 1):

                coordenadas = formatStringToCoordinates(zona.coordinates)
                coordenadas = coordenadas[1:]
                zonas_json.append(
                {
                    "id": zona.id,
                    "nombre": zona.name,
                    "coordenadas": coordenadas,
                    "color": zona.colour
                })
        
    message = {
        #'status': 200,
        #'message': 'OK',
        'zonas': zonas_json,
        'total': len(zonas)
    }

    resp = jsonify(message)
    resp.status_code = 200

    return resp


def getZone(id):
    zona = FloodableZoneDao.get(id)

    if not(zona):
        resp = jsonify({"message": 'Not Found'})
        resp.status_code = 401
        return resp
    else:
        coordenadas = formatStringToCoordinates(zona.coordinates)
        body =  {
                    "id": zona.id,
                    "nombre": zona.name,
                    "coordenadas":coordenadas,
                    "color": zona.colour
                }
        
        message = {
            #'status': 200,
            'message': 'OK',
            'atributos': body
        }

        resp = jsonify(message)
        resp.status_code = 200
        return resp
    
def formatStringToCoordinates(lista):
    """Esta funcion formatea el string de coordenadas que viene de la base de datos. 
    Se debe cumplir que cada coordenada mantega un formato de [ 111, 111 ], para que
    funcione el algoritmo.

    Args:
        lista (List): Las coordernadas cargadas en un string.

    Returns:
        List: Contiene el formato json en que se transformo el string
    """
    listCoord = lista.split("]")
    jsonCoord = []

    #El primero es especial.
    formatItem = listCoord[0][1:]
    splitCoord = formatItem.split(",")
    jsonCoord.append({"lat":splitCoord[0], "long":splitCoord[1]})
    
    for item in listCoord[1:]:
        formatItem = item[2:]
        if(len(formatItem) > 0):
            splitCoord = formatItem.split(",")        
        jsonCoord.append({"lat":splitCoord[0], "long":splitCoord[1]})

    return jsonCoord

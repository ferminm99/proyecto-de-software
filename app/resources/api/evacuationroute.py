from flask import jsonify, Blueprint, request
from app.dao.evacuationrouteSQLAlchemy import EvacuationRouteDao
from app.models.evacuationroute import EvacuationRoute
from app.db import db
from app.helpers.validator import isValidEmail, isValidText, isValidCoordinates, isNotXSSFormat
import json
from sqlalchemy import func
from app.dao.settingDaoSQLAlchemy import SettingDao

evacuationroute_api = Blueprint("evacuationroute", __name__, url_prefix="/recorridos-evacuacion")

# Este servicio permite obtener el listado de los recorridos de
# evacuación paginados según configuración de la plataforma.
@evacuationroute_api.get("/")
def index():
    page = int(request.args.get("page" , 1))
    per_page = int(request.args.get("per_page" , int(SettingDao.getByType("rowsCant").element)))
    if(page < 1):
        message = {"400": "page tiene que ser un entero positivo"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    if(per_page < 1):
        message = {"400": "per_page tiene que ser un entero positivo"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    count = EvacuationRouteDao.getCount()
    cant_page = count/per_page
    if(cant_page < (page-1)):
        message = {"404": "No existe la pagina solicitada"}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    evacuationroute_page = EvacuationRouteDao.getPage(page, per_page)
    evacuationroutes = [formatEvacuationroute(evacuationroute) for evacuationroute in evacuationroute_page.items]
    message = {
            "recorridos": evacuationroutes,
            "total": count,
            "pagina": page
        }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

def formatEvacuationroute(evacuationroute):
    auxdic = {
        "id": evacuationroute.id,
        "nombre": evacuationroute.name,
        "coordenadas": formatStringToCoordinates(evacuationroute.coordinates)[1:],
        "descripcion": evacuationroute.description
    }
    return auxdic

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
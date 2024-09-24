from flask import jsonify, Blueprint, request
from app.dao.meetingpointDaoSQLAlchemy import MeetingPointDao
from app.models.meetingpoint import MeetingPoint
from app.db import db
from app.helpers.validator import isValidEmail, isValidText, isValidCoordinates, isNotXSSFormat
import json
from sqlalchemy import func
from app.dao.settingDaoSQLAlchemy import SettingDao

meetingpoint_api = Blueprint("meetingpoint", __name__, url_prefix="/puntos-encuentro")

# Este servicio permite obtener el listado de los puntos de
# evacuación paginados según configuración de la plataforma.

@meetingpoint_api.get("/")
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
    count = MeetingPointDao.getCount()
    cant_page = count/per_page
    if(cant_page < (page-1)):
        message = {"404": "No existe la pagina solicitada"}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    meetingpoint_page = MeetingPointDao.getPage(page, per_page)
    meetingpoints = [formatMeetingpoint(meetingpoint) for meetingpoint in meetingpoint_page.items]
    message = {
            "puntos_encuentro": meetingpoints,
            "total": count,
            "pagina": page
        }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

def formatMeetingpoint(meetingpoint):
    auxdic = {
        "id": meetingpoint.id,
        "nombre": meetingpoint.name,
        "dirección": meetingpoint.address,
        "lat": meetingpoint.latitude,
        "long": meetingpoint.length,
        "telefono": meetingpoint.telephone,
        "email": meetingpoint.email
    }
    return auxdic
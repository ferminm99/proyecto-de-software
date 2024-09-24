from flask import jsonify, Blueprint, request
from app.dao.complaintDaoSQLAlchemy import ComplaintDao
from app.dao.evacuationrouteSQLAlchemy import EvacuationRouteDao
from app.dao.floodablezoneDaoSQLAlchemy import FloodableZoneDao
from app.dao.meetingpointDaoSQLAlchemy import MeetingPointDao
from app.dao.followupDAOSQLAlchemy import FollowUpDao
from app.dao.userDaoSQLAlchemy import UserDao
from app.db import db
from app.helpers.validator import isValidEmail, isValidText, isValidCoordinates, isNotXSSFormat
import json
from sqlalchemy import func

statistic_api = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")

@statistic_api.get("/")
def index():
    complaint_count=ComplaintDao.getCount()
    complaintwitoutfollowup_count = complaint_count - FollowUpDao.getUniqueComplaintsCount()
    evacuationroute_count=EvacuationRouteDao.getCount()
    floodablezone_count=FloodableZoneDao.getCount()
    meetingpoint_count=MeetingPointDao.getCount()
    user_count=UserDao.getCount()
    useradmin_count = UserDao.getAdminCount()
    
    message = formatMessage(complaint_count=complaint_count, 
        evacuationroute_count=evacuationroute_count, 
        floodablezone_count=floodablezone_count,
        meetingpoint_count=meetingpoint_count,
        user_count=user_count,
        useradmin_count=useradmin_count,
        complaintwitoutfollowup_count=complaintwitoutfollowup_count)
    
    resp = jsonify(message)
    resp.status_code = 200
    return resp

def formatMessage(complaint_count=None, evacuationroute_count=None, 
    floodablezone_count=None, meetingpoint_count=None, user_count=None,
    useradmin_count=None, complaintwitoutfollowup_count=None):
    message = {
        "cant. usuarios": user_count,
        "cant. administradores": useradmin_count,
        "cant. operadores": user_count - useradmin_count,
        "cant. rutas de evacuacion": evacuationroute_count,
        "cant. zonas inundables": floodablezone_count,
        "cant. puntos de encuentro": meetingpoint_count,
        "cant. denuncias": complaint_count,
        "cant. denuncias con seguimientos": complaint_count - complaintwitoutfollowup_count,
        "cant. denuncias sin seguimientos": complaintwitoutfollowup_count,
    }
    return message

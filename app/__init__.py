from os import path, environ
from flask import Flask, render_template, g, session, Blueprint
from flask_session import Session
from config import config
from app import db
from app.resources import evacuationroute, floodablezone, palette
from app.resources import user
from app.resources import meetingpoint
from app.resources import floodablezone
from app.resources import complaint 
from app.resources import auth
from app.resources import config as systemConfig
from app.helpers import handler
from app.helpers.auth import required_login
from app.helpers import auth as helper_auth
from app.helpers import initialSetting as settings
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.resources.api.complaint import complaint_api
from app.resources.api.meetingpoint import meetingpoint_api
from app.resources.api.evacuationroute import evacuationroute_api
from app.resources.api.statistic import statistic_api

# DAO Imports:
from app.dao.meetingpointDaoSQLAlchemy import MeetingPointDao
from app.dao.floodablezoneDaoSQLAlchemy import FloodableZoneDao
#Descomenta las siguientes lineas si queres activar el logging
#import logging
#logging.basicConfig()
#logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


# Python standard libraries
import os

def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    CORS(app)
    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+str(app.config['DB_USER']) + \
        ':'+str(app.config['DB_PASS'])+'@localhost/'+str(app.config['DB_NAME'])
    db = SQLAlchemy(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(isAdmin=helper_auth.isAdmin)
    app.jinja_env.globals.update(have_permission=helper_auth.have_permission)
    app.jinja_env.globals.update(colorStyles=settings.stylesPage)
    app.jinja_env.globals.update(getUser = helper_auth.getUser)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )
    # google login
    app.add_url_rule("/login", "auth_google_login", auth.login_google) 
    app.add_url_rule(
        "/login/callback", "auth_callback", auth.callback, methods=["GET"]
    )

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/get", "get_user",
                     user.getUsers, methods=["GET"])
    #Update
    app.add_url_rule("/usuarios/edit", "user_edit",
                     user.editUser, methods=["GET"])
    app.add_url_rule("/usuarios/edit_my_user", "myuser_edit",
                     user.editMyUser, methods=["GET"])
    app.add_url_rule("/usuarios/update", "user_update",
                     user.updateUser, methods=["PUT"])
    app.add_url_rule("/usuarios/update_my_user", "myuser_update",
                     user.updateMyUser, methods=["PUT"])
    app.add_url_rule("/usuarios/edit_password", "password_edit",
                     user.editPassword, methods=["GET"])
    app.add_url_rule("/usuarios/edit_mypassword", "mypassword_edit",
                     user.editMyPassword, methods=["GET"])
    app.add_url_rule("/usuarios/edit_password/update_password", "password_update",
                     user.updatePassword, methods=["PUT"])
    app.add_url_rule("/usuarios/edit_password/update_my_password", "mypassword_update",
                     user.updateMyPassword, methods=["PUT"])
    app.add_url_rule("/usuarios/destroy", "user_destroy",
                     user.delete, methods=["POST","GET"])

    # Rutas de Configuracion
    app.add_url_rule("/configuracion", "settings_index",
                     systemConfig.index, methods=["GET"])
    app.add_url_rule("/configuracion", "settings_update",
                     systemConfig.updateSettings, methods=["POST"])
    app.add_url_rule("/configuracion/paleta", "palette_update", palette.update, methods=["POST"])

    # Rutas de puntos de encuentro
    app.add_url_rule("/puntosDeEncuentro", "meetingpoint_index", meetingpoint.index)
    # app.add_url_rule("/puntosDeEncuentro", "meetingpoint_create", meetingpoint.create, methods=["POST"])
    app.add_url_rule("/puntosDeEncuentro/get", "get_meetingpoint",
                     meetingpoint.getMeetingPoints, methods=["GET"])
    app.add_url_rule("/puntosDeEncuentro/destroy", "meetingpoint_destroy",
                     meetingpoint.delete, methods=["POST","GET"])
    app.add_url_rule("/puntosDeEncuentro/edit", "meetingpoint_edit",
                     meetingpoint.edit, methods=["GET","POST"])
    app.add_url_rule("/puntosDeEncuentro/update", "meetingpoint_update",
                     meetingpoint.update, methods=["PUT"])

    app.add_url_rule("/puntosDeEncuentroMap", "show_meetingpoint", meetingpoint.showMeetingPoints)
    app.add_url_rule("/agregarPuntoDeEncuentro", "add_meetingPoint", meetingpoint.addMeetingPoint)
    app.add_url_rule("/agregarPuntoEncuentro", "meetpoint_create", meetingpoint.createMeetPoint, methods=["POST"])


    #Ruta para zonas inundables
    app.add_url_rule("/zonasinundables", "floodablezone_index", floodablezone.index)
    app.add_url_rule("/zonasinundables/get", "get_flooadableAreas",
                     floodablezone.getflooadableAreas, methods=["GET"])
    app.add_url_rule("/zonasinundables/show", "floodablezone_checkinfo", floodablezone.checkinfo)
    app.add_url_rule("/zonasinundables/destroy", "floodablezone_destroy", floodablezone.destroy)
    app.add_url_rule("/zonasinundables/edit", "floodablezone_edit", floodablezone.edit)
    app.add_url_rule("/zonasinundables/update", "floodablezone_update", floodablezone.update, methods=["POST", "PUT"])

    app.add_url_rule("/zonasinundables/import", "floodablezone_import", floodablezone.upload,  methods=["GET","POST"])


    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        """ Devolver meetpoints, floodableZones y recorridos """
        meeting_point = MeetingPointDao.getAll()
        floodableAreas = FloodableZoneDao.getAll()
        return render_template("home.html", meeting_point=meeting_point, floodableAreas=floodableAreas)

    # Rutas de las denuncias
    app.add_url_rule("/denuncias", "complaint_index", complaint.index)
    app.add_url_rule("/denuncias/get", "get_complaint",
                     complaint.getComplaints, methods=["GET"])
    app.add_url_rule("/denuncias/getOperator", "get_complaint_operator",
                     complaint.getComplaintsOperators, methods=["GET"])
    app.add_url_rule("/denuncias/new", "complaint_new",
                     complaint.new, methods=["POST","GET"])
    app.add_url_rule("/denuncias/destroy", "complaint_destroy",
                     complaint.delete, methods=["POST","GET"])
    app.add_url_rule("/denuncias/edit", "complaint_edit",
                     complaint.edit, methods=["GET","POST"])
    app.add_url_rule("/denuncias/update", "complaint_update",
                     complaint.update, methods=["PUT"])
    app.add_url_rule("/denuncias/updateOperator", "complaint_update_operator",
                     complaint.updateOperator, methods=["PUT"])
    
    #Rutas de Zonas inundables
    app.add_url_rule("/api/zonas-inundables/", " floodablezone_index", floodablezone.getAllZones, methods=["GET"])
    app.add_url_rule("/api/zonas-inundables/<id>", " floodablezone_show", floodablezone.getZone, methods=["GET"])
    
    #Rutas de Recorridos
    app.add_url_rule("/recorridos-evacuacion/new", "evacuationroute_new", evacuationroute.new, methods=["GET"])
    app.add_url_rule("/recorridos-evacuacion/create", "evacuationroute_create", evacuationroute.create, methods=["POST"])
    app.add_url_rule("/recorridos-evacuacion/index", "evacuationroute_index", evacuationroute.index, methods=["GET"])
    app.add_url_rule("/recorridos-evacuacion/getAll", "evacuationroute_getAll", evacuationroute.get_evacuationroute, methods=["GET"])
    app.add_url_rule("/recorridos-evacuacion/show", "evacuationroute_show", evacuationroute.show, methods=["GET"])
    app.add_url_rule("/recorridos-evacuacion/update", "evacuationroute_update", evacuationroute.update, methods=["PUT"])
    app.add_url_rule("/recorridos-evacuacion/route", "evacuationroute_route", evacuationroute.show_route, methods=["GET"])
    app.add_url_rule("/recorridos-evacuacion/update_route", "evacuationroute_update_route", evacuationroute.update_route, methods=["PUT"])
    app.add_url_rule("/recorridos-evacuacion/destroy", "evacuationroute_destroy", evacuationroute.delete,  methods=["POST","GET"])


    
    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(complaint_api)
    api.register_blueprint(meetingpoint_api)
    api.register_blueprint(evacuationroute_api)
    api.register_blueprint(statistic_api)

    app.register_blueprint(api)
  
    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app

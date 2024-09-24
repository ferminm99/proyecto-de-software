import pymysql

from flask import current_app
from flask import g
from flask import cli
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connection():
    if "db_conn" not in g:
        conf = current_app.config
        g.db_conn = pymysql.connect(
            host=conf["DB_HOST"],
            user=conf["DB_USER"],
            password=conf["DB_PASS"],
            db=conf["DB_NAME"],
            cursorclass=pymysql.cursors.DictCursor,
        )
    try:
        g.db_conn.cursor()
    except:
        print("Fallo al conectar la base de datos")
    else:
        print("Conexion exitosa")
    return g.db_conn


def close(e=None):
    conn = g.pop("db_conn", None)

    if conn is not None:
        conn.close()


def init_app(app):
    app.teardown_appcontext(close)

"""from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    config_db(app)

def config_db(app):
    @app.before_first_request
    def init_database():
        db.create_all()
    
    @app_teardown_request
    def close_session(exception=None):
        db.session.remove()"""


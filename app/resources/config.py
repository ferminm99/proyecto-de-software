from flask import redirect, render_template, request, url_for
from app.helpers.auth import required_login, wrap_have_permission
from app.db import db
#------DAO------#
from app.dao.paletteDaoSQLAlchemy import PaletteDao
from app.dao.settingDaoSQLAlchemy import SettingDao


@required_login
@wrap_have_permission(permisos=['settings_index'])
def index():
    db.engine.dispose()
    palettes = PaletteDao.getAll()
    orderByUsers = SettingDao.getByType("orderBy")
    orderByMeetingPoints = SettingDao.getByType("orderByMP")
    return render_template('config.html', data=getSettingsAsDict(), 
    palettes=palettes, orderBy=orderByUsers.element, orderByMP = orderByMeetingPoints.element)



@required_login
@wrap_have_permission(permisos=['settings_update'])  
def updateSettings():

    data = SettingDao.getAll()

    aux = next(x for x in data if x.type == 'orderBy')
    aux.element = request.form['orderBy']
    aux = next(x for x in data if x.type == 'orderByMP')
    aux.element = request.form['orderByMP']
    aux = next(x for x in data if x.type == 'rowsCant')
    aux.element = request.form['rowsCant']

    # actualizando las tablas y commit de los cambios
    for x in range(len(data)):
        db.session.merge(data[x])
    db.session.commit()


    palettes = PaletteDao.getAll()
    orderByUsers = SettingDao.getByType("orderBy")
    orderByMeetingPoints = SettingDao.getByType("orderByMP")
    return render_template('config.html', data=getSettingsAsDict(), 
    palettes=palettes, orderBy=orderByUsers.element, orderByMP = orderByMeetingPoints.element, success= True)


def getSettingsAsDict():
    data = SettingDao.getAll()
    data = dict(zip(map(lambda data: data.type, data),
                    map(lambda data: data.element, data)))
    return data

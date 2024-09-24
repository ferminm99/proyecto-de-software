from flask import render_template, request
from app.helpers.auth import required_login, wrap_have_permission
#------DAO------#
from app.dao.paletteDaoSQLAlchemy import PaletteDao
from app.dao.settingDaoSQLAlchemy import SettingDao

@required_login
@wrap_have_permission(permisos=['palette_index'])
def index():
    palettes = PaletteDao.getAll()
    return render_template("palette.html", palettes=palettes, title="Paleta de Colores")

@required_login
@wrap_have_permission(permisos=['palette_update'])
def update():
 
    paletteAct = PaletteDao.getActive()
    PaletteDao.deactivate(paletteAct.id)

    idPalette = request.form.get('checkStyles')
    PaletteDao.activate(idPalette)

    orderByUsers = SettingDao.getByType("orderBy")
    orderByMeetingPoints = SettingDao.getByType("orderByMP")
    
    palettes = PaletteDao.getAll()
    return render_template('config.html', data=getSettingsAsDict(), palettes=palettes, orderBy=orderByUsers.element, 
        orderByMP = orderByMeetingPoints.element, title="Configuracion del Sistema")

def getSettingsAsDict():
    data = SettingDao.getAll()
    data = dict(zip(map(lambda data: data.type, data),
                    map(lambda data: data.element, data)))
    return data
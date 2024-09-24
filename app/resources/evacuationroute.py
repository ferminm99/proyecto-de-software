from flask import render_template, request, jsonify, session
from app.helpers.auth import required_login, wrap_have_permission
from app.models.evacuationroute import EvacuationRoute
from datatables import ColumnDT, DataTables

#-----DAO-----#
from app.dao.evacuationrouteSQLAlchemy import EvacuationRouteDao
from app.dao.settingDaoSQLAlchemy import SettingDao

@required_login
@wrap_have_permission(permisos=['evacuationroute_index'])
def index():
    idUsuario = session['user'].id
    settings = SettingDao.getByType("rowsCant")
    settingsOrder = SettingDao.getByType("orderByMP")
    return render_template("evacuationroute/index.html", state="2", rows=settings.element, orderCriterion=settingsOrder.element, id=idUsuario)

@required_login
#@wrap_have_permission(permisos=[''])
def new():
    return render_template("evacuationroute/addEvacuationRoute.html")

@required_login
@wrap_have_permission(permisos=['evacuationroute_create'])
def create():
    coordinates = request.form['coordinates']
    formatCoordinates = coordinates[1:len(coordinates)-1]
    
    eroute = EvacuationRoute(request.form['name'], request.form['state'], formatCoordinates, request.form['description'])

    EvacuationRouteDao.insert(eroute)

    return render_template("evacuationroute/addEvacuationRoute.html")

@required_login
#@wrap_have_permission(permisos=[''])
def get_evacuationroute():
    state = request.args.get("state")
    print(state)
    eroute = EvacuationRouteDao.getAllByState(state)
    columns = [
        ColumnDT(EvacuationRoute.name),
        ColumnDT(EvacuationRoute.description),
        ColumnDT(EvacuationRoute.state),
        ColumnDT(EvacuationRoute.coordinates),
        ColumnDT(EvacuationRoute.id),
        ColumnDT(EvacuationRoute.id)
    ]
    rowTable = DataTables(request.args.to_dict(), eroute, columns)

    return jsonify(rowTable.output_result())

@required_login
@wrap_have_permission(permisos=['evacuationroute_show'])
def show():
    id = request.args.get("id")
    route = EvacuationRouteDao.getBy('id',id)
    print(route)
    
    return render_template("evacuationroute/update.html", route=route)

@required_login
@wrap_have_permission(permisos=['evacuationroute_update'])
def update():
    id = request.form['id']
    print(request.form['id'])
    body = request.form.to_dict()
    print(body)
    if 'state' not in body.keys():
        state = 0
    else:
        state = 1
    
    eRoute = EvacuationRoute(request.form['name'], state,[],request.form['description'])
    
    res = EvacuationRouteDao.update(id, eRoute)

    print(res.state)
    return "Actualizado"

@required_login
@wrap_have_permission(permisos=['evacuationroute_update'])
def show_route():
    print(request.args.get("id"))
    id = request.args.get("id")
    route = EvacuationRouteDao.getBy('id',id)

    return render_template("evacuationroute/showRoute.html", coordinates= route.coordinates, id=id)

@required_login
@wrap_have_permission(permisos=['evacuationroute_update'])
def update_route():
    coordinates = request.form['coordinates']
    id = request.form['id']
    formatCoordinates = coordinates[1:len(coordinates)-1]
    print(formatCoordinates)
    EvacuationRouteDao.updateCoordinates(id,formatCoordinates)
    return render_template("evacuationroute/showRoute.html")

@required_login
@wrap_have_permission(permisos=['evacuationroute_destroy'])
def delete():
    id = request.args.get("idERoute")
    EvacuationRouteDao.delete(id)

    idUsuario = session['user'].id
    settings = SettingDao.getByType("rowsCant")
    settingsOrder = SettingDao.getByType("orderByMP")
    return render_template("evacuationroute/index.html", state="2", rows=settings.element, orderCriterion=settingsOrder.element, id=idUsuario)



from flask import jsonify, Blueprint, request
from app.dao.complaintDaoSQLAlchemy import ComplaintDao
from app.dao.categoryDaoSQLAlchemy import CategoryDao
from app.models.complaint import Complaint
from app.db import db
from app.helpers.validator import isValidEmail, isValidText, isValidCoordinates, isNotXSSFormat, isPhoneNumber
import json
from sqlalchemy import func

complaint_api = Blueprint("denuncias", __name__, url_prefix="/denuncias")

@complaint_api.get("/categories")
def categories():
    category_rows = CategoryDao.getAll()
    #return render_template("complaint/new.html", categories = categories)

    categories = [complaint.as_dict() for complaint in category_rows]

    resp = jsonify(categories=categories)
    resp.status_code = 200

    return resp


@complaint_api.get("/")
def index():
    complaint_rows=ComplaintDao.getAllConfirmed()
    complaints = [complaint.as_dict() for complaint in complaint_rows]
    return jsonify(complaints=complaints)


def isValidComplaintRequest(request):
    print("Evaluando request")
    if(len(request)!=8):
        print("0")
        return False
    if(type(request["categoria_id"]) != int):
        print("categoria_id no cumple el formato correcto")
        return "categoria_id no cumple el formato correcto"
    if(not (isValidCoordinates(request["coordenadas"]) and 
        isNotXSSFormat(request["coordenadas"]))):
        print("coordenadas no cumple el formato correcto")
        return "coordenadas no cumple el formato correcto"
    if(not (isValidText(request["apellido_denunciante"]) and 
        isNotXSSFormat(request["apellido_denunciante"]))):
        print("apellido_denunciante no cumple el formato correcto")
        return "apellido_denunciante no cumple el formato correcto"
    if(not (isValidText(request["nombre_denunciante"]) and 
        isNotXSSFormat(request["nombre_denunciante"]))):
        print("nombre_denunciante no cumple el formato correcto")
        return "nombre_denunciante no cumple el formato correcto"
    if(not (isNotXSSFormat(request["telcel_denunciante"]) and 
        isPhoneNumber(request["telcel_denunciante"]))):
        print("telcel_denunciante no cumple el formato correcto")
        return "telcel_denunciante no cumple el formato correcto"
    if(not (isValidEmail(request["email_denunciante"]) and 
        isNotXSSFormat(request["email_denunciante"]))):
        print("email_denunciante no cumple el formato correcto")
        return "email_denunciante no cumple el formato correcto"
    if(not isNotXSSFormat(request["titulo"])):
        print("titulo no cumple el formato correcto")
        return "titulo no cumple el formato correcto"
    if(not isNotXSSFormat(request["descripcion"])):
        print("descripcion no cumple el formato correcto")
        return "descripcion no cumple el formato correcto"
    print("Ok")
    return "Ok"

@complaint_api.post("/")
def create():
    body = request.get_json()
    print("body:")
    print(body)
    coordinates = body["coordenadas"].split(sep=', ', maxsplit=1)
    id = int(body["categoria_id"])
    Ok = isValidComplaintRequest(body)
    if(Ok != "Ok"):
        resp = jsonify({"message": Ok})
        resp.status_code = 400
        return resp
    if(CategoryDao.get(id)==None):
        resp = jsonify({"message": "No existe una categoria que corresponda al category_id indicado"})
        resp.status_code = 400
        return resp
    new_complaint = Complaint(
        title=body["titulo"], id_category=id, email=body["email_denunciante"], 
        latitude=float(coordinates[0]), length=float(coordinates[1]), id_state=1, 
        first_name=body["nombre_denunciante"], last_name=body["apellido_denunciante"], 
        telephone=body["telcel_denunciante"], description=body["descripcion"])
    ComplaintDao.insert(new_complaint)
    message = {
            'atributos': body
        }
    resp = jsonify(message)
    resp.status_code = 201
    return resp
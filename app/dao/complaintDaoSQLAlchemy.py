from sqlalchemy.sql.elements import Null
from app.models import followup
from app.models.category import Category
from app.models.complaint import Complaint
from app.models.followup import FollowUp 
from app.db import db
from sqlalchemy import func

class ComplaintDao:

    @classmethod
    def getAll(cls):
        return Complaint.query.all()
    
    @classmethod
    def getAllConfirmed(cls):
        return Complaint.query.filter(Complaint.id_state!= 1)
    @classmethod
    def getCount(cls):
        return Complaint.query.count()

    @classmethod
    def getAllFollowUp(cls):
        return FollowUp.query.all()

    @classmethod
    def getFollowUpById(cls, id):
        return FollowUp.query.filter_by(id_author=id).first()
    
    @classmethod
    def getFollowsUp(cls, id_complaint):
        return FollowUp.query.filter_by(id_complaint=id_complaint)
        #followsUp = followsUp.order_by(FollowUp.created_at.desc())

    @classmethod
    def getAllByState(cls, state):
        complaint = Complaint.query.with_entities(
        Complaint.title, Complaint.telephone, 
        Complaint.email, Complaint.created_at, Complaint.latitude, Complaint.length, Complaint.id_state, Complaint.id, Complaint.id)
        if (state != "10"):
            complaint = complaint.filter_by(id_state = state)
        db.engine.dispose()
        return complaint

    @classmethod
    def getAllByStateOperator(cls, state,id_user_assigned ):
        complaint = Complaint.query.with_entities(
        Complaint.title, Complaint.telephone, 
        Complaint.email, Complaint.created_at, Complaint.latitude, Complaint.length, Complaint.id_state, Complaint.id, Complaint.id)
        if (state != "10"):
            complaint = complaint.filter_by(id_state = state)
        complaint = complaint.filter_by(id_user_assigned = id_user_assigned)
        db.engine.dispose()
        return complaint

    @classmethod
    def delete(cls, id):
        Complaint.query.filter(Complaint.id == id).delete()
        db.session.commit()
   
    @classmethod
    def getById(cls, id):
        return Complaint.query.filter_by(id=id).first()

    @classmethod
    def update(cls, id_complaint, state, id_user_assigned, description, id, id_category):
        
        complaint = db.session.query(Complaint).filter_by(id=id_complaint).first()
        followup = db.session.query(FollowUp).filter_by(id_complaint=id_complaint).first()

        try:
            idForCompare = int(id_user_assigned)
        except ValueError as e:
            return 'Error'

        if followup is not None and followup.description=="":
            followup.id_author = id_user_assigned
        elif int(id_user_assigned)==id:
            newFollowup = FollowUp(description, id, id_complaint)
            if newFollowup.description != "":
                db.session.add(newFollowup)
        
        complaint.id_user_assigned = id_user_assigned
        complaint.id_category = id_category
        complaint.id_state = state
        if int(complaint.id_state) == 4:
            complaint.closed_at = func.now()
        
        db.session.commit()

    @classmethod
    def updateOperator(cls, id_complaint, state, description, id, id_category):
        
        complaint = db.session.query(Complaint).filter_by(id=id_complaint).first()
        followup = FollowUp(description, id, id_complaint)
        if followup.description != "":
            db.session.add(followup)

        complaint.id_category = id_category
        complaint.id_state = state
        if int(complaint.id_state) == 4:
            complaint.closed_at = func.now()
        
        db.session.commit()

    @classmethod
    def insert(cls, newComplaint):
        """Crea una nueva denuncia en la base de datos

        Args:
            newComplaint (Complaint): denuncia nueva
        """
        db.session.add(newComplaint)
        db.session.commit()
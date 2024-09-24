from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db import db
from sqlalchemy.sql import func
from sqlalchemy.orm import backref, relationship
from app.models.complaint import Complaint

class FollowUp(db.Model):
    __tablename__ = 'Followup'

    id = Column(Integer, primary_key=True)
    description = Column(String(300), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    id_author = Column(Integer, ForeignKey('complaint.id_user_assigned'))
    complaint = db.relationship("Complaint", backref = backref("followup", uselist=False))
    #lo mismo para este de abajo.
    id_complaint = Column(Integer, nullable=False)


    def __init__(self, description, id_author, id_complaint):
        self.description = description
        self.id_author = id_author
        self.id_complaint = id_complaint
        
    def getComplaint(self):
        return self.complaint

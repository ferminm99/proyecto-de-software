from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import backref, relationship
from app.db import db
from app.models.category import Category
from app.resources.user import create
from sqlalchemy import Column, String, Integer
from app.db import db
from sqlalchemy import func

class Complaint(db.Model):
    __tablename__ = 'complaint'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)
    id_category = Column(Integer, nullable=True)
    #id_category = Column(Integer, ForeignKey('category.id'))
    #category = db.relationship("Category", backref = backref("complaint", uselist=False))
    description = Column(String(65535), nullable=True)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    latitude = Column(String(255), nullable=True)
    length = Column(String(255), nullable=True)
    id_state = Column(Integer, nullable=True)
    id_user_assigned = Column(Integer, nullable=True)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    telephone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)

    id_user_assigned = Column(Integer, ForeignKey('User.id'))
    user = db.relationship("User", backref = backref("complaint", uselist=False))
    
    def __init__(self, title=None, id_category=None, closed_at=None, email=None, latitude=None, 
                length=None, id_state=None, id_user_assigned=None, first_name=None, last_name=None, 
                telephone=None, description=None, address=None):
        self.title = title
        self.created_at = func.now()
        self.id_category = id_category
        self.closed_at = closed_at
        self.email = email
        self.latitude = latitude
        self.length = length
        self.id_state = id_state
        self.id_user_assigned = id_user_assigned 
        self.first_name = first_name
        self.last_name = last_name
        self.telephone = telephone
        self.description = description
        self.address = address

    def as_dict(self):
        return {attr.name: getattr(self,attr.name) for attr in self.__table__.columns}
    
    def getId(self):
        return self.id

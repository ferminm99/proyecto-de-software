from sqlalchemy import Column, String, Integer
from app.db import db

class MeetingPoint(db.Model):
    __tablename__ = 'meetingpoint'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    state = Column(Integer, nullable=False)
    telephone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    latitude = Column(String(255), nullable=False)
    length = Column(String(255), nullable=False)
    
    def __init__(self, name, address, state, telephone, email, latitude, length):
        self.name = name
        self.address = address
        self.state = state
        self.telephone = telephone
        self.email = email
        self.latitude = latitude
        self.length = length
        
    def as_dict(self):
        return {attr.name: getattr(self,attr.name) for attr in self.__table__.columns}
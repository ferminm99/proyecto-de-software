from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.db import db
from app.resources.user import create

class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)
    
    def __init__(self, type=None):
        self.type = type
    
    def as_dict(self):
        return {attr.name: getattr(self,attr.name) for attr in self.__table__.columns}
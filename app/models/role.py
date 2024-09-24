from sqlalchemy import Column, String, Integer
from app.db import db


class Role(db.Model):
    __tablename__ = 'Role'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    permissions = db.relationship('Permission', secondary='role_permission',
                                  lazy='subquery', backref=db.backref('roles', lazy='subquery'))
    
    def getName(self):
        return self.name
from sqlalchemy import Column, String, Integer
from app.db import db

class Palette(db.Model):
    __tablename__ = 'Palette'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    className = Column(String(255), nullable=False)
    bgColor = Column(String(255), nullable=False)
    textColor = Column(String(255), nullable=False)
    secondColor = Column(String(255), nullable=False)
    active = Column(Integer, nullable=False)

    def __init__(self, name, className, bgColor, textColor, secondColor, active):
        self.bgColor = bgColor
        self.secondColor = secondColor
        self.textColor = textColor
        self.active = active
        self.className = className
        self.name = name
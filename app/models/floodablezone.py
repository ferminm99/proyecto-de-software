from typing import Text
from sqlalchemy import Column, String, Integer
from app.db import db

class FloodableZone(db.Model):
    __tablename__ = 'floodablezone'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    coordinates = Column(String(4294967295), nullable=False)
    state = Column(Integer, nullable=True)
    colour = Column(String(255), nullable=True)
    
    def __init__(self, name, coordinates, state, color):
        self.name = name
        self.state = state
        self.coordinates = coordinates
        self.colour = color

    def __init__(self, name, coordinates):
        self.name = name
        self.state = 1
        self.coordinates = coordinates
        self.colour = '#3e4144'

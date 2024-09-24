from sqlalchemy import Column, String, Integer
from app.db import db
from typing import Text

class EvacuationRoute(db.Model):
    __tablename__ = 'evacuationroute'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    state = Column(Integer, nullable=False)
    coordinates = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    def __init__(self, name, state, coordinates, description):
        self.name = name
        self.state = state
        self.coordinates = coordinates
        self.description = description
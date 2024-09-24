from app.models.floodablezone import FloodableZone
from app.db import db

class FloodableZoneDao:

    @classmethod
    def getAll(cls):
        return FloodableZone.query.all()
    
    @classmethod
    def getCount(cls):
        return FloodableZone.query.count()

    @classmethod
    def insert(cls,floodablezone):
        db.session.add(floodablezone)
        db.session.commit()

    @classmethod
    def getAllByState(cls, state):
        floodablezone = FloodableZone.query.with_entities(
        FloodableZone.name, FloodableZone.state, FloodableZone.id, FloodableZone.id)
        if (state != "10"):
            floodablezone = floodablezone.filter_by(state=state)
        db.engine.dispose()
        return floodablezone

    @classmethod
    def returnwithID(cls, idzone):
        """ Retorna la zona que matchea con el id pasado como parametro """
        zone = FloodableZone.query.filter(FloodableZone.id == idzone).all()
        db.engine.dispose()
        return zone

    @classmethod
    def delete(cls, idzone):
        FloodableZone.query.filter(FloodableZone.id == idzone).delete()
        db.session.commit()


    @classmethod
    def update(cls, idzone, color, state):
        """ Actualiza, en este caso solo color y estado """
        zone = FloodableZone.query.filter(FloodableZone.id == idzone).first()
        zone.colour = color
        zone.state = state
        db.session.commit()
        return zone

    @classmethod
    def isRepetead(cls, arregloDeNombres):
        namesOfAreas = FloodableZone.query.all()
        return namesOfAreas
        for i in arregloDeNombres:
            if (arregloDeNombres[i] == namesOfAreas):
                return False
        return True

    @classmethod
    def replace(cls, floodablezone):
        FloodableZone.query.filter(FloodableZone.name == floodablezone.name).delete()
        db.session.add(floodablezone)
        db.session.commit()
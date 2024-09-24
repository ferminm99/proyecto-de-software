from app.models.evacuationroute import EvacuationRoute
from app.db import db


class EvacuationRouteDao:

    @classmethod
    def getAll(cls):
        return EvacuationRoute.query.all()

    @classmethod
    def getPage(cls, page, per_page):
        return EvacuationRoute.query.paginate(page=page, per_page=per_page )
    
    @classmethod
    def getCount(cls):
        return EvacuationRoute.query.count()
    
    @classmethod
    def insert(cls, eroute):
        db.session.add(eroute)
        db.session.commit()
    
    @classmethod
    def getAllByState(cls, state="-1"):
        eroute = EvacuationRoute.query.with_entities(
        EvacuationRoute.name, EvacuationRoute.description,  EvacuationRoute.state, EvacuationRoute.coordinates,  EvacuationRoute.id, EvacuationRoute.id )
        if (state != "2"):
            eroute = eroute.filter_by(state=state)
        db.engine.dispose()
        return eroute
    
    @classmethod
    def getBy(cls, criterion, value):
        criteria = {
            'id': EvacuationRoute.query.filter_by(id=value).first()
        }
        return criteria.get(criterion)
    
    @classmethod
    def updateCoordinates(cls, id, values):
        eRoute = db.session.query(EvacuationRoute).filter_by(id=id).first()
        eRoute.coordinates = values
        db.session.commit()
        return eRoute
    
    @classmethod
    def update(cls, id, values):
        eRoute = db.session.query(EvacuationRoute).filter_by(id=id).first()
        eRoute.name = values.name
        eRoute.description = values.description
        eRoute.state = values.state
        db.session.commit()
        return eRoute
    
    @classmethod
    def delete(cls, id):
        """Elimina una ruta de la base de datos
        Args:
            id (int): id de la ruta que se quiere eliminar
        """
        EvacuationRoute.query.filter(EvacuationRoute.id == id).delete()
        db.session.commit()
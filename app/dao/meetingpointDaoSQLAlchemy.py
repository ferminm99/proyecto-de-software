from app.models.meetingpoint import MeetingPoint
from app.db import db

class MeetingPointDao:

    @classmethod
    def getAll(cls):
        return MeetingPoint.query.all()
    
    @classmethod
    def getCount(cls):
        return MeetingPoint.query.count()
    
    @classmethod
    def getPage(cls, page, per_page):
        return MeetingPoint.query.paginate(page=page, per_page=per_page )
    
    @classmethod
    def getCount(cls):
        return MeetingPoint.query.count()
    
    @classmethod
    def getAllWithoutMe(cls, id):
        """Retorna todos los puntos de encuentro excepto del que se pasa id
        Returns:
            Any: una lista de puntos de encuentro
        """
        users = MeetingPoint.query.filter(MeetingPoint.id != id).all()
        db.engine.dispose()
        return users
    
    @classmethod
    def getAllPublics(cls):
        return MeetingPoint.query.filter(MeetingPoint.state == 1).all()

    @classmethod
    def getAllByState(cls, state):
        meetingPoint = MeetingPoint.query.with_entities(
        MeetingPoint.name, MeetingPoint.address, MeetingPoint.telephone, 
        MeetingPoint.email, MeetingPoint.latitude, MeetingPoint.length, MeetingPoint.state, MeetingPoint.id, MeetingPoint.id)
        if (state != "2"):
            meetingPoint = meetingPoint.filter_by(state=state)
        db.engine.dispose()
        return meetingPoint
    
    @classmethod
    def getById(cls, id):
        return MeetingPoint.query.filter_by(id=id).first()
    
    @classmethod
    def insert(cls,meetpoint):
        db.session.add(meetpoint)
        db.session.commit()
    
    @classmethod
    def delete(cls, id):
        MeetingPoint.query.filter(MeetingPoint.id == id).delete()
        db.session.commit()
   
    @classmethod
    def update(cls, id, name, address, state, telephone, email, latitude, length):
        
        meetingpoint = db.session.query(MeetingPoint).filter_by(id=id).first()

        meetingpoint.name = name
        meetingpoint.address = address
        meetingpoint.state = state
        meetingpoint.telephone = telephone
        meetingpoint.email = email
        meetingpoint.latitude = latitude
        meetingpoint.length = length
        db.session.commit()
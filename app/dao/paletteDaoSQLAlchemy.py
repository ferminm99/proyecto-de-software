from app.models.palette import Palette
from app.db import db

class PaletteDao:

    @classmethod
    def getAll(cls):
       return Palette.query.all()
    
    @classmethod
    def activate(cls, id):
        db.session.query(Palette).filter_by(id=int(id)).update({Palette.active:1}, synchronize_session = False)
        db.session.commit()
    
    @classmethod
    def deactivate(cls, id):
        db.session.query(Palette).filter_by(id=int(id)).update({Palette.active:0}, synchronize_session = False)
        db.session.commit()

    @classmethod
    def getActive(cls):
        return Palette.query.filter_by(active=1).first()
from app.db import db

class Permission(db.Model):
    __tablename__ = 'Permission'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

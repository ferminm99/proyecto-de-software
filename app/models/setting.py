from app.db import db

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    element = db.Column(db.String(500), nullable=False)
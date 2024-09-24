from app.db import db

role_permission = db.Table('role_permission',
                            db.Column('id_role_permission',
                                    db.Integer, primary_key=True),
                            db.Column('role_id', db.Integer,
                                    db.ForeignKey('Role.id')),
                            db.Column('permission_id', db.Integer,
                                    db.ForeignKey('Permission.id'))
                           )
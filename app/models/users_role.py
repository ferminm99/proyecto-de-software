from app.db import db

users_role = db.Table('users_role',
                     db.Column('id_users_role', db.Integer, primary_key=True),
                     db.Column('user_id', db.Integer,
                               db.ForeignKey('User.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('Role.id'))
                     )

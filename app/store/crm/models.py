# from app.store.crm.gino import db
from sqlalchemy import func
import gino

db = gino.Gino()

class ConnectInfo(db.Model):
    __tablename__ = 'connect_info'
    id = db.Column(db.Integer(), primary_key=True)
    # connect_time = db.Column(db.DateTime(), server_default='now()') # doesn't work this way
    connect_time = db.Column(db.DateTime(), default=func.now())  # this works well


class UserInfo(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    email = db.Column(db.Unicode(), default=None)
    name = db.Column(db.String, nullable=False)
    # phone = db.Column(nullable=False)

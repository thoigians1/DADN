from unicodedata import name
from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from dataclasses import dataclass

class Base(db.Model):
    __abstract__ = True

    serialize_only = []

    def serialize(self):
        res = {}
        for c in self.__table__.columns:
            if c.name in self.serialize_only:
                res[c.name] = getattr(self, c.name)
        return res

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()


class User(Base, UserMixin):
    __tablename__ = "user"

    serialize_only = ["id", "email", "name"]

    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    pw_hash = db.Column(db.String(80), nullable=False)

    buzzer_log = db.relationship('BuzzerLog', backref='pushed_user', lazy = True )
    control_log = db.relationship('ControlLog', backref='user', lazy = True )



class RoomLog(Base):
    __tablename__ = "room_log"

    serialize_only = ["id", "time", "nop", "rpid"]

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    time = db.Column(db.DateTime, nullable = False)
    nop = db.Column(db.Integer, nullable = False)
    rpid = db.Column(db.Integer, db.ForeignKey('weekly_report.id'))

    
class ControlLog(Base):
    __tablename__ = "control_log"

    serialize_only = ["id", "time", "command", "uid"]

    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime, nullable = False)
    command = db.Column(db.String(20), nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    rpid = db.Column(db.Integer, db.ForeignKey('weekly_report.id'))

class BuzzerLog(Base):
    __tablename__ = "buzzer_log"

    serialize_only = ["id", "time", "uid", ]

    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    rpid = db.Column(db.Integer, db.ForeignKey('weekly_report.id'))

    def serialize(self):
        ser = super().serialize()
        name = User.get_by_id(self.uid).name
        ser.update({'u_name' : name})
        return ser

class WeeklyReport(Base):
    __tablename__ = "weekly_report"

    serialize_only = ["id", "date_created", "average_nop", "max_nop", "n_alert"]

    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    date_created = db.Column(db.DateTime, nullable = False)
    average_nop = db.Column(db.Float)
    max_nop = db.Column(db.Integer, nullable = True)
    n_alert = db.Column(db.Integer, nullable = True)

    room_log = db.relationship('RoomLog', backref='weekly_report', lazy = True)
    control_log = db.relationship('ControlLog', backref='weekly_report', lazy = True)
    buzzer_log = db.relationship('BuzzerLog', backref='weekly_report', lazy = True)
    





    
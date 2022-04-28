from cmath import log
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

    control_log = db.relationship('ControlLog', backref='user', lazy = True )



class RoomLog(Base):
    __tablename__ = "room_log"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)

    time = db.Column(db.DateTime, nullable = False)
    nop = db.Column(db.Integer, nullable = False)
    rpid = db.Column(db.Integer, db.ForeignKey('daily_report_content.id'))

    
class ControlLog(Base):
    __tablename__ = "control_log"

    serialize_only = ["id", "time", "command", "uid"]

    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime, nullable = False)
    command = db.Column(db.String(20), nullable = False)
    door_id = db.Column(db.Integer, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    rpid = db.Column(db.Integer, db.ForeignKey('daily_report.id'))

class BuzzerLog(Base):
    __tablename__ = "buzzer_log"

    serialize_only = ["id", "time", "uid", ]

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    time = db.Column(db.DateTime, nullable = False)
    rpid = db.Column(db.Integer, db.ForeignKey('daily_report_content.id'))

    # def serialize(self):
    #     ser = super().serialize()
    #     name = User.get_by_id(self.uid).name
    #     ser.update({'u_name' : name})
    #     return ser

class DailyReport(Base):
    __tablename__ = "daily_report"
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime)

    content = db.relationship('DailyReportContent', backref='cover', lazy = True, uselist=False)
    week_id = db.Column(db.String, db.ForeignKey('weekly_report.id'))

class DailyReportContent(Base):
    __tablename__ = "daily_report_content"

    id = db.Column(db.Integer, primary_key = True)
    avg_nop = db.Column(db.Integer, nullable=True)
    n_alert = db.Column(db.Integer, nullable=True)

    cover_id = db.Column(db.Integer, db.ForeignKey('daily_report.id'))
    room_log = db.relationship('RoomLog', backref='daily_report', lazy = True)
    buzzer_log = db.relationship('BuzzerLog', backref='daily_report', lazy = True)

class WeeklyReport(Base):
    __tablename__ = "weekly_report"

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, nullable=False)
    content = db.relationship('WeeklyReportContent', backref='cover', lazy = True, uselist=False)

    day_reports = db.relationship('DailyReport', backref='weekly_report', lazy=True)

class WeeklyReportContent(Base):
    # Monitor:
    # Times buzzer triggered
    # Total number of people went in the room in a week
    # average number of people went in the room per day
    __tablename__ = "weekly_report_content"


    id = db.Column(db.Integer, primary_key = True)
    avg_nop = db.Column(db.Float) 
    n_alert = db.Column(db.Integer, nullable = True)
    cover_id = db.Column(db.Integer, db.ForeignKey('weekly_report.id'))







    
from flask import Blueprint, request
from flask_login import current_user, login_required
from datetime import datetime
from app.model import *


api = Blueprint("api",__name__, url_prefix='/api')


# Get list of all user
@api.route("/user", methods=["GET"])
@login_required
def get_all_user():
    users = User.get_all()
    return { 'users' : list(map(lambda log : log.serialize(), users))}

# Get user by id
@api.route("/user/<id>", methods=["GET"])
@login_required
def get_user(id):
    user = User.get_by_id(id)
    return user.serialize()


# Delete user
@api.route("/user/<id>", methods=["DELETE"])
@login_required
def delete_user(id):
    User.delete(id)
    return {}

# Get all room's log
@api.route("/room/log", methods=["GET"])
def get_all_room_log():
    logs = RoomLog.get_all()
    return { 'room_logs' : list(map(lambda log : log.serialize(), logs))}


@api.route("/room/log/<id>", methods=["GET"])
def get_room_log(id):
    log = RoomLog.get_by_id(id)
    return { 'room_logs' : [log.serialize()]}


# Add room's log
# URL Arguments : (nop : int)
@api.route("/room/log", methods=["PUT"])
def add_room_log():
    args = request. args
    if not args.get('nop'):
        return {'status' : 'failed', 'message' : 'Ussage : host/roon/log/add?nop=<int>'}
    nop = args.get('nop')

    rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()

    # If there is no report in database, return an error
    if not rp : 
        return {'status' : "failed", 'message' : 'This log currently does not belong to any report. Please generate a report first.'}
    rpid = rp.id

    log = RoomLog(
        time=datetime.now(),
        nop=nop,
        rpid=rpid
    )

    db.session.add(log)
    db.session.commit()

    return log.serialize()

# Delete a room's log
# URL Arguments : (id : int)
@api.route("/room/log/<id>", methods=["DELETE"])
def delete_room_log(id):
    RoomLog.query.filter_by(id=id).delete()
    db.session.commit()
    return {}


# Get all buzzer's log
@api.route("/buzzer/log", methods=["GET"])
def get_all_buzzer_logs():
    logs = BuzzerLog.get_all()
    return {"buzzer_logs" : []}
    # return { "buzzer_logs" : list( map(lambda log : log.serialize(), logs) )}

@api.route("/buzzer/log/<id>", methods=["GET"])
def get_buzzer_log(id):
    log = BuzzerLog.get_by_id(id)
    return { "buzzer_logs" : [log.serialize()]}


# Add a buzzer's log to database
@api.route("/buzzer/log", methods=["PUT"])
def add_buzzer_log():
    # Find the most recently added report    
    rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()
    # If there is no report in database, return an error
    if not rp : 
        return {'error' : 507, 'message' : 'This log currently does not belong to any report. Please generate a report first.'}

    log = BuzzerLog(
        time=datetime.now(),
        uid=current_user.id,
        rpid=rp.id
    )
    db.session.add(log)
    db.session.commit()
    return log.serialize()

    

@api.route("/buzzer/log/delete/<id>", methods=["DELETE"])
def delete_buzzer_log(id):
    BuzzerLog.delete(id)
    return {}


@api.route("/control/log", methods=["GET"])
def get_all_control_log():
    logs = ControlLog.get_all()
    return { "control_logs" : list( map(lambda log : log.serialize(), logs))}


@api.route("/control/log/<id>", methods=["GET"])
def get_control_log(id):
    log = ControlLog.get_by_id(id)
    return { "control_logs" : [log.serialize()]}
    

@api.route("/control/<command>", methods=["PUT"])
def control_door(command):
    if not command in [0, 1]:
        return {"status" : "failed"}

    rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()
    # If there is no report in database, return an error
    if not rp : 
        return {'status' : "failed", 'message' : 'This log currently does not belong to any report. Please generate a report first.'}

    log = ControlLog(
        time=datetime.now(),
        command=command,
        uid=current_user.id,
        rpid=rp.id
    )

    db.session.add(log)
    db.session.commit()
    return {}

@api.route("/control/<id>", methods=["PUT"])
def delete_control(id):
    ControlLog.delete(id)
    return {}


@api.route("/report/create", methods=["PUT"])
def create_weekly_report():
    rp = WeeklyReport(
        date_created = datetime.now()
    )
    db.session.add(rp)
    db.session.commit()
    return rp.serialize()

@api.route("/report/", methods=["GET"])
def get_all_report():
    rps = WeeklyReport.get_all()
    return { "reports" : list( map(lambda rp: rp.serialize(), rps) )}

@api.route("/report/<id>", methods=["GET"])
def get_report(id):
    rp = WeeklyReport.get_by_id(id)
    return { "reports" : [rp.serialize()]}


@api.route("/report/<id>", methods=["DELETE"])
def delete_report(id):
    WeeklyReport.get_by_id(id).delete()
    return {}


@api.route("/report/<id>/logs/room", methods=["GET"])
def get_report_room_logs(id):
    logs = WeeklyReport.query.get(id).get_room_logs()
    return {
            "room_logs" : list( map(lambda log : log.serialize(), logs) )
        }

@api.route("/report/<id>/logs/buzzer", methods=["GET"])
def get_report_buzzer_logs(id):
    logs = WeeklyReport.query.get(id).get_buzzer_logs()
    return {
            "buzzer_logs" : list( map(lambda log : log.serialize(), logs) )
        }


@api.route("/report/<id>/logs/control", methods=["GET"])
def get_report_control_logs(id):
    logs = WeeklyReport.query.get(id).get_control_logs()
    return {
            "control_logs" : list( map(lambda log : log.serialize(), logs) )
        }

@api.route("/report/<id>/logs", methods=["GET"])
def get_report_logs(id):
    rp = WeeklyReport.query.get(id)
    logs = rp.get_all_logs()
    for k in logs:
        logs.update({ k : list(map(lambda l : l.serialize(), logs[k]))})
    
    return logs
    


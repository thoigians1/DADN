from flask import Blueprint, request
from flask_login import current_user, login_required
from datetime import datetime
from app.model import *


api = Blueprint("api",__name__, url_prefix='/api')


# Get list of all user
@api.route("/user/get/all", methods=["GET"])
@login_required
def get_all_user():
    users = User.get_all()
    return { 'users' : list(map(lambda log : log.serialize(), users))}

# Get user by id
@api.route("/user/get/<id>", methods=["GET"])
@login_required
def get_user(id):
    user = User.get_by_id(id)
    return user.serialize()

@api.route("/user/")
def user_update():
    print(current_user)
    return {}


# Delete user
@api.route("/user/delete/<id>", methods=["DELETE"])
@login_required
def delete_user(id):
    User.delete(id)
    return {}

# Get all room's log
@api.route("/room/log/get/all", methods=["GET"])
def get_all_room_log():
    logs = RoomLog.get_all()
    return { 'logs' : list(map(lambda log : log.serialize(), logs))}


@api.route("/room/log/get/<id>", methods=["GET"])
def get_room_log(id):
    # args = request. args
    # if not args.get('id'):
    #     return {'error' : 428, 'message' : 'Ussage : host/roon/log/get?id=<int>'}
    # id = args.get('id')
    log = RoomLog.get_by_id(id)
    return log.serialize()


# Add room's log
# URL Arguments : (nop : int)
@api.route("/room/log/add", methods=["PUT"])
@login_required
def add_room_log():
    args = request. args
    if not args.get('nop'):
        return {'error' : 428, 'message' : 'Ussage : host/roon/log/add?nop=<int>'}
    nop = args.get('nop')

    rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()

    # If there is no report in database, return an error
    if not rp : 
        return {'error' : 507, 'message' : 'This log currently does not belong to any report. Please generate a report first.'}
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
@api.route("/room/log/delete", methods=["DELETE"])
@login_required
def delete_room_log():
    args = request.args
    if not args.get('id'): 
        return {'error' : 428, 'message' : 'Ussage : HOST/roon/log/delete?id=<int>'}
    id = args.get('id')
    RoomLog.query.filter_by(id=id).delete()
    db.session.commit()
    return {}


# Get all buzzer's log
@api.route("/buzzer/log/get/all", methods=["GET"])
def get_all_buzzer_log():
    logs = BuzzerLog.get_all()
    return { "logs" : list( map(lambda log : log.serialize(), logs) )}


# Add a room's log to database
@api.route("/buzzer/log/add", methods=["PUT"])
@login_required
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


@api.route("/control/log/get/all", methods=["GET"])
def get_all_control_log(id):
    logs = ControlLog.get_all()
    return { "logs" : list( lambda log : log.serialize(), logs)}


@api.route("/control/log", methods=["GET"])
def get_control_log(id):
    log = ControlLog.get_by_id(id)
    return log.serialize()

@api.route("/control/open/", methods=["GET"])
@login_required
def open_door():
    rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()
    # If there is no report in database, return an error
    if not rp : 
        return {'error' : 507, 'message' : 'This log currently does not belong to any report. Please generate a report first.'}

    log = ControlLog(
        time=datetime.now(),
        command='open',
        uid=current_user.id,
        rpid=rp.id
    )

    db.session.add(log)
    db.session.commit()
    return {}
    

@api.route("/control/close", methods=["GET"])
def close_door():
    rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()
    # If there is no report in database, return an error
    if not rp : 
        return {'error' : 507, 'message' : 'This log currently does not belong to any report. Please generate a report first.'}

    log = ControlLog(
        time=datetime.now(),
        command='close',
        uid=current_user.id,
        rpid=rp.id
    )

    db.session.add(log)
    db.session.commit()
    return {}


@api.route("/controle/deactivate", methods=["GET"])
def deactivate_buzzer():
    pass

@api.route("/report/create", methods=["PUT"])
def create_weekly_report():
    rp = WeeklyReport(
        date_created = datetime.now()
    )
    db.session.add(rp)
    db.session.commit()
    return rp.serialize()

@api.route("/report/get/all", methods=["GET"])
def get_all_report():
    rps = WeeklyReport.get_all()
    return { "reports" : list( map(lambda rp: rp.serialize(), rps) )}

@api.route("/report/get/<id>", methods=["GET"])
def get_report(id):
    rp = WeeklyReport.get_by_id(id)
    return rp.serialize()
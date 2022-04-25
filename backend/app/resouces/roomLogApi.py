from flask import request
from flask_restful import Resource, abort, fields, marshal
from datetime import datetime
from app import db, HEADER
from ..model import DailyReport, RoomLog
from ..controller import DailyReportController
from ..utils.function import abort_if_not_exist, date2int
import requests

BASE = r"https://io.adafruit.com/api/v2/duongthanhthuong/feeds/people/data"


roomlog_fields = {
    'id' : fields.String,
    'time' : fields.DateTime,
    'nop' : fields.Integer,
    'rpid' : fields.Integer
}

class RoomLogListAPI(Resource):
    def get(self):
        logs = RoomLog.get_all()
        n = request.args.get('n')
        if n:
            logs = logs[:3]
        
        return { 'room_logs' : list(map(lambda log : marshal(log,roomlog_fields), logs))}

    def post(self):
        nop = request.args.get('nop')
        if nop:
            today = datetime.today()
            rp_id = date2int(today.date())
            
            if not DailyReport.query.get(rp_id) : 
                DailyReportController.createDailyReport()

            log = RoomLog(
                time=datetime.now(),
                nop=nop,
                rpid= rp_id
            )

            db.session.add(log)
            db.session.commit()

            return marshal(log, roomlog_fields)

        abort(404, message='Missing required URL arguments (int:nop)')


class RoomLogAPI(Resource):
    def get(self, id):
        abort_if_not_exist(RoomLog, id)
        log = RoomLog.get_by_id(id)
        return { 'room_logs' : [marshal(log, roomlog_fields)]}

    def delete(self, id):
        abort_if_not_exist(RoomLog, id)
        RoomLog.delete(id)
        requests.delete(BASE + '/' + id, headers=HEADER)
        return {}

class RoomLogRecentAPI(Resource):
    def get(self):
        recent = RoomLog.query.order_by(RoomLog.time.desc()).first()
        return marshal(recent, roomlog_fields)

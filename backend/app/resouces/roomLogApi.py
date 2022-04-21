import json
from flask import request, redirect
from flask_restful import Resource, abort, reqparse, fields, marshal, url_for
from datetime import datetime
from app import db, HEADER
from app.resouces.dailyReportApi import AllDailyReportAPI
from ..model import DailyReport, RoomLog, WeeklyReport
from ..utils.function import abort_if_exist, abort_if_not_exist, date2int
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
        n = request.args.get('n')
        if not n:
            n = 9
        else:
            n = int(n)
        logs = RoomLog.query.order_by(RoomLog.id.desc()).limit(n)
        return { 'room_logs' : list(map(lambda log : marshal(log,roomlog_fields), logs))}

    def post(self):
        # nop = request.args.get('nop')
        nop = request.args.get('nop')
        if nop:
            today = datetime.today()
            rp_id = date2int(today.date())
            
            if not DailyReport.query.get(rp_id) : 
                AllDailyReportAPI().post()

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

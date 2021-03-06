from flask import request
from flask_restful import Resource, reqparse, fields, marshal, abort
from datetime import datetime

from sqlalchemy import values
from app import db, HEADER
from app.resouces.dailyReportApi import AllDailyReportAPI
from ..model import BuzzerLog, DailyReport, WeeklyReport
from ..utils.function import abort_if_exist, abort_if_not_exist, date2int
import requests

BASE = r"https://io.adafruit.com/api/v2/duongthanhthuong/feeds/buzzer/data"

buzzer_fields = {
    'id' : fields.String,
    'time' : fields.DateTime,
    'rpid' : fields.Integer
}

class BuzzerLogListAPI(Resource):
    def get(self):
        logs = BuzzerLog.get_all()
        return {"buzzer_logs" : list( map(lambda log: marshal(log, buzzer_fields), logs))}

    def post(self):
        today = datetime.today()
        rp_id = date2int(today.date())

        if not DailyReport.query.get(rp_id):
            AllDailyReportAPI().post()

        log = BuzzerLog(
            time=datetime.now(),
            rpid=rp_id
        )

        db.session.add(log)
        db.session.commit()
        return marshal(log, buzzer_fields)
        

class BuzzerLogAPI(Resource):
    def get(self, id):
        log = BuzzerLog.get_by_id(id)
        return marshal(log, buzzer_fields)

    def delete(self, id):
        BuzzerLog.delete(id)
        return {}


class DeactivateBuzzerAPI(Resource):
    def get(self):
        resp = requests.post(BASE,{'value' : 5}, headers=HEADER)
        return {'code' : 0 if resp.ok else 1}

class CurrentBuzzerLogAPI(Resource):
    def get(self):
        resp = requests.get(BASE + "/retain", headers=HEADER)
        resp = resp.text[:-1].split(",")
        return {"status" : 0 if resp[0] == "5" else 1}
            

        
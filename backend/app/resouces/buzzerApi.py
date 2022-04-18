from flask import request
from flask_restful import Resource, reqparse, fields, marshal, abort
from datetime import datetime
from app import db, HEADER
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

        if DailyReport.query.get(rp_id) : 

            log = BuzzerLog(
                time=datetime.now(),
                rpid=rp_id
            )

            db.session.add(log)
            db.session.commit()
            return marshal(log, buzzer_fields)

        abort(409, message="Today report has not been created.")
        

class BuzzerLogAPI(Resource):
    def get(self, id):
        log = BuzzerLog.get_by_id(id)
        return marshal(log, buzzer_fields)

    def delete(self, id):
        BuzzerLog.delete(id)
        return {}
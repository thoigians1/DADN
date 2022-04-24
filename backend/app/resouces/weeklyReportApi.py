from dataclasses import field
from flask import request
from flask_restful import Resource, reqparse, fields, marshal, abort
from datetime import datetime
from app import db
from ..model import WeeklyReport
from ..utils.function import abort_if_not_exist, generateDailyReport

report_fields = {
    'id' : fields.Integer,
    'created_at' : fields.DateTime,
    'avg_nop' : fields.Float,
    'n_alert' : fields.Integer
}

daily_rp_fields = {
    "weekday" : fields.String,
    "date" : fields.DateTime,
    "avg_nop" : fields.Float,
    "alert" : fields.Integer
}
class AllWeeklyReportAPI(Resource):
    def get(self):
        rps = WeeklyReport.get_all()
        return {'reports' : list( map(lambda rp: marshal(rp, report_fields), rps) )}

    def post(self):
        today = datetime.today()

        recent_rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()
        if recent_rp and (today - recent_rp.created_at).days <= 7:
            abort(409, message="A report has already created for this week")
        
        rp = WeeklyReport(
            id= int( str(today.date()).replace("-","") ),
            created_at=today,
            average=0.0,
            n_alert=0
        )

        db.session.add(rp)
        db.session.commit()
        return marshal(rp, report_fields),201
        
class WeeklyReportAPI(Resource):
    def get(self, id):
        rp = WeeklyReport.get_by_id(id)
        return marshal(rp, report_fields)

    def delete(self, id):
        abort_if_not_exist(WeeklyReport, id)
        WeeklyReport.delete(id)
        return {}

class CurrentWeekReportAPI(Resource):
    # Get current week report. If has not been created or expired, create a new one
    def get(self):
        recent_rp = getCurrentWeeklyReport()

        return marshal(recent_rp, report_fields)


class GenerateWeeklyReportAPI(Resource):
    def get(self):
        rp = getCurrentWeeklyReport()
        weekday = ["monday","tuesday","wednesday","thursday", "friday", "saturday", "sunday"]
        weekday_rp = []
        sum = 0
        n = 0
        alert = 0
        for drp in rp.day_reports:
            generateDailyReport(drp)
            id = drp.id
            m = len(drp.room_log)
            n += m
            print(drp.avg_nop)
            sum += round(drp.avg_nop*m,2)
            alert += drp.n_alert
            weekday_rp.append(marshal({
                "weekday" : weekday[id%10],
                "date" : drp.created_at,
                "avg_nop" : drp.avg_nop,
                "alert" : drp.n_alert
            },daily_rp_fields))
        w_avg = round(sum/n,2)
        rp.avg_nop = w_avg
        rp.n_alert = alert
        ret = marshal(rp, report_fields)
        ret.update({'weekday_report' : weekday_rp})
        return ret


# Helper Function
def getCurrentWeeklyReport():
    today = datetime.today()
    recent_rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()

    if not recent_rp or (today - recent_rp.created_at).days > 7:
        recent_rp = AllWeeklyReportAPI().post()

    return recent_rp


    
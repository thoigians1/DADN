from functools import reduce
from flask import request, redirect, url_for
from flask_restful import Resource, fields, marshal, abort
from datetime import datetime
from app import db
from app.resouces.weeklyReportApi import AllWeeklyReportAPI
from ..model import DailyReport, WeeklyReport
from ..utils.function import abort_if_not_exist, generateDailyReport

report_fields = {
    'id' : fields.Integer,
    'created_at' : fields.DateTime,
    'avg_nop' : fields.Float,
    'n_alert' : fields.Integer,
}

alert_log_fields = {'time' : fields.DateTime}
class AllDailyReportAPI(Resource):
    def get(self):
        rps = DailyReport.get_all()
        return {'reports' : list( map(lambda rp : marshal(rp,report_fields), rps))}


    def post(self):
        today = datetime.today()

        date = str(today.date()).replace("-","")
        id = int( date + str(today.weekday()) )
        if DailyReport.query.get(id):
            abort(409, message="A daily report has already been created.")
        
        week_rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()
        if not week_rp or (today - week_rp.created_at).days > 7:
            week_rp = AllWeeklyReportAPI().post()[0]
        else:
            week_rp = marshal(week_rp, report_fields)
        
        rp = DailyReport(
            id=id,
            created_at=today,
            in_people=0,
            n_alert=0,
            week_id=week_rp["id"]
        )

        db.session.add(rp)
        db.session.commit()
        
        return marshal(rp, report_fields), 201

class DailyReportAPI(Resource):
    def get(self, id):
        abort_if_not_exist(DailyReport, id)
        return marshal( DailyReport.get_by_id(id), report_fields)

    def delete(self,id):
        abort_if_not_exist(DailyReport, id)
        DailyReport.delete(id)
        return {}

class CurrentDateReport(Resource):
    def get(self):
        rp = getCurrentDailyReport()
        return marshal(rp, report_fields)


class GenerateDailyReportAPI(Resource):
    def get(self, id):
        print(id)
        abort_if_not_exist(DailyReport,id)
        rp = DailyReport.get_by_id(id)
        generateDailyReport(rp)
        alert_logs = list(map( lambda l : marshal(l,alert_log_fields), rp.buzzer_log))
        db.session.commit()
        ret = marshal(rp, report_fields)
        ret.update({"alert_log" : alert_logs})
        return ret


def getCurrentDailyReport():
    today = datetime.today()

    date = str(today.date()).replace("-","")
    id = int( date + str(today.weekday()) )
    rp = DailyReport.query.get(id)
    if not rp:
        return AllDailyReportAPI().post()
    
    return rp
    
            


from dataclasses import field
from flask import request
from flask_restful import Resource, reqparse, fields, marshal, abort
from datetime import datetime
from app import db
from app.controller import WeeklyReportController, DailyReportController
from ..model import WeeklyReport
from ..utils.function import abort_if_not_exist

report_fields = {
    'id' : fields.Integer,
    'created_at' : fields.DateTime,
}

content_fields = {
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
        rp = WeeklyReportController.createWeeklyReport()
        return marshal(rp, report_fields),201
        
class WeeklyReportAPI(Resource):
    def get(self, id):
        rp = WeeklyReport.get_by_id(id)
        content = rp.content
        weekday = ["monday","tuesday","wednesday","thursday", "friday", "saturday", "sunday"]
        weekday_rp = []
        sum = 0
        n = 0
        alert = 0
        for drp in rp.day_reports:
            print(drp)
            drp_content = drp.content
            DailyReportController.generateDailyReport(drp_content)
            id = drp.id
            m = len(drp_content.room_log)
            n += m
            sum += round(drp_content.avg_nop*m,2)
            alert += drp_content.n_alert
            weekday_rp.append(marshal({
                "weekday" : weekday[id%10],
                "date" : drp.created_at,
                "avg_nop" : drp_content.avg_nop,
                "alert" : drp_content.n_alert
            },daily_rp_fields))
        w_avg = round(sum/n,2) if n else 0
        content.avg_nop = w_avg
        content.n_alert = alert
        db.session.commit()

        ret = marshal(rp, report_fields)
        ret.update(marshal(content, content_fields))
        ret.update({'weekday_report' : weekday_rp})
        return ret

    def delete(self, id):
        abort_if_not_exist(WeeklyReport, id)
        WeeklyReport.delete(id)
        return {}



    
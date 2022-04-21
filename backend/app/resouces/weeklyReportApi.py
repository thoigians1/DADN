from dataclasses import field
from flask import request
from flask_restful import Resource, reqparse, fields, marshal, abort
from datetime import datetime
from app import db
from ..model import WeeklyReport
from ..utils.function import abort_if_exist, abort_if_not_exist

report_fields = {
    'id' : fields.Integer,
    'created_at' : fields.DateTime,
    'average' : fields.Float,
    'total' : fields.Integer,
    'n_alert' : fields.Integer
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
        today = datetime.today()
        recent_rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()

        if not recent_rp or (today - recent_rp.created_at).days > 7:
            recent_rp = self.post()

        return marshal(recent_rp, report_fields)


    
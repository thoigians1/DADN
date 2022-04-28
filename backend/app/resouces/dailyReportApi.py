from dataclasses import field
from flask_restful import Resource, fields, marshal
from datetime import datetime
from ..model import DailyReport, DailyReportContent
from ..controller import DailyReportController
from ..utils.function import abort_if_not_exist

report_fields = {
    'id' : fields.Integer,
    'created_at' : fields.DateTime,
}

content_fields = {
    'avg_nop' : fields.Float,
    'n_alert' : fields.Integer,
}

alert_log_fields = {'time' : fields.DateTime}
room_log_fields = {'time' : fields.DateTime, 'nop' : fields.Integer}
class AllDailyReportAPI(Resource):
    def get(self):
        rps = DailyReport.get_all()
        return {'reports' : list( map(lambda rp : marshal(rp,report_fields), rps))}


    def post(self):
        rp = DailyReportController.createDailyReport()
        return marshal(rp, report_fields), 201

class DailyReportAPI(Resource):
    def get(self, id):
        abort_if_not_exist(DailyReport,id)
        rp = DailyReport.get_by_id(id)
        return parseDailyReport(rp)

    def delete(self,id):
        abort_if_not_exist(DailyReport, id)
        DailyReport.delete(id)
        DailyReportContent.delete(id)
        return {}

class CurrentDateReport(Resource):
    def get(self):
        rp = getCurrentDailyReport()
        return parseDailyReport(rp)



def getCurrentDailyReport():
    today = datetime.today()

    date = str(today.date()).replace("-","")
    id = int( date + str(today.weekday()) )
    rp = DailyReport.query.get(id)
    if not rp:
        return AllDailyReportAPI().post()
    
    return rp

def parseDailyReport(rp):
    content = rp.content
    DailyReportController.generateDailyReport(content)
    alert_logs = list(map( lambda l : marshal(l,alert_log_fields), content.buzzer_log))
    room_logs = list( map( lambda l : marshal(l, room_log_fields), content.room_log))
    ret = marshal(rp, report_fields)
    ret.update(marshal(content,content_fields))
    ret.update({'room_logs' : room_logs})
    ret.update({"alert_log" : alert_logs})
    return ret
    
            


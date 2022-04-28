from functools import reduce
from datetime import datetime
from flask_restful import abort
from ..controller import WeeklyReportController
from ..model import db,DailyReport, DailyReportContent, WeeklyReport


def createDailyReport():
    today = datetime.today()

    date = str(today.date()).replace("-","")
    id = int( date + str(today.weekday()) )
    if DailyReport.query.get(id):
        abort(409, message="A daily report has already been created.")
    
    week_rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()
    if not week_rp or (today - week_rp.created_at).days > 7:
        week_rp = WeeklyReportController.createWeeklyReport()
    
    rp = DailyReport(
        id=id,
        created_at=today,
        week_id=week_rp.id
    )

    content = DailyReportContent(
        id=id,
        avg_nop=0,
        n_alert=0,
        cover_id=id
    )

    db.session.add(rp)
    db.session.add(content)
    db.session.commit()


def generateDailyReport(rp):
    sum = reduce(lambda s, rlog : s + rlog.nop, rp.room_log, 0)
    l = len(rp.room_log)
    rp.avg_nop = round(sum/len(rp.room_log),2) if l else 0
    rp.n_alert = len(rp.buzzer_log)

    db.session.commit()

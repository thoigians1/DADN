from flask_restful import abort
from datetime import datetime
from ..model import WeeklyReportContent, db, WeeklyReport

def createWeeklyReport():
    today = datetime.today()

    recent_rp = WeeklyReport.query.order_by(WeeklyReport.id.desc()).first()
    if recent_rp and (today - recent_rp.created_at).days <= 7:
        abort(409, message="A report has already created for this week")
    
    id = int( str(today.date()).replace("-","") )
    
    rp = WeeklyReport(
        id= id,
        created_at=today,
    )

    content = WeeklyReportContent(
        id=id,
        avg_nop=0.0,
        n_alert=0,
        cover_id=id
    )

    db.session.add(rp)
    db.session.add(content)
    db.session.commit()

    return rp
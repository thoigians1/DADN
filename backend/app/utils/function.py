
from email import message
from flask_restful import abort
from functools import reduce
def abort_if_not_exist(model, id):
    if model.query.get(id) == None:
        abort(404, message=f"{model.__name__}:{id} did not exist")

def abort_if_exist(model, id):
    if not model.query.get(id) == None:
        abort(404, message=f"{model.__name__}:{id} already exist")

def date2int(date):
    return int( str(date).replace("-","") + str(date.weekday()))

def generateDailyReport(rp):
    sum = reduce(lambda s, rlog : s + rlog.nop, rp.room_log, 0)
    rp.avg_nop = (sum*100//len(rp.room_log))/100
    rp.n_alert = len(rp.buzzer_log)
    


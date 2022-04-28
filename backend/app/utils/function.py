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
    


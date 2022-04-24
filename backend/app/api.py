from flask import Blueprint, request
from flask_login import current_user, login_required
from flask_restful import Api, Resource
from datetime import datetime
from app.model import *
from app import api
from .resouces.userApi import *
from .resouces.roomLogApi import *
from .resouces.buzzerApi import *
from .resouces.weeklyReportApi import *
from .resouces.dailyReportApi import *


api = Blueprint("api",__name__, url_prefix='/api')
rest_api = Api(api)


rest_api.add_resource(UserListAPI, '/user')
rest_api.add_resource(UserAPI, '/user/<int:id>')

rest_api.add_resource(RoomLogListAPI, '/room/log')
rest_api.add_resource(RoomLogRecentAPI, '/room/log/recent')
rest_api.add_resource(RoomLogAPI, '/room/log/<string:id>')

rest_api.add_resource(BuzzerLogListAPI, '/buzzer/log')
rest_api.add_resource(BuzzerLogAPI, '/buzzer/log/<int:id>')
rest_api.add_resource(DeactivateBuzzerAPI, '/buzzer/off')
rest_api.add_resource(CurrentBuzzerLogAPI, '/buzzer/status')

rest_api.add_resource(AllWeeklyReportAPI, '/report/week')
rest_api.add_resource(WeeklyReportAPI, '/report/week/<int:id>')

rest_api.add_resource(AllDailyReportAPI, '/report/day')
rest_api.add_resource(DailyReportAPI, '/report/day/<int:id>')
from flask_restful import Resource
from ..model import User
from ..utils.function import abort_if_not_exist, abort_if_exist

class UserListAPI(Resource):
    def get(self):
        users = User.get_all()
        return { 'users' : list(map(lambda log : log.serialize(), users))}

    

class UserAPI(Resource):
    def get(self,id):
        abort_if_not_exist(User, id)
        user = User.get_by_id(id)
        return { 'users' : user.serialize()}

    def delete(self, id):
        abort_if_not_exist(User, id)
        User.delete(id)
        return {}
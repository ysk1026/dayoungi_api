from flask import request
from flask_restful import Resource, reqparse

from com_dayoung_api.usr.model.user_dao import UserDao
class Auth(Resource):
    ''' 지금 사용 안함'''
    @staticmethod
    def post():
        body = request.get_json()
        actor = ActorDto(**body)
        ActorDao.save(actor)
        id = actor.actor_id
        return {'id': str(id)}, 200

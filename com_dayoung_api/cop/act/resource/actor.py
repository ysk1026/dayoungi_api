from flask_restful import Resource, reqparse

from com_dayoung_api.cop.act.model.actor_dao import ActorDao

parser = reqparse.RequestParser()
parser.add_argument('actor_id', type=str, required=True,
                    help='This field should be a actorId')
parser.add_argument('password', type=str, required=True,
                    help='This field should be a password')

class Actor(Resource):
    @staticmethod
    def get(id: str):
        print(f'Actor {id} added ')
        try:
            actor = ActorDao.find_by_id(id)
            data = actor.json()
            return data, 200
        except Exception as e:
            print(e)
            return {'message': 'Actor not found'}, 404

    @staticmethod
    def delete(id):
        try:
            ActorDao.delete_actor_by_setting_state_to_one(id)
            print(f'Actor {id} deleted')
            return {'code': 0, 'message': 'SUCCESS'}, 200
        except Exception as e:
            return e, 404

class Actors(Resource):
    @staticmethod
    def post():
        ud = ActorDao()
        ud.bulk('actors')

    @staticmethod
    def get():
        actors = ActorDao.find_state_one()
        data = []
        for actor in actors:
            data.append(actor.json())
        return data[:]


class AddActor(Resource):
    @staticmethod
    def post(name):
        try:
            print(name)
            id = ActorDao.find_id_by_name(name)
        except Exception as e:
            print(e)
            return {'message': 'Actor not found in the database'}, 401
        try:
            ActorDao.add_actor_by_setting_state_to_one(id)
            print(f'Actor {name} added')
        except Exception as e:
            print(e)
            return {'message': 'Actor Already displayed'}, 404
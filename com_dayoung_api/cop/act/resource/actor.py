parser = reqparse.RequestParser()
parser.add_argument('actor_id', type=str, required=True,
                    help='This field should be a actorId')
parser.add_argument('password', type=str, required=True,
                    help='This field should be a password')


class Actor(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()
        print(f'Actor {args["id"]} added ')
        params = json.loads(request.get_data(), encoding='utf-8')
        if len(params) == 0:

            return 'No parameter'

        params_str = ''
        for key in params.keys():
            params_str += 'key: {}, value: {}<br>'.format(key, params[key])
        return {'code': 0, 'message': 'SUCCESS'}, 200

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
    def update():
        args = parser.parse_args()
        print(f'Actor {args["id"]} updated ')
        return {'code': 0, 'message': 'SUCCESS'}, 200

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


class Access(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()
        actor = ActorVo()
        actor.actor_id = args.actorId
        actor.password = args.password
        print(actor.actor_id)
        print(actor.password)
        data = ActorDao.login(actor)
        return data[0], 200


class Auth(Resource):
    @staticmethod
    def post():
        body = request.get_json()
        actor = ActorDto(**body)
        ActorDao.save(actor)
        id = actor.actor_id
        return {'id': str(id)}, 200


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
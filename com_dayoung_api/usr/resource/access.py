from flask_restful import Resource, reqparse
from com_dayoung_api.usr.model.user_dao import UserDao
class Access(Resource):
    """
    서버와 정보를 주고 받는다.
    """
    @staticmethod
    def post():
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('user_id', type=str, required=True,
                                                help='This field should be a user_id')
        parser.add_argument('password', type=str, required=True,
                                                help='This field should be a password')
        args = parser.parse_args()
        print(args)
        user = UserVo()
        user.user_id = args.user_id
        user.password = args.password

        print("아이디: ", user.user_id)
        print("비밀번호: ", user.password)
        data = UserDao.login(user)
        return data[0], 200

from flask_restful import Resource, reqparse
from com_dayoung_api.usr.model.user_dao import UserDao
class Auth(Resource):
    # self, user_id, password,fname, lname, age, gender,email
    @staticmethod
    def post():
        """
        유저 정보를 받아와 새로운 유저를 생성해 준다.
        """
        print("------------------여기는 user.py Auth ------------------- ")
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('user_id', type=str, required=True,
                                                help='This field should be a user_id')
        parser.add_argument('password', type=str, required=True,
                                                help='This field should be a password')
        parser.add_argument('gender', type=str, required=True,
                                                help='This field should be a gender')
        parser.add_argument('email', type=str, required=True,
                                                help='This field should be a email')
        parser.add_argument('lname', type=str, required=True,
                                                help='This field should be a lname')
        parser.add_argument('fname', type=str, required=True,
                                                help='This field should be a fname')
        parser.add_argument('age', type=int, required=True,
                                        help='This field should be a age')
        args = parser.parse_args()
        user = UserDto(args.user_id, args.password, args.fname, args.lname,
                       args.age, args.gender, args.email)

        print("아이디: ", user.user_id)
        print("비밀번호: ", user.password)
        print("이메일 :", user.email)
        print("성 :", user.lname)
        print("이름 :", user.fname)
        print("나이 :", user.age)
        print("성별 :", user.gender)
        try:
            UserDao.register(user)  # return 하긴 함
            return "worked"
        except Exception as e:
            return e
    

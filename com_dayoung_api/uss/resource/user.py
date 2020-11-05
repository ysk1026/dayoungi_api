import os
import json
from flask import request
from flask_restful import Resource, reqparse
from com_dayoung_api.ext.db import db, openSession  # db 선택 Dayoungdb 에서
import pandas as pd
from com_dayoung_api.utils.file_helper import FileReader
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

class User(Resource):
    """
    서버와 정보를 주고 받는다.
    """
    @staticmethod
    def put(id: str):
        """
        서버에서 해당 ID 의 새로운 유저 정보를 받아온다.
        정보를 토대로 해당 ID 유저의 정보를 바꿔서
        정보를 서버에 보내준다.
        parameter: 유저 아이디를 받아온다
        return: 새로운 유저 데이터를 리턴 한다
        """
        parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
        parser.add_argument('user_id', type=str, required=True,
                                                help='This field should be a user_id')
        parser.add_argument('password', type=str, required=True,
                                                help='This field should be a password')
        parser.add_argument('gender', type=str, required=True,
                                                help='This field should be a gender')
        parser.add_argument('lname', type=str, required=True,
                                                help='This field should be a lname')
        parser.add_argument('fname', type=str, required=True,
                                                help='This field should be a fname')
        parser.add_argument('email', type=str, required=True,
                                                help='This field should be a fname')
        parser.add_argument('age', type=int, required=True,
                                                help='This field should be a age')

        print("argument added")
        # def __init__(self, user_id, password,fname, lname, age, gender,email):
        args = parser.parse_args()
        print(f'User {args["user_id"]} updated')
        print(f'User {args["password"]} updated')
        user = UserDto(args.user_id, args.password, args.fname,
                       args.lname, args.age, args.gender, args.email)
        print("user created")
        UserDao.update(user)
        data = user.json()
        return data, 200

    @staticmethod
    def delete(id: str):
        """
        유저 아디를 받아와 해당 유저를 삭제한다.
        Parameter: 유저 아이디
        """
        UserDao.delete(id)
        print(f'User {id} Deleted')

    # @staticmethod
    # def post():
    #     """
    #     이거 아무것도 안하는데??
    #     """
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('user_id', type=str, required=True,
    #                                             help='This field should be a user_id')
    #     parser.add_argument('password', type=str, required=True,
    #                                             help='This field should be a password')
    #     args = parser.parse_args()
    #     print(f'User {args["id"]} added ')
    #     params = json.loads(request.get_data(), encoding='utf-8')
    #     if len(params) == 0:
    #         return 'No parameter'
    #     params_str = ''
    #     for key in params.keys():
    #         params_str += 'key: {}, value: {}<br>'.format(key, params[key])
    #     return {'code': 0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def get(id: str):
        """
        유저 아이디를 받아와 해당 유저 객채를 리턴한다
        Parameter: User ID 를 받아온다
        return: 해당 아이디 유저 객채
        """
        print(f'::::::::::::: User {id} added ')
        try:
            user = UserDao.find_by_id(id)
            data = user.json()
            return data, 200
        except Exception as e:
            print(e)
            return {'message': 'User not found'}, 404

    # @staticmethod
    # def update():
    #     args = parser.parse_args()
    #     print(f'User {args["id"]} updated ')
    #     return {'code':0, 'message': 'SUCCESS'}, 200

    # @staticmethod
    # def delete():
    #     args = parser.parse_args()
    #     print(f'Us er {args["id"]} deleted')
    #     return {'code' : 0, 'message' : 'SUCCESS'}, 200


class Users(Resource):
    """
    서버와 정보를 주고 받는다.
    """
    @staticmethod
    def post():
        """
        모든 유저 정보를 데이터 베이스 안에 넣어준다
        """
        ud = UserDao()
        ud.bulk('users')

    @staticmethod
    def get():
        """
        데이터 베이스 안에 있는 모든 유저 정보를 찾아서 리턴해준다.
        """
        data = UserDao.find_all()
        print("list : ", type(data))
        return data, 200


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


class Delete(Resource):
    """
    정보를 받아와 유저 정보를 삭제 한다
    """
    @staticmethod
    def post(id: str):
        """
        Parameter: 유저 아이디를 받아온다.
        """
        UserDao.delete(id)
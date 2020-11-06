from sqlalchemy import func
import pandas as pd
import json

from com_dayoung_api.ext.db import db, openSession
from com_dayoung_api.usr.model.user_dto import UserDto
from com_dayoung_api.usr.model.user_dfo import UserDfo


Session = openSession()
session = Session()
class UserDao(UserDto):
    """
        User 모델을 접근 하는 객체
        예: CRUD: (Create, Read, Update, Delete)
    """
    
    @staticmethod
    def bulk():
        """
        모든 유저 리스트를 DataBase 안에 넣어준다
        """
        aaa = UserDfo()
        df = aaa.hook()
        print(df.head())
        session.bulk_insert_mappings(UserDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

    @staticmethod
    def count():
        """
        데이터 베이스 안에 몇명의 유저들이 있는지
        숫자를 리턴한다
        """
        return session.query(func.count(UserDto.usr_id)).one()

    @staticmethod
    def update(user):
        """
        유저 정보를 수정해 준다
        새로운 유저 정보를 가진 유저를 가져와 기존의
        유저 정보를 수정해 준다.
        Parameter: 새로운 유저 정보를 가진 유저
        """
        Session = openSession()
        session = Session()
        print(f"{user.lname}")
        print(f"{user.fname}")
        session.query(UserDto).filter(UserDto.usr_id == user.usr_id).update({UserDto.lname: user.lname,
                                                                               UserDto.fname: user.fname,
                                                                               UserDto.age: user.age,
                                                                               UserDto.password: user.password,
                                                                               UserDto.age: user.age,
                                                                               UserDto.email: user.email})
        session.commit()
        session.close()

    @staticmethod
    def register(user):
        """
        새로운 유저를 parameter 로 가져온다.
        새로운 유저를 데이터베이스 안에 넣는다.
        """
        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        """
        유저의 id 정보 (usr_id) 를 가져와
        해당 id를 가진 유저를 데이터베이스에서
        삭제 시켜준다.
        """
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()
        session.close()


    @classmethod
    def find_all(cls):
        """
        데이터 베이스 안에 있는 모든 유저 정보를 찾는다
        Returns:
            제이슨 형식으로 데이터를 리턴해준다.
        """
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def find_by_name(cls, name):
        """
        주어진 이름을 토대로 유저를 찾아서
        해당 정보를 리턴해준다.
        """
        return session.query(UserDto).filter(UserDto.fname.like(f'%{name}%'))

    @classmethod
    def find_by_id(cls, usr_id):
        """
        주어진 아이디를 토대로 유저를 찾아서
        해당 정보를 리턴해준다.
        """
        return session.query(UserDto).filter(UserDto.usr_id.like(f'{usr_id}')).one()

    @classmethod
    def login(cls, user):
        """
        유저 정보를 받아와, 해당 유저가 데이터베이스에 있는지 확인.
        확인 후, 있으면 로그인 시켜준다.
        Parameter: 유저 모델을 받아온다
        return: 유저 정보를 리턴해준다.
        """
        print("----------------login")
        sql = cls.query\
            .filter(cls.usr_id.like(user.usr_id))\
            .filter(cls.password.like(user.password))
        print("login type ", type(sql))
        df = pd.read_sql(sql.statement, sql.session.bind)
        print(json.loads(df.to_json(orient='records')))
        return json.loads(df.to_json(orient='records'))

if __name__ == "__main__":
    """
    데이터 베이스에 모든 유저 정보들을 넣어준다.
    """
    UserDao.bulk()
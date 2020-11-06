import json
import pandas as pd
from flask import request, jsonify
from flask_restful import Resource, reqparse

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func

from com_dayoung_api.ext.db import db, openSession

from com_dayoung_api.cop.rat.model.rating_dfo import RatingDfo
from com_dayoung_api.cop.rat.model.rating_dto import RatingDto

Session = openSession()
session = Session()
class RatingDao(RatingDto):

    @staticmethod
    def bulk():
        print('***** [movie_rating] df 삽입 *****')
        m = RatingDfo()
        df = m.hook()
        print(df)
        session.bulk_insert_mappings(RatingDto, df.to_dict(orient='records'))
        session.commit()
        session.close()
        print('***** [movie_rating] df 삽입 완료 *****')

    @classmethod
    def count(cls):
        return session.query(func.count(RatingDto.rat_id)).one()

    @classmethod
    def find_all(cls):
        print('find_all')
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @staticmethod
    def find_by_id(rat_id):
        print('##### find id #####')
        return session.query(RatingDto).filter(RatingDto.rat_id.like(rat_id)).all()

    @staticmethod
    def register_rating(rating):
        print('##### new rating data registering #####')
        print(rating)
        newRating = RatingDao(rat_id = rating['rat_id'],
                            userid = rating['userid'],
                            movieid = rating['movieid'],
                            rating = rating['rating'])
        session.add(newRating)
        session.commit()
        db.session.close()
        print('##### new rating data register complete #####')

    # update [table] set [field] = '변경값' where = '조건값'
    # session.query(테이블명).filter(테이블명.필드명 == 조건 값).update({테이블명.필드명:변경 값})

    @staticmethod
    def modify_rating(rat_id):
        print('##### rating data modify #####')
        session.query(RatingDto).filter(RatingDto.rat_id == rat_id['rat_id']).update({RatingDto.rating:rat_id['rating']})                                                        
        session.commit()
        session.close()

        print('##### rating data modify complete #####')

    @classmethod
    def delete_rating(cls, rat_id):
        print('##### rating data delete #####')
        data = cls.query.get(rat_id)
        db.session.delete(data)
        session.commit()
        session.close()
        print('##### rating data delete complete #####')
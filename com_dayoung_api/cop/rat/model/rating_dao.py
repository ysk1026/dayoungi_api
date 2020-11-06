import json
import pandas as pd
from flask import request, jsonify
from flask_restful import Resource, reqparse

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func

from com_dayoung_api.ext.db import db, openSession

from com_dayoung_api.cop.rat.model.rating_dfo import MovieRatingDf
from com_dayoung_api.cop.rat.model.rating_dto import MovieRatingDto

Session = openSession()
session = Session()
class MovieRatingDao(MovieRatingDto):

    @staticmethod
    def bulk():
        print('***** [movie_rating] df 삽입 *****')
        m = MovieRatingDf()
        df = m.hook()
        print(df)
        session.bulk_insert_mappings(MovieRatingDto, df.to_dict(orient='records'))
        session.commit()
        session.close()
        print('***** [movie_rating] df 삽입 완료 *****')

    @classmethod
    def count(cls):
        return session.query(func.count(MovieRatingDto.ratingid)).one()

    @classmethod
    def find_all(cls):
        print('find_all')
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @staticmethod
    def find_by_id(ratingid):
        print('##### find id #####')
        return session.query(MovieRatingDto).filter(MovieRatingDto.ratingid.like(ratingid)).all()

    @staticmethod
    def register_rating(rating):
        print('##### new rating data registering #####')
        print(rating)
        newRating = MovieRatingDao(ratingid = rating['ratingid'],
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
    def modify_rating(ratingid):
        print('##### rating data modify #####')
        session.query(MovieRatingDto).filter(MovieRatingDto.ratingid == ratingid['ratingid']).update({MovieRatingDto.rating:ratingid['rating']})                                                        
        session.commit()
        session.close()

        print('##### rating data modify complete #####')

    @classmethod
    def delete_rating(cls, ratingid):
        print('##### rating data delete #####')
        data = cls.query.get(ratingid)
        db.session.delete(data)
        session.commit()
        session.close()
        print('##### rating data delete complete #####')
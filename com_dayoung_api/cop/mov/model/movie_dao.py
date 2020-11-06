from typing import List
import json
import pandas as pd
import os
import sys
import urllib.request
import csv
import ast
import time
from pandas import DataFrame
from pathlib import Path

from flask import request, jsonify
from flask_restful import Resource, reqparse

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func

from com_dayoung_api.ext.db import db, openSession

from com_dayoung_api.cop.mov.model.movie_dto import MovieDto
from com_dayoung_api.cop.mov.model.movie_dfo import MovieDf

Session = openSession()
session = Session()

class MovieDao(MovieDto):
    
    @staticmethod
    def bulk():
        print('***** [movies_recommendation] df 삽입 *****')
        recomoviedf = MovieDf()
        df = recomoviedf.hook()
        print(df)
        session.bulk_insert_mappings(MovieDto, df.to_dict(orient='records'))
        session.commit()
        session.close()
        print('***** [movies_recommendation] df 삽입 완료 *****')

    @staticmethod
    def count():
        return session.query(func.count(MovieDto.mov_id)).one()
    
    @classmethod
    def find_by_title(cls, title):
        print('##### find title #####')
        return session.query(MovieDto).filter(MovieDto.title_kor.like(title)).all()
    
    @classmethod
    def find_by_id(cls, mov_id):
        print('##### find title #####')
        return session.query(MovieDto).filter(MovieDto.mov_id.like(f'{mov_id}')).one()

    @classmethod
    def find_all(cls):
        print('***** find all movie_reco *****')
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

# mov_id,movie_l_title,movie_l_org_title,movie_l_genres,movie_l_year,movie_l_rating,movie_l_rating_count
    @staticmethod
    def register_movie(movie):
        print('##### new movie data registering #####')
        print(movie)
        newMovie = MovieDao(mov_id = movie['mov_id'],
                            title_kor = movie['title_kor'],
                            title_naver_eng = movie['title_naver_eng'],
                            genres_kor = movie['genres_kor'],
                            keyword_kor = movie['keyword_kor'],
                            running_time_kor = movie['running_time_kor'],
                            year_kor = movie['year_kor'],
                            director_naver_kor = movie['director_naver_kor'],
                            actor_naver_kor = movie['actor_naver_kor'],
                            movie_l_rating = movie['movie_l_rating'],
                            movie_l_rating_count = movie['movie_l_rating_count'],
                            movie_l_popularity = movie['movie_l_popularity'],
                            link_naver = movie['link_naver'],
                            image_naver = movie['image_naver'])
        session.add(newMovie)
        session.commit()
        session.close()
        print('##### new movie data register complete #####')

    @staticmethod
    def modify_movie(movie):
        print('##### movie data modify #####')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        session.query(MovieDto).filter(MovieDto.mov_id == movie['mov_id']).update({MovieDto.title_kor:movie['title_kor'],
                                                                                    MovieDto.title_naver_eng:movie['title_naver_eng'],
                                                                                    MovieDto.genres_kor:movie['genres_kor'],
                                                                                    MovieDto.keyword_kor:movie['keyword_kor'],
                                                                                    MovieDto.running_time_kor:movie['running_time_kor'],
                                                                                    MovieDto.year_kor:movie['year_kor'],
                                                                                    MovieDto.director_naver_kor:movie['director_naver_kor'],
                                                                                    MovieDto.actor_naver_kor:movie['actor_naver_kor'],
                                                                                    MovieDto.movie_l_rating:movie['movie_l_rating'],
                                                                                    MovieDto.movie_l_rating_count:movie['movie_l_rating_count'],
                                                                                    MovieDto.movie_l_popularity:movie['movie_l_popularity'],
                                                                                    MovieDto.link_naver:movie['link_naver'],
                                                                                    MovieDto.image_naver:movie['image_naver']})                                                        
        session.commit()
        session.close()
        print('##### movie data modify complete #####')

    @classmethod
    def delete_movie(cls,mov_id):
        print('##### movie data delete #####')
        data = cls.query.get(mov_id)
        db.session.delete(data)
        db.session.commit()
        db.session.close()
        print('##### movie data delete complete #####')
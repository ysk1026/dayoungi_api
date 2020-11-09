from flask_restful import Resource, reqparse
from flask import request
import json
from flask import jsonify
import pandas as pd
import numpy as np
import os
from com_dayoung_api.cop.rev.model.review_dfo import ReviewDfo 
from com_dayoung_api.cop.rev.model.review_dto import ReviewDto
from com_dayoung_api.cop.mov.model.movie_dao import MovieDao
from com_dayoung_api.cop.mov.model.movie_dto import MovieDto, MovieVo
from com_dayoung_api.ext.db import db, openSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func

class ReviewDao(ReviewDto):
    
    @classmethod
    def count(cls):
        Session = openSession()
        session = Session()
        return session.query(func.count(ReviewDto.rev_id)).one()

    @classmethod
    def group_by(cls):
        Session = openSession()
        session = Session()
        titledict = {}
        titles = session.query(cls.title, cls.label).all() # 타이틀 뽑아 왔음
        for title in titles:
            if title[0] not in titledict:
                titledict[title[0]] = 1
            else:
                titledict[title[0]] += 1
            if title[1] == 1:
                titledict[title[0]] += 1
        titledict = {k: v for k, v in sorted(titledict.items(), key=lambda item: item[1])}
        return titledict
            
                
    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        df_movie_id = df['mov_id']
        print(df_movie_id[0])
        print(len(df['mov_id']))
        count = 0
        for movie in df_movie_id:
            df_movie_id[count] = MovieDao.find_by_id(movie).title_kor 
            print(MovieDao.find_by_id(movie).title_kor)
            count += 1
        return json.loads(df.to_json(orient='records'))
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name == name)
    
    @classmethod
    def find_by_id(cls, id):
        Session = openSession()
        session = Session()
        print("FIND BY ID method 진입!")
        print(f'ID : {id}')

        return session.query(ReviewDto).filter(ReviewDto.rev_id.like(id)).one()
    
    @classmethod
    def find_review_by_user_id(cls, user_id):
        Session = openSession()
        session = Session()
        print("FIND BY USER ID METHOD 진입!")
        print ("성공")
        return session.query(ReviewDto).filter(ReviewDto.usr_id.like(user_id)).all()
    
    '''
    위에 find_review_by_user_id가 기존에 있던 코드
    밑에 껄로 join 해서 시도중, 안되면 위에껄로 다시 초기화 해야함..
    매우 어렵다
    '''
    '''
    @classmethod
    def find_review_by_user_id(cls, user_id):
        Session = openSession()
        session = Session()
        print("FIND BY USER ID METHOD 진입!")
        print ("성공")
        print()
        print("USER ID의 리뷰 불러오기!")
        f = session.query(ReviewDto).join(MovieDto).filter(MovieDto.mov_id.like(ReviewDto.mov_id)).all()
        for a in f:
            print(a)
        # print(f)
        # print(f.title_kor) 
        # print(session.query(f).filter(f.mov_id.like(2)).one())
        
        li = []
        count = 1
        original_review = session.query(ReviewDto).filter(ReviewDto.usr_id.like(user_id)).all()
        for rev_data in original_review:
            df = pd.DataFrame( {
                'usr_id' : rev_data.usr_id,
                'mov_id' : rev_data.mov_id,
                'title' : rev_data.title,
                'content' : rev_data.content,
                'label' : rev_data.label
            }, index = [0])
            mov_id = rev_data.mov_id
            for u, a in session.query(ReviewDto, MovieDto).filter(mov_id == MovieDto.mov_id).all():
                count += 1
                if count % 2 != 0:
                    continue
                print("출력")
                print(a.title_kor)
                df['mov_id'] = a.title_kor
                df = json.loads(df.to_json(orient='records'))
                li.append(df)
        print(li)
        # q = session.query(ReviewDto).join(MovieDto).filter(MovieDto.mov_id == mov_id).one()
        return session.query(ReviewDto).filter(ReviewDto.usr_id.like(user_id)).all()
        '''
    
    @classmethod
    def find_by_movie_title(cls, title):
        Session = openSession()
        session = Session()
        print("FIND BY TITLE 진입 !")
        return session.query(ReviewDto).filter(ReviewDto.title.like(title)).all()
    
    @staticmethod
    def save(review):
        Session = openSession()
        session = Session()
        print('SAVE 진입')
        print(f'REVIEW: {review}')
        print(f'Rev id : {review.rev_id} / Movie_id :{review.mov_id}/\
            User_id: {review.usr_id}/ Title: {review.title}/ Content: {review.content} / Label: {review.label}')
        print('1 clear')
        session.add(review)
        print('2 clear')
        session.commit()
        print('3 clear')
        session.close()
        print('4 clear')
    
    @staticmethod
    def update(review, id):
        Session = openSession()
        session = Session()
        print('진입')
        print(f'Rev id : {review.rev_id} / Movie_id :{review.mov_id}/\
            User_id: {review.usr_id}/ Title: {review.title}/ Content: {review.content} / Label: {review.label}')
        print('update 1 clear')
        print(f'************ID : {id} **************** ')
        print('update 2 clear')
        session.query(ReviewDto).filter(ReviewDto.rev_id == review.rev_id).update({ReviewDto.usr_id:review.usr_id,
                                                                                   ReviewDto.mov_id:review.mov_id,
                                                                                   ReviewDto.title:review.title,
                                                                                   ReviewDto.content:review.content,
                                                                                   ReviewDto.label:review.label
                                                                                   })
        print('update 3 clear')
        session.commit()
        session.close()
        print('update 4 clear')
    
    @staticmethod   
    def insert_many():
        service = ReviewDfo()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(ReviewDto, df.to_dict(orient="records"))
        session.commit()
        session.close()          
        
    @classmethod
    def delete(cls,rev_id):
        print('##### review data delete #####')
        print(rev_id)
        data = cls.query.get(rev_id)
        print(f'###### review data: {data}')
        db.session.delete(data)
        print("Delete in progress")
        db.session.commit()
        print('##### review data delete complete #####')
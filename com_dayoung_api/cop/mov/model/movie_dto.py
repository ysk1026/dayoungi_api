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

class MovieDto(db.Model):
    
    __tablename__ = 'movies'
    __talbe_args__ = {'mysql_collate':'utf8_general_ci'}
    
    '''
    DataFrame Columns(14)
    'movieid', 
    'title_kor', 
    'title_naver_eng', 
    'genres_kor', 
    'keyword_kor',
    'running_time_kor', 
    'year_kor', 
    'director_naver_kor', 
    'actor_naver_kor',
    'movie_l_rating', 
    'movie_l_rating_count', 
    'movie_l_popularity',
    'link_naver', 
    'image_naver'
    '''
    mov_id : int = db.Column(db.Integer, primary_key = True, index = True)
    title_kor : str = db.Column(db.String(100))
    title_naver_eng : str = db.Column(db.String(100))
    genres_kor : str = db.Column(db.String(30))
    keyword_kor : str = db.Column(db.String(150))
    running_time_kor : int = db.Column(db.Integer)
    year_kor : str = db.Column(db.String(4))
    director_naver_kor : str = db.Column(db.String(50))
    actor_naver_kor : str = db.Column(db.String(50))
    movie_l_rating : float = db.Column(db.Float)
    movie_l_rating_count : int = db.Column(db.Integer)
    movie_l_popularity : float = db.Column(db.Float)
    link_naver : str = db.Column(db.String(80))
    image_naver : str = db.Column(db.String(80))

    def __init__(self, 
                mov_id, 
                title_kor,
                title_naver_eng, 
                genres_kor, 
                keyword_kor, 
                running_time_kor, 
                year_kor,
                director_naver_kor,
                actor_naver_kor,
                movie_l_rating,
                movie_l_rating_count,
                movie_l_popularity,
                link_naver,
                image_naver
                ):
        self.mov_id = mov_id
        self.title_kor = title_kor
        self.title_naver_eng = title_naver_eng
        self.genres_kor = genres_kor
        self.keyword_kor = keyword_kor
        self.running_time_kor = running_time_kor
        self.year_kor = year_kor
        self.director_naver_kor = director_naver_kor
        self.actor_naver_kor = actor_naver_kor
        self.movie_l_rating = movie_l_rating
        self.movie_l_rating_count = movie_l_rating_count
        self.movie_l_popularity = movie_l_popularity
        self.link_naver = link_naver
        self.image_naver = image_naver


    def json(self):
        return {
            'mov_id' : self.mov_id,
            'title_kor' : self.title_kor,
            'title_naver_eng' : self.title_naver_eng,
            'genres_kor' : self.genres_kor,
            'keyword_kor' : self.keyword_kor,
            'running_time_kor' : self.running_time_kor,
            'year_kor' : self.year_kor,
            'director_naver_kor' : self.director_naver_kor,
            'actor_naver_kor' : self.actor_naver_kor,
            'movie_l_rating' : self.movie_l_rating,
            'movie_l_rating_count' : self.movie_l_rating_count,
            'movie_l_popularity' : self.movie_l_popularity,
            'link_naver' : self.link_naver,
            'image_naver' : self.image_naver
        }

class MovieVo():
    mov_id: int = 0
    title_kor: str = ''
    title_naver_eng: str = ''
    genres_kor: str = ''
    keyword_kor: str = ''
    running_time_kor: int = 0
    year_kor: str = ''
    director_naver_kor: str = ''
    actor_naver_kor: str = ''
    movie_l_rating: float = 0.0
    movie_l_rating_count: int = 0
    movie_l_popularity: float = 0.0
    link_naver: str = ''
    image_naver: str = ''
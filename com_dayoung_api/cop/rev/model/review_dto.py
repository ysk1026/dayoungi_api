from typing import List
from flask_restful import Resource, reqparse
from flask import request
import json
from flask import jsonify
import pandas as pd
import numpy as np
import os
from com_dayoung_api.cmm.util.file_helper import FileReader
from com_dayoung_api.cop.mov.model.movie_dto import MovieDto
from com_dayoung_api.usr.model.user_dto import UserDto

from pathlib import Path
from com_dayoung_api.ext.db import db, openSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func

class ReviewDto(db.Model):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}
    
    rev_id: int = db.Column(db.Integer, primary_key=True, index=True)
    title: str = db.Column(db.String(100))
    content: str = db.Column(db.String(500))
    label: int = db.Column(db.Integer)
     
    usr_id: str = db.Column(db.String(30), db.ForeignKey(UserDto.usr_id))
    mov_id: int = db.Column(db.Integer, db.ForeignKey(MovieDto.mov_id))
    
    # movie = db.relationship('MovieDto', back_populates="reviews")
    
    def __init__(self, title, content, label, usr_id, mov_id):
        self.title = title
        self.content = content
        self.label = label
        self.usr_id = usr_id
        self.mov_id = mov_id
        
    def __repr__(self):
        return f'rev_id = {self.rev_id}, usr_id = {self.usr_id}, mov_id = {self.mov_id},\
            title = {self.title}, content = {self.content}, label = {self.label}'
    
    def json(self):
        return {
            'rev_id' : self.rev_id,
            'usr_id' : self.usr_id,
            'mov_id' : self.mov_id,
            'title' : self.title,
            'content' : self.content,
            'label' : self.label
        }
        
class ReviewVo:
    rev_id: int = 0
    title: str = ''
    content: str = ''
    label: int = 0
    usr_id: str = ''
    mov_id: int = 0
from typing import List
import json
import pandas as pd
import numpy as np
import os
from com_dayoung_api.cmm.util.file_helper import FileReader
from pathlib import Path
from com_dayoung_api.ext.db import db, openSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func

class ReviewDfo(object):
    
    def __init__(self):
        self.fileReader = FileReader()
        self.data = os.path.join(os.path.abspath(os.path.dirname(__file__)) + '/data')
        
    def hook(self):
        train = 'rating.csv'
        this = self.fileReader
        this.train = self.new_model(train) # payload
        df = pd.DataFrame(
            {
                'user_id' : this.train.id,
                'movie_id' : '2',
                'title' : 'Avengers',
                'content' : this.train.document,
                'label' : this.train.label
            }
        )
        df = df.dropna()
        df = df[:50] # 데이터 불러올 갯수, 너무 많아지면 핸들링하기 힘드니 상황에 맞게 조절한다.
        print(df.head())
        
        return df
    
    def new_model(self, payload) -> object:
        this = self.fileReader
        this.data = self.data
        this.fname = payload
        print(f'{self.data}')
        print(f'{this.fname}')
        return pd.read_csv(Path(self.data, this.fname))
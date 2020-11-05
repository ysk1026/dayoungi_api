import os
import json
from flask import request
from flask_restful import Resource, reqparse
from com_dayoung_api.ext.db import db, openSession  # db 선택 Dayoungdb 에서
import pandas as pd
from com_dayoung_api.utils.file_helper import FileReader
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property


class UserDfo(object):
    """
    [This class is the main operator for user]
    Creates User Database with 7 columns.
    This enables user CRUD (Crete, Read, Update, Delete)
    Args:
        object ([object]): [description]
    """
    def __init__(self):
        """
        Creates fileReader object and sets the path to ""
        """
        self.fileReader = FileReader()
        self.path = os.path.abspath("")

    def hook(self):
        """
            Creates new model,
            for now it simply creates new_model which gets data from user.csv
        """
        data = self.new_model()
        print(data)
        return data

    def new_model(self) -> object:        
        path = os.path.abspath("")
        # \com_dayoung_api\
        fname = r"\com_dayoung_api\resources\data\user.csv"
        data = pd.read_csv(path + fname, encoding='utf-8')
        # print('***********')
        # data = data.head()
        # print(data)
        return data
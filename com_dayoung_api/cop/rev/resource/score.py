from flask_restful import Resource, reqparse
from flask import request
import json
from flask import jsonify
from com_dayoung_api.cop.rev.model.review_dao import ReviewDao

class ReviewScore(Resource):
    
    @staticmethod
    def get():
        print("진입")
        top_movie = ReviewDao.group_by()
        return top_movie
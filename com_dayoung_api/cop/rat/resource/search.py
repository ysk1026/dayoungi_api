from com_dayoung_api.cop.rat.model.rating_dao import MovieRatingDao
from com_dayoung_api.cop.rat.model.rating_dto import MovieRatingDto
from flask import request, jsonify
from flask_restful import Resource, reqparse

class MovieRatingSearch(Resource):
    def get(self, ratingid):
        print("SEARCH 진입")
        print(f'ratingid : {ratingid}')
        movie = MovieRatingDao.find_by_id(ratingid)
        movielist = []
        for rev in movie:
            movielist.append(rev.json())
        print(f'Review List : {movielist}')
        return movielist[:]
from com_dayoung_api.cop.rat.model.rating_dao import RatingDao
from com_dayoung_api.cop.rat.model.rating_dto import RatingDto
from flask import request, jsonify
from flask_restful import Resource, reqparse

class Rating(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('ratingid', type=int, required=False, help='This field should be a ratingid')
        parser.add_argument('userid', type=int, required=True, help='This field should be a userid')
        parser.add_argument('movieid', type=int, required=True, help='This field should be a movieid')
        parser.add_argument('rating', type=float, required=True, help='This field should be a rating')    
        args = parser.parse_args()
        ratings = RatingDto(args['ratingid'], \
                        args['userid'], \
                        args['movieid'], \
                        args['rating'])
        print('*********')
        print(args)
        try:
            RatingDao.register_rating(args)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured registering the rating'}, 500

    @staticmethod
    def get(id: str):
        try:
            reco_movie = RatingDao.find_by_id(id)
            data = reco_movie.json()
            print(data)
            return data, 200
        except:
            print('fail')
            return {'message':'Title not found'}, 404

    @staticmethod
    def put():
        parser = reqparse.RequestParser()
        parser.add_argument('ratingid', type=int, required=True, help='This field should be a ratingid')
        parser.add_argument('userid', type=int, required=False, help='This field should be a userid')
        parser.add_argument('movieid', type=int, required=False, help='This field should be a movieid')
        parser.add_argument('rating', type=float, required=True, help='This field should be a rating')    
        args = parser.parse_args()
        ratings = RatingDto(args['ratingid'], \
                        args['userid'], \
                        args['movieid'], \
                        args['rating'])
        print('*********')
        print(args)
        try:
            RatingDao.modify_rating(args)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured registering the rating'}, 500

class Ratings(Resource):
    
    def post(self):
        md = RatingDao()
        md.bulk('movies')

    def get(self):
        data = RatingDao.find_all()
        return data, 200

class RatingDel(Resource):

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('ratingid', type=int, required=True, help='This field should be a ratingid')
        args = parser.parse_args()
        print('*********')
        print(args)
        ratingid = args['ratingid']

        try:
            RatingDao.delete_rating(ratingid)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured registering the movie'}, 500
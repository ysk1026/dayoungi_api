from flask import request, jsonify
from flask_restful import Resource, reqparse

from com_dayoung_api.cop.mov.model.movie_dao import RecoMovieDao
from com_dayoung_api.cop.mov.model.movie_dto import RecoMovieDto
from com_dayoung_api.cop.mov.model.movie_dfo import RecoMovieDf

class RecoMovie(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('movieid', type=int, required=False, help='This field should be a movieid')
        parser.add_argument('title_kor', type=str, required=True, help='This field should be a title_kor')
        parser.add_argument('title_naver_eng', type=str, required=True, help='This field should be a title_naver_eng')
        parser.add_argument('genres_kor', type=str, required=True, help='This field should be a genres_kor')
        parser.add_argument('keyword_kor', type=str, required=True, help='This field should be a keyword_kor')
        parser.add_argument('running_time_kor', type=int, required=True, help='This field should be a running_time_kor')
        parser.add_argument('year_kor', type=str, required=True, help='This field should be a year_kor')
        parser.add_argument('director_naver_kor', type=str, required=True, help='This field should be a director_naver_kor')
        parser.add_argument('actor_naver_kor', type=str, required=True, help='This field should be a actor_naver_kor')
        parser.add_argument('movie_l_rating', type=float, required=True, help='This field should be a movie_l_rating')
        parser.add_argument('movie_l_rating_count', type=int, required=True, help='This field should be a movie_l_rating_count')
        parser.add_argument('movie_l_popularity', type=float, required=True, help='This field should be a movie_l_popularity')
        parser.add_argument('link_naver', type=str, required=True, help='This field should be a link_naver')
        parser.add_argument('image_naver', type=str, required=True, help='This field should be a image_naver')              
        args = parser.parse_args()
        print('*********')
        print(args)
        try:
            RecoMovieDao.register_movie(args)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured registering the movie'}, 500

    @staticmethod
    def get(id: str):
        print('##### get #####')
        print(id)
        try:
            reco_movie = RecoMovieDao.find_by_title(id)
            data = reco_movie.json()
            print(data)
            return data, 200
        except:
            print('fail')
            return {'message':'Title not found'}, 404

    @staticmethod
    def put():
        parser = reqparse.RequestParser()
        parser.add_argument('movieid', type=int, required=True, help='This field should be a movieid')
        parser.add_argument('title_kor', type=str, required=True, help='This field should be a title_kor')
        parser.add_argument('title_naver_eng', type=str, required=True, help='This field should be a title_naver_eng')
        parser.add_argument('genres_kor', type=str, required=True, help='This field should be a genres_kor')
        parser.add_argument('keyword_kor', type=str, required=True, help='This field should be a keyword_kor')
        parser.add_argument('running_time_kor', type=int, required=True, help='This field should be a running_time_kor')
        parser.add_argument('year_kor', type=str, required=True, help='This field should be a year_kor')
        parser.add_argument('director_naver_kor', type=str, required=True, help='This field should be a director_naver_kor')
        parser.add_argument('actor_naver_kor', type=str, required=True, help='This field should be a actor_naver_kor')
        parser.add_argument('movie_l_rating', type=float, required=True, help='This field should be a movie_l_rating')
        parser.add_argument('movie_l_rating_count', type=int, required=True, help='This field should be a movie_l_rating_count')
        parser.add_argument('movie_l_popularity', type=float, required=True, help='This field should be a movie_l_popularity')
        parser.add_argument('link_naver', type=str, required=True, help='This field should be a link_naver')
        parser.add_argument('image_naver', type=str, required=True, help='This field should be a image_naver')         
        args = parser.parse_args()
        print(args)
        movies = RecoMovieDto(args['movieid'], \
                        args['title_kor'], \
                        args['title_naver_eng'], \
                        args['genres_kor'], \
                        args['keyword_kor'], \
                        args['running_time_kor'], \
                        args['year_kor'], \
                        args['director_naver_kor'], \
                        args['actor_naver_kor'], \
                        args['movie_l_rating'], \
                        args['movie_l_rating_count'], \
                        args['movie_l_popularity'], \
                        args['link_naver'], \
                        args['image_naver'])
        print('*********')
        print(f'{args}')
        try:
            RecoMovieDao.modify_movie(args)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured registering the movie'}, 500

class RecoMovies(Resource):
    @staticmethod
    def post():
        rmd = RecoMovieDao()
        rmd.bulk()

    @staticmethod
    def get():
        data = RecoMovieDao.find_all()
        print(data[0])
        return data, 200        

class RecoMovieDel(Resource):

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('movieid', type=str, required=True, help='This field should be a movieid')     
        args = parser.parse_args()
        print('*********')
        print(f'{args}')
        print('*********')
        movieid = args['movieid']
        print(movieid)

        try:
            RecoMovieDao.delete_movie(movieid)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured registering the movie'}, 500
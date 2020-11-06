from flask_restful import Resource, reqparse

from com_dayoung_api.cop.mov.model.movie_dao import MovieDao

class MovieSearch(Resource):
    def get(self, title):
        print("SEARCH 진입")
        print(f'타이틀 : {title}')
        movie = MovieDao.find_by_title(title)
        # review = {review[i]: review[i + 1] for i in range(0, len(review), 2)}
        # review = json.dump(review)
        movielist = []
        # for review in reviews:
            # reviewdic
        for rev in movie:
            movielist.append(rev.json())
        # print(f'Review type : {type(review[0])}')
        print(f'Review List : {movielist}')
        return movielist[:]    
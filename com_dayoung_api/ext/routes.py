import logging
from flask import Blueprint
from flask_restful import Api

from com_dayoung_api.usr.resource.user import User, Users, Delete
from com_dayoung_api.cop.act.resource.auth import Auth
from com_dayoung_api.usr.resource.access import Access

from com_dayoung_api.cop.act.resource.actor import Actor, Actors, AddActor

from com_dayoung_api.cop.mov.resource.movie import Movie, Movies, MovieDel
from com_dayoung_api.cop.mov.resource.search import MovieSearch

from com_dayoung_api.cop.rat.resource.rating import Rating, Ratings, RatingDel
from com_dayoung_api.cop.rat.resource.search import RatingSearch

############################## USER ##############################
user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')
auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')
############################## USER ##############################

############################## ACTOR ##############################
actor = Blueprint('actor', __name__, url_prefix='/api/actor')
actors = Blueprint('actors', __name__, url_prefix='/api/actors')
delete = Blueprint('delete', __name__, url_prefix='/api/delete')
addActor = Blueprint('addActor', __name__, url_prefix='/api/addActor')
############################## ACTOR ##############################

############################## MOVIE ##############################
movie = Blueprint('movie', __name__, url_prefix='/api/movie')
movies = Blueprint('movies', __name__, url_prefix='/api/movies')
moviesearch = Blueprint('moviesearch', __name__, url_prefix='/api/movie-search')
############################## MOVIE ##############################

############################## RATING ##############################
rating = Blueprint('rating', __name__, url_prefix='/api/rating')
ratings = Blueprint('ratings', __name__, url_prefix='/api/ratings')
rating_search = Blueprint('rating_search', __name__, url_prefix='/api/rating-search')
rating_del = Blueprint('rating_del', __name__, url_prefix='/api/rating-del')
############################## RATING ##############################


############################## USER ##############################
api = Api(user)
api = Api(users)
api = Api(auth)
api = Api(access)
############################## USER ##############################

############################## ACTOR ##############################
api = Api(actor)
api = Api(actors)
api = Api(delete)
api = Api(addActor)
############################## ACTOR ##############################

############################## MOVIE ##############################
api = Api(movie)
api = Api(movies)
api = Api(moviesearch)
############################## MOVIE ##############################

############################## RATING ##############################
api = Api(rating)
api = Api(ratings)
api = Api(rating_search)
api = Api(rating_del)
############################## RATING ##############################


def initialize_routes(api):
############################## USER ##############################
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Auth, '/api/auth')
    api.add_resource(Access, '/api/access')
############################## USER ##############################

############################## ACTOR ##############################
    api.add_resource(Actor, '/api/actor/<string:id>')
    api.add_resource(AddActor, '/api/addActor/<string:name>')
    api.add_resource(Delete, '/api/delete/<string:id>')
    api.add_resource(Actors, '/api/actors')    
############################## ACTOR ##############################

############################## MOVIE ##############################
    api.add_resource(Movie, '/api/movie')
    api.add_resource(Movies, '/api/movies')
    api.add_resource(MovieSearch, '/api/movie-search/<string:title>')
    api.add_resource(MovieDel, '/api/movie-del')
############################## MOVIE ##############################

############################## RATING ##############################
    api.add_resource(Rating, '/api/rating')
    api.add_resource(Ratings, '/api/ratings')
    api.add_resource(RatingSearch, '/api/rating-search/<string:ratingid>')
    api.add_resource(RatingDel, '/api/rating-del')
############################## RATING ##############################


import logging
from flask import Blueprint
from flask_restful import Api
from com_dayoung_api.usr.resource.user import User, Users, Delete
from com_dayoung_api.cop.act.resource.actor import Actor, Actors, AddActor
from com_dayoung_api.cop.act.resource.auth import Auth
from com_dayoung_api.usr.resource.access import Access
from com_dayoung_api.cop.mov.resource.movie import RecoMovie, RecoMovies, RecoMovieDel
from com_dayoung_api.cop.mov.resource.search import RecoMovieSearch
from com_dayoung_api.cop.rat.resource.rating import MovieRating, MovieRatings, MovieRatingDel
from com_dayoung_api.cop.rat.resource.search import MovieRatingSearch
from com_dayoung_api.cop.rev.resource.my_review import MyReview
from com_dayoung_api.cop.rev.resource.review import Review, Reviews
from com_dayoung_api.cop.rev.resource.score import Score
from com_dayoung_api.cop.rev.resource.search import Search


actor = Blueprint('actor', __name__, url_prefix='/api/actor')
actors = Blueprint('actors', __name__, url_prefix='/api/actors')
delete = Blueprint('delete', __name__, url_prefix='/api/delete')
addActor = Blueprint('addActor', __name__, url_prefix='/api/addActor')
user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')
auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')
movie_rating = Blueprint('movie_rating', __name__, url_prefix='/api/movie-rating')
movie_ratings = Blueprint('movie_ratings', __name__, url_prefix='/api/movie-ratings')
movie_rating_search = Blueprint('movie_rating_search', __name__, url_prefix='/api/movie-rating-search')
movie_rating_del = Blueprint('movie_rating_del', __name__, url_prefix='/api/movie-rating-del')
recomovie = Blueprint('recomovie', __name__, url_prefix='/api/recomovie')
recomovies = Blueprint('recomovies', __name__, url_prefix='/api/recomovies')
recomoviesearch = Blueprint('recomoviesearch', __name__, url_prefix='/api/recomoviesearch')
review = Blueprint('review', __name__, url_prefix='/api/review')
reviews = Blueprint('reviews', __name__, url_prefix='/api/reviews')
myreview = Blueprint('myreview', __name__, url_prefix='/api/myreview')
reviewscore = Blueprint('reviewscore', __name__, url_prefix='/api/reviewscore')
reviewsearch = Blueprint('reviewsearch', __name__, url_prefix='/api/reviewsearch')

# actor = Blueprint('actor', __name__, url_prefix='/api/actor')
# actors = Blueprint('actors', __name__, url_prefix='/api/actors')

api = Api(actor)
api = Api(actors)
api = Api(delete)
api = Api(addActor)
api = Api(user)
api = Api(users)
api = Api(auth)
api = Api(access)
api = Api(movie_rating)
api = Api(movie_ratings)
api = Api(movie_rating_search)
api = Api(movie_rating_del)
api = Api(recomovie)
api = Api(recomovies)
api = Api(recomoviesearch)
api = Api(review)
api = Api(reviews)
api = Api(myreview)
api = Api(reviewscore)
api = Api(reviewsearch)


def initialize_routes(api):
    print('========== 2 ==========')
    # api.add_resource(Home, '/api')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Auth, '/api/auth')
    api.add_resource(Access, '/api/access')
    api.add_resource(Actor, '/api/actor/<string:id>')
    api.add_resource(AddActor, '/api/addActor/<string:name>')
    api.add_resource(Delete, '/api/delete/<string:id>')
    api.add_resource(Actors, '/api/actors')
    api.add_resource(MovieRating, '/api/movie-rating')
    api.add_resource(MovieRatings, '/api/movie-ratings')
    api.add_resource(MovieRatingSearch, '/api/movie-rating-search/<string:ratingid>')
    api.add_resource(MovieRatingDel, '/api/movie-rating-del')
    api.add_resource(RecoMovie, '/api/recomovie')
    api.add_resource(RecoMovies, '/api/recomovies')
    api.add_resource(RecoMovieSearch, '/api/recomoviesearch/<string:title>')
    api.add_resource(RecoMovieDel, '/api/recomoviedel')
    api.add_resource(Review, '/api/review<string:id>')
    api.add_resource(Reviews, '/api/reviews')
    api.add_resource(MyReview, '/api/myreview<string:user_id>')
    api.add_resource(Score, '/api/reviewscore')
    api.add_resource(Search, '/api/reviewsearch<string:movie_title>')

def movie_rating_api_error(e):
    logging.exception('An error occurred during movie_rating request. %s' % str(e))
    return 'An internal error occurred.', 500

@recomovie.errorhandler(500)
def reco_movie_api_error(e):
    logging.exception('An error occurred during reco_movie request. %s' % str(e))
    return 'An internal error occurred.', 500
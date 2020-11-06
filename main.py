from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from com_dayoung_api.ext.db import url, db
from com_dayoung_api.ext.routes import initialize_routes
from com_dayoung_api.usr.model.user_dao import UserDao
from com_dayoung_api.cop.act.model.actor_dao import ActorDao
from com_dayoung_api.cop.rat.model.rating_dao import MovieRatingDao
from com_dayoung_api.cop.mov.model.movie_dao import RecoMovieDao
from com_dayoung_api.cop.rev.model.review_dao import ReviewDao

print('========== 1 ==========')
app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()
with app.app_context():
    print('데이터 DB 삽입')
    count_user = UserDao.count()
    count_actor = ActorDao.count()
    count_reco_movie = RecoMovieDao.count()
    count_movierating = MovieRatingDao.count()    
    count_review = ReviewDao.count()
    print(f'User Total Count is {count_user[0]}')
    print(f'Actor Total Count is {count_actor[0]}')
    print(f'Reco_Movies Total Count is {count_reco_movie[0]}')
    print(f'Movie Rating Total Count is {count_movierating[0]}')
    print(f'Review Total Count is {count_review}')
           
    if count_user[0] == 0:
        UserDao.bulk()
    
    if count_actor[0] == 0:
        ActorDao.bulk()
        
    if count_reco_movie[0] == 0:
        RecoMovieDao.bulk()

    if count_movierating[0] == 0:
        MovieRatingDao.bulk()

    if count_review == 0:
        ReviewDao.insert_many()
        
initialize_routes(api)
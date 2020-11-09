from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from com_dayoung_api.ext.db import url, db
from com_dayoung_api.ext.routes import initialize_routes

from com_dayoung_api.usr.model.user_dao import UserDao

from com_dayoung_api.cop.act.model.actor_dao import ActorDao

from com_dayoung_api.cop.mov.model.movie_dao import MovieDao

from com_dayoung_api.cop.rat.model.rating_dao import RatingDao

from com_dayoung_api.cop.rev.model.review_dao import ReviewDao

app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()
    
with app.app_context():
    print('***** 데이터 DB 삽입 *****')
    count_user = UserDao.count()    
    count_actor = ActorDao.count()
    count_movie = MovieDao.count()
    count_rating = RatingDao.count()    
    count_review = ReviewDao.count()

    print(f'USR TABLE COUNT : {count_user[0]:6}')
    print(f'ACT TABLE COUNT : {count_actor[0]:6}')
    print(f'MOV TABLE COUNT : {count_movie[0]:6}')
    print(f'RAT TABLE COUNT : {count_rating[0]:6}')
    print(f'REV TABLE COUNT : {count_review[0]:6}')
    
    if count_user[0] == 0:
        print('***** USR DATA INSERT *****')
        UserDao.bulk()

    if count_actor[0] == 0:
        print('***** ACT DATA INSERT *****')
        ActorDao.bulk()

    if count_movie[0] == 0:
        print('***** MOV DATA INSERT *****')
        MovieDao.bulk()

    if count_rating[0] == 0:
        print('***** RAT DATA INSERT *****')
        RatingDao.bulk()

    # if count_review[0] == 0:
    #     print('***** REV DATA INSERT *****')
    #     ReviewDao.insert_many()

print('********** INITIALIZE **********')
initialize_routes(api)
from com_dayoung_api.ext.db import db



class MovieRatingDto(db.Model):

    __tablename__ = 'movie_ratings'
    __table_args__ = {'mysql_collate':'utf8_general_ci'}

    # 'userid', 'movieid', 'rating'
    ratingid : int = db.Column(db.Integer, primary_key = True, index = True)
    userid : int = db.Column(db.Integer)
    movieid : int = db.Column(db.Integer)
    rating : float = db.Column(db.Float)



    def __init__(self,ratingid,userid,movieid,rating):
        self.ratingid = ratingid
        self.userid = userid
        self.movieid = movieid
        self.rating = rating

    def json(self):
        return {
            'ratingid' : self.ratingid,
            'userid' : self.userid,
            'movieid' : self.movieid,
            'rating' : self.rating
        }

class MovieRatingVo:
    ratingid: int = 0
    userid: int = 0
    movieid: int = 0
    rating: float = 0.0
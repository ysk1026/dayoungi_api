from com_dayoung_api.ext.db import db

from com_dayoung_api.usr.model.user_dto import UserDto
from com_dayoung_api.cop.mov.model.movie_dto import MovieDto

class RatingDto(db.Model):

    __tablename__ = 'ratings'
    __table_args__ = {'mysql_collate':'utf8_general_ci'}

    # 'userid', 'mov_id', 'rating'
    rat_id : int = db.Column(db.Integer, primary_key = True, index = True)
    usr_id : str = db.Column(db.String(30), db.ForeignKey(UserDto.usr_id))
    mov_id : int = db.Column(db.Integer, db.ForeignKey(MovieDto.mov_id))
    rating : float = db.Column(db.Float)



    def __init__(self,rat_id,usr_id,mov_id,rating):
        self.rat_id = rat_id
        self.usr_id = usr_id
        self.mov_id = mov_id
        self.rating = rating

    def json(self):
        return {
            'rat_id' : self.rat_id,
            'usr_id' : self.usr_id,
            'mov_id' : self.mov_id,
            'rating' : self.rating
        }

class RatingVo:
    rat_id: int = 0
    usr_id: str = ''
    mov_id: int = 0
    rating: float = 0.0
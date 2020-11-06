from flask_restful import Resource, reqparse
from flask import request
import json
from flask import jsonify
from com_dayoung_api.cop.rev.model.review_dao import ReviewDao

class MyReview(Resource):
    
    def get(self, user_id):
        print("마이 리뷰 찾기 진입!")
        print(f"User ID : {user_id}의 리뷰들를 불러오는 중 . . .")
        review = ReviewDao.find_review_by_user_id(user_id)
        # 여기서 이제 review를 제이슨화 시킨후 보내주면 됨
        reviewlist = []
        for rev in review:
            reviewlist.append(rev.json())
        print(f"{user_id}의 전체 리뷰: {reviewlist}")
        return reviewlist[:]
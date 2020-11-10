from flask_restful import Resource, reqparse
from flask import request
import json
from flask import jsonify
from com_dayoung_api.cop.rev.model.review_dto import ReviewDto
from com_dayoung_api.cop.rev.model.review_dao import ReviewDao
from com_dayoung_api.cop.rev.model.review_ai import ReviewAi

class ReviewEmotion(Resource):
    
    def get(self, content):
        print("감정 분석 진입!")
        print(f"리뷰 내용 : {content}")
        ai = ReviewAi()
        score = ai.predict_review(content)
        # score = round(score * 100)
        # if(score > 0.5):
        #     print(f"{review} ==> {round(score*100)}% 확률로 긍정 리뷰입니다.")
        # else:
        #     print(f"{review} ==> {round((1-score)*100)}% 확률로 부정 리뷰입니다.")
        return score
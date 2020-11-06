from flask_restful import Resource, reqparse
from flask import request
import json
from flask import jsonify
from com_dayoung_api.cop.rev.model.review_dto import ReviewDto
from com_dayoung_api.cop.rev.model.review_dao import ReviewDao

class Review(Resource):
    
    @staticmethod
    def post():
        print('진입')
        # service = ReviewService()
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type =str, required =False, help ='This field cannot be left blank')
        parser.add_argument('movie_id', type =int, required =False, help ='This field cannot be left blank')
        parser.add_argument('title', type =str, required =False, help ='This field cannot be left blank')
        parser.add_argument('content', type =str, required =False, help ='This field cannot be left blank')
        parser.add_argument('label', type =int, required =False, help ='This field cannot be left blank')

        args = parser.parse_args()

        # review = ReviewDto(args.title, args.content, 1, args.user_id, args.movie_id)
        review = ReviewDto(args.title, args.content, 1, "jason", args.movie_id)
        print('=======3======')
 
        # print(f'Rev id : {review.rev_id} / Movie_id :{review.movie_id}/\
        #     User_id: {review.user_id}/ Title: {review.title}/ Content: {review.content} / Label: {review.label}')
        # review = ReviewDao(args['title'], args['movie_id'], \
        #     args['user_id'], args['content'])
        try: 
            ReviewDao.save(review)
            return {'code' : 0, 'message' : 'SUCCESS'}, 200    
        except:
            return {'message': 'An error occured inserting the article'}, 500
    

    def get(self, id):
        print("진입 성공!")
        print(id)
        review = ReviewDao.find_by_id(id)
        print("Review 가져옴!")
        # print(f'리뷰 정보: \n {review}')
        # print(f'리뷰 타입 {type(review)}')
        # print(f'제이슨 변환 이후: {review.json()}')
        return review.json()
        # if review:
        #     return review.json()
        # return {'message' : 'Article not found'}, 404
    
    def put(self, id):
        print('PUT 진입')
        parser = reqparse.RequestParser()
        parser.add_argument('title', type =str, required =False, help ='This field cannot be left blank')
        parser.add_argument('content', type =str, required =False, help ='This field cannot be left blank')
        
        args = parser.parse_args()
        print(args)
        review = ReviewDao.find_by_id(id)
        review.title = args['title']
        review.content = args['content']
        # review = ReviewDto(args)
        # data = review.json()
        # return data
        print('리뷰', review)
        print('리뷰 타입', type(review))
        try: 
            ReviewDao.update(review, id)
            return {'code' : 0, 'message' : 'SUCCESS'}, 200    
        except:
            return {'message': 'An error occured inserting the article'}, 500
    
    def delete(self, rev_id):
        print('Delete 진입')
        review = ReviewDao.find_by_id(rev_id)
        print('리뷰 아이디', review.rev_id)
        print('전체 리뷰', review)
        print('리뷰 타입', type(review))
        try:
            ReviewDao.delete(review.rev_id)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured registering the movie'}, 500

class Reviews(Resource):
    def get(self):
        # return {'review' : list(map(lambda review: review.json(), ReviewDao.find_all()))}
        # return {'articles':[article.json() for article in ArticleDao.find_all()]}
  
        print('========== 10 ==========')
        data = ReviewDao.find_all()
        return data, 200
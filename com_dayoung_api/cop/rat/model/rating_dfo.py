import os
import sys
import urllib.request
import csv
import ast
import time
import pandas as pd
from pandas import DataFrame
from pathlib import Path

from com_dayoung_api.cmm.util.file_helper import FileReader, FileChecker

class RatingDfo:
    def __init__(self):
        self.fileReader = FileReader()  
        self.filechecker = FileChecker()
        self.path = os.path.abspath("")

    def hook(self):
        print('***** 무비 렌즈 UI용 DF가공 시작 *****')

        movie_lens_rating_df = self.read_movie_lens_rating_csv()
        arrange_movie_lens_rating_df = self.arrange_movie_lens_rating_df(movie_lens_rating_df)

        print('***** 무비 렌즈 UI용 DF가공 완료 *****')
        
        return arrange_movie_lens_rating_df

    def read_movie_lens_rating_csv(self):
        print('***** 무비렌즈 평점 데이터 읽기*****')
        path = os.path.abspath("")
        fname = '\com_dayoung_api\cop\\rat\model\data\\ratings_small.csv'
        # path = os.path.abspath("")
        # fname = '\data\movie_lens\\ratings_small.csv'
        movie_lens_meta_df = pd.read_csv(path + fname, encoding='utf-8')
        print('***** 무비렌즈 평점 데이터 읽기 완료*****')
        return movie_lens_meta_df

    def arrange_movie_lens_rating_df(self, movie_lens_keyword_df):
        print('***** 무비렌즈 레이팅 데이터 가공 *****')
        '''
        [original columns]
        'userId',
        'movieId',
        'rating',
        'timestamp'
        '''

        ##### 필요없는 column 삭제 #####
        drop_df = movie_lens_keyword_df.drop(['timestamp'], axis=1)
        ##### 필요없는 column 삭제 #####

        ##### 데이터 축소 #####
        '''
        userid : 70 번 까지 (10000 row)
        (원본 데이터 : 10만 건)
        '''
        reduction_df = drop_df[(drop_df['userId'] < 71)]
        ##### 데이터 축소 #####

        ##### ratingid column 추가 #####
        mylist = []
        for i in range(0, len(reduction_df['movieId'])):
            mylist.append(i)
        ratingid_column = pd.DataFrame(mylist, columns=['ratingid'])
        reduction_df = pd.concat([reduction_df, ratingid_column], axis=1)
        ##### ratingid column 추가 #####


        ##### column 정렬 및 이름 변경 #####
        column_sort_df = reduction_df[['ratingid', 'userId', 'movieId', 'rating']]

        mycolumns = {
            'ratingid':'ratingid',
            'userId':'userid',
            'movieId':'movieid',
            'rating':'rating'
        }

        sort_df = column_sort_df.rename(columns=mycolumns)
        ##### column 정렬 및 이름 변경 #####

        final_movie_lens_rating_df = sort_df
        print('***** 무비렌즈 레이팅 데이터 가공 완료 *****')
        return final_movie_lens_rating_df


if __name__ == "__main__":
    test = RatingDfo()
    test.hook()


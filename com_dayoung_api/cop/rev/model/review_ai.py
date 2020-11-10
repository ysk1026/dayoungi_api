import json
import os
from pprint import pprint
from konlpy.tag import Okt
from tensorflow.keras.models import load_model
import time
import datetime
import numpy as np
import tensorflow as tf
import nltk
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics

class ReviewAi(object):
    def __init__(self):
        self.okt = Okt()
        self.x_train = None
        self.y_train = None
        self.fname =  '/Users/youngseonkim/Documents/project_merge/api_master/com_dayoung_api/cop/rev/model/data'
        self.x_test = None
        self.y_test = None

    def create_docs(self):
        with open(self.fname + '/train_docs.json') as f:
            train_docs = json.load(f)
            
        with open(self.fname + '/test_docs.json') as f:
            test_docs = json.load(f)
        # print(train_docs[:10])
        return [train_docs, test_docs]

    @staticmethod
    def create_tokens(train_docs):
        tokens = [t for d in train_docs for t in d[0]]
        return tokens
        
    @staticmethod
    def create_nltk_text(tokens):
        return nltk.Text(tokens, name='NMSC')

    def tokenize(self, review):
        #형태소와 품사를 join
        return ['/'.join(t) for t in self.okt.pos(review, norm=True, stem=True)]
    
    @staticmethod
    def transfer_text_to_selected_words(text):
        selected_words = [f[0] for f in text.vocab().most_common(10000)]
        return selected_words

    def term_frequency(self, doc):
        ai = ReviewAi()
        docs = self.create_docs()
        train_docs = docs[0]
        tokens = ai.create_tokens(train_docs)
        text = ai.create_nltk_text(tokens)
        selected_words = self.transfer_text_to_selected_words(text)
        return [doc.count(word) for word in selected_words]
    
    def set_train(self):
        train_x = [self.term_frequency(d) for d, _ in train_docs]
        test_x = [self.term_frequency(d) for d, _ in test_docs]
        train_y = [c for _, c in train_docs]
        test_y = [c for _, c in test_docs]
        self.x_train = np.asarray(train_x).astype('float32')
        self.x_test = np.asarray(test_x).astype('float32')
        self.y_train = np.asarray(train_y).astype('float32')
        self.y_test = np.asarray(test_y).astype('float32')

        
    def model_save(self):

        FREQUENCY_COUNT = 10000;

        # 레이어 구성
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(FREQUENCY_COUNT,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # 학습 프로세스 설정
        model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.001),
            loss=tf.keras.losses.binary_crossentropy,
            metrics=[tf.keras.metrics.binary_accuracy]
            )
        model.fit(self.x_train, self.y_train, epochs=10, batch_size=512)

        model.save('another_model.h5')

    def model_load(self):
        loaded_model = load_model(self.fname + '/review_model.h5')
        return loaded_model

    def model_eval(self, model):
        result = model.evaluate(self.x_test, self.y_test)
        return result

    def predict_review(self, review):
        token = self.tokenize(review)
        tfq = self.term_frequency(token)
        data = np.expand_dims(np.asarray(tfq).astype('float32'), axis=0)
        loaded_model = self.model_load()
        score = float(loaded_model.predict(data))
        if(score > 0.5):
            print(f"{review} ==> {round(score*100)}% 확률로 긍정 리뷰입니다.")
        else:
            print(f"{review} ==> {round((1-score)*100)}% 확률로 부정 리뷰입니다.")
        
        return score

if __name__ == "__main__":
    ai = ReviewAi()
    docs = ai.create_docs()
    train_docs = docs[0]
    test_docs = docs[1]
    print(f'[ 훈련데이터 상위 10 Rows ] : {train_docs[:10]}')
    tokens = ai.create_tokens(train_docs)
    print(f'[ 전체 토큰의 개수 ] : {len(tokens)}')
    # docs = tokens
    # temp_tokens = ai.tokenize(train_docs)
    nltk_text =  ai.create_nltk_text(tokens)
    print(f'[ 중복을 제외한 토큰의 개수 ] {len(nltk_text.tokens)}')
    print(f'[ 출현 빈도가 높은 상위 토큰 10개 ] {nltk_text.vocab().most_common(10)}') 
    
    # 출현 빈도 높은 상위 10000개 토큰 분류
    selected_words = ai.transfer_text_to_selected_words(nltk_text)
    print(f'[ 출현 빈도가 높은 상위 토큰 100개 ] {selected_words[:100]}')
    
    
    # term_freq_count = ai.term_frequency(train_docs)
    # ai.set_train()
    # ai.model_save()
    # model = ai.model_load()
    # answer = ai.model_eval(model)
    # print(f'[ 모델 평가한 답 ] {answer}')
    # print(f'================= Practice Result ====================')
    ai.predict_review("재미 정말 없어요 갖다 버리세요")
    ai.predict_review("이건 개망한 영화인데;; 누가보냐")
    ai.predict_review("좋았어 이거 또 보러 온다")
    ai.predict_review("너무 예쁜데요 ㅠㅠ 최고에요")
    ai.predict_review("하하하 쩔었다~~")
    ai.predict_review("21세기 최고의 영화다 진짜!!")
    ai.predict_review("너무 재밌어요 ㅋㅋ 진짜 쩐다 쩔어")
    ai.predict_review("수업 가기 귀찮다...")
        
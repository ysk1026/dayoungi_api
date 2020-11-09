import json
import os
from pprint import pprint
from konlpy.tag import Okt
from tensorflow.keras.models import load_model
import time
import datetime

okt = Okt()
fname = '/Users/youngseonkim/Documents/project_merge/api_master/com_dayoung_api/cop/rev/model/data'
with open(fname + '/train_docs.json') as f:
    train_docs = json.load(f)
    
with open(fname + '/test_docs.json') as f:
    test_docs = json.load(f)

# print(train_docs[:10])

tokens = [t for d in train_docs for t in d[0]]
# print(len(tokens))

import nltk
text = nltk.Text(tokens, name='NMSC')

def tokenize(doc):
    #형태소와 품사를 join
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

# 전체 토큰의 개수
print(len(text.tokens))

# 중복을 제외한 토큰의 개수
print(len(set(text.tokens)))            

# 출현 빈도가 높은 상위 토큰 10개
pprint(text.vocab().most_common(10))

selected_words = [f[0] for f in text.vocab().most_common(10000)]

def term_frequency(doc):
    return [doc.count(word) for word in selected_words]
'''
Train X
'''


'''
Test_x
'''

test_x = [term_frequency(d) for d, _ in test_docs]

'''
Train y
'''

train_y = [c for _, c in train_docs]


'''
Test_y
'''
test_y = [c for _, c in test_docs]

import numpy as np

x_train = np.asarray(train_x).astype('float32')
x_test = np.asarray(test_x).astype('float32')

y_train = np.asarray(train_y).astype('float32')
y_test = np.asarray(test_y).astype('float32')

import tensorflow as tf
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
model.fit(x_train, y_train, epochs=10, batch_size=512)

model.save('another_model.h5')
loaded_model = load_model(fname + '/review_model.h5')

results = loaded_model.evaluate(x_test, y_test)

def predict_review(review):
    token = tokenize(review)
    tfq = term_frequency(token)
    data = np.expand_dims(np.asarray(tfq).astype('float32'), axis=0)
    score = float(loaded_model.predict(data))
    if(score > 0.5):
        print(f"{review} ==> {round(score*100)}% 확률로 긍정 리뷰입니다.")
    else:
        print(f"{review} ==> {round((1-score)*100)}% 확률로 부정 리뷰입니다.")

predict_review("재미 정말 없어요 갖다 버리세요")
predict_review("이건 개망한 영화인데;; 누가보냐")
predict_review("좋았어 이거 또 보러 온다")
predict_review("너무 예쁜데요 ㅠㅠ 최고에요")
predict_review("하하하 쩔었다~~")
predict_review("21세기 최고의 영화다 진짜!!")
predict_review("너무 재밌어요 ㅋㅋ 진짜 쩐다 쩔어")
predict_review("수업 가기 귀찮다...")

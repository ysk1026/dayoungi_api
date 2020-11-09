from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
# pip install sklearn
# conda install python-graphviz
import pydotplus  # pip install pydotplus
from IPython.core.display import Image
from IPython.display import display
# pip install Ipython
# conda install -c anaconda ipython
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn import metrics
from six import StringIO 
import os, sys
# PATH = r'C:/Program Files/Graphviz 2.44.1/bin'
# os.environ["PATH"] += os.pathsep+ PATH
class ActorAi:
    def __init__(self):
        ...

    def train_actors(self):
        df = self.bring_dfo() # shape: (340, 10)
        df = df[df['state'] == 1] # 현재 보이는 배우들만 확인
        # df = df.head()
        # print(df)
        #         age       name       real_name              religion         agency                 spouse    children        debut_year   gender  state
        #     0   50        이병헌      no real name           불교             BH엔터테인먼트          이민정      이준후(아들)    1991         m       1
        #     1   39        전지현      왕지현(王智賢)          no religion      문화창고               최준혁       2남            1997        f        1
        #     2   38        손예진      손언진                  no religion     엠에스팀엔터테인먼트     no spouse   no child       1999        f        1
        #     3   28        안소희      no real name           불교             BH엔터테인먼트          no spouse   no child       2004        f        1 
        #     4   39        강동원      no real name           무신론[1]        YG 엔터테인먼트         no spouse   no child       2003        m        1

        # print(df.columns.values.tolist())
        # ['age', 'name', 'real_name', 'religion', 'agency', 'spouse', 'children','debut_year', 'gender', 'state']

        # 총 9개의 column 이지만 8개의 질문만 하면 됨
        # 처음부터 state 는 1인걸 알고 있음
        # 1st Question: 남자 입니까?
        # 2nd Question: 자녀가 있습니까?
        # 3rd Question: 배우자가 있습니까?
        # 4th Question: 소속사가 관련 ->  
        # 5th Question: 종교 관련 -> 
        # 6th Question: 본명으로 활동 하나요?
        # 7th Question: 나이가 어떻게 됩니까?
        # 8th Question: 데뷔년도가 어떻게 됩니까?
        # x = df['age', 'real_name', 'religion', 'agency', 'spouse', 'children','debut_year', 'gender', 'state']
        # print(x)
        
        print("-----------------------------------")
        y_train = df.filter(["name"])  # 구할 것 Output
        X_train = df.filter(['act_id','age', 'real_name', 'religion', 'agency', 'spouse', 'children','debut_year', 'gender', 'state'])
        print("**************************************")
        print(y_train)
        print(X_train)
        
        y_test = y_train
        # 모르는 것을 예측 하는 것이 아니기 때문에 pred 에 train_set 과 같은 value
        # 예상 100퍼 맞춤

        
        print("-----------------------------------------------------------------------")
        for set_max_depth in range(1,15):
            set_random_state = 0
            clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth=set_max_depth, random_state=set_random_state)
            clf.fit(X_train,y_train)
            y_pred = clf.predict(X_train)

            print("Accuracy :", metrics.accuracy_score(y_test, y_pred))
            print("raondom state: ", set_random_state)
            print("Max Depth: ", set_max_depth)
            print("-----------------------------------------------------------------------")
            dot_data = StringIO()
            tree.export_graphviz(clf, out_file=dot_data)
            graph = pydotplus.graph_from_dot_data(dot_data.getvalue()) 
            Image(graph.write_png("max_depth{}.png".format(set_max_depth)))  # png file 생성
        # ---------------------------------------------------------------------------------------------
        # Actor ID 를 Drop 했을때
        # 총 9개의 컬럼이 있기 때문에 max_depth 가 9 개면 100퍼 가까이 나올거라 예상.
        # Accuracy : 0.9766763848396501
        # raondom state:  0
        # Max Depth:  9
        # 내 예상으로는 100프로 나올거라 생각했지만 나오지 않았음
        # 배우 수 = 343
        # 343 * 0.9766763848396501 = 335
        # 343 - 335 = 8명의 데이터가 겹치는 것을 알 수 있음! 

        # Actor ID 를 Drop "안" 했을 때
        # dot_data = StringIO(Accuracy : 1.0
        # raondom state:  0
        # Max Depth:  9

        # ----------------------------------------------------------------------
        # 하지만 Actor ID 는 유저는 모르기 때문에 아무 의미 없음.
        # 실제 이용할 데이터셋은 Drop Actor ID

    def bring_dfo(self):
        df = pd.read_csv("./data/actors2.csv")
        #  print(df.shape)  #  (340, 13) 13개중 두개의 컬럼은 actor_id 와 photo url 이기 때문에 필요 없음), 그래서 두개를 drop 하겠음
        #  더해서 index 도 필요 없으니 삭제 하겠음
        #   print(df.columns)
        #   Index(['Unnamed: 0', 'photo_url', 'age', 'act_id', 'name', 'real_name',
        #          'religion', 'agency', 'spouse', 'children', 'debut_year', 'gender',
        #          'state'], dtype='object')

        df = df.drop('photo_url',1)  # 0 means to drop rows, 1 means drop columns
        df = df.drop('act_id',1) 
        # print(df.shape) #  (340, 10)
        return df

if __name__ == "__main__":
    ai = ActorAi()
    # df = pd.read_csv("./data/actors2.csv")
    # df = df.drop('photo_url',1)  # 0 means to drop rows, 1 means drop columns
    # df = df.drop('act_id',1) 
    # df = df[df['state'] == 1]
    # print(df)
    ai.train_actors()
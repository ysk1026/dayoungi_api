
import os
import pandas as pd
import numpy as np
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import Reader, Dataset, SVD, accuracy

import warnings; warnings.simplefilter('ignore')


# path = os.path.abspath("")
# fname = '\data\movie_lens\movies_metadata.csv'
# in 2
path = os.path.abspath('')
fname = '\data\movies_metadata.csv'
md = pd.read_csv(path + fname, encoding='utf-8')
# print(md.head())

# in 3
print('////////////////////// Before ////////////////////// \n', md['genres'].head(), '\n////////////////////// Before //////////////////////')

# dictionary안에 담겨있는 Genre 정보를 List 형태로 세팅
# 1. md['genres'].fillna('[]') : genres 컬럼에 null 값을 '[](빈 리스트 값)'으로 채워넣음
# 2. apply(literal_eval) : literal_eval를 사용하여 String으로 되어있는 값을 List & Dictionary로 사용할 수 있게 변환
# 3. apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else []) : x가 list인 경우 안에 들어있는 dictionary 중 name에 해당하는 값을 list에 담음
md['genres'] = md['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

print('////////////////////// After ////////////////////// \n', md['genres'].head(), '\n////////////////////// After //////////////////////')

# in4
# print('vote ::: \n', md[['vote_count', 'vote_average']].head())
vote_counts = md[md['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages = md[md['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()
# print(C)

# in5
# 총 45460개의 영화 중 상위 5%는 2273번째
# print(vote_counts.sort_values(ascending=False)[2273:2274])

# quantile는 데이터를 크기대로 정렬하였을 때 분위수를 구하는 함수. quantile(0.95)는 상위 5%에 해당하는 값을 찾는 것
m = vote_counts.quantile(0.95)
# print(m)

# in 6
# print('release_date ::: \n', md['release_date'].head())

# pd.to_datetime
# errors : {‘ignore’, ‘raise’, ‘coerce’}, default ‘raise’
# If ‘raise’, then invalid parsing will raise an exception
# If ‘coerce’, then invalid parsing will be set as NaT
# If ‘ignore’, then invalid parsing will return the input

# 'release_date'를 split해서 year만 추출
md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

# print('year ::: \n', md['year'].head())

# in 7
# 평가 수가 상위 5%인(434보다 큰) 데이터 추출
qualified = md[(md['vote_count'] >= m) & (md['vote_count'].notnull()) & (md['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
qualified['vote_count'] = qualified['vote_count'].astype('int')
qualified['vote_average'] = qualified['vote_average'].astype('int')
# print(qualified.shape)

# in 8
def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

# in 9
x = qualified
qualified['wr'] = qualified.apply(weighted_rating, axis=1)

# in 10
# Weighted Rating 상위 250개의 영화 
qualified = qualified.sort_values('wr', ascending=False).head(250)

# in 11
# print(qualified.head(15))

# in 12
# stack() : stack이 (위에서 아래로 길게, 높게) 쌓는 것이면, unstack은 쌓은 것을 옆으로 늘어놓는것(왼쪽에서 오른쪽으로 넓게) 라고 연상이 될 것
# reset_index() : 기존의 행 인덱스를 제거하고 인덱스를 데이터 열로 추가
s = md.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
s.name = 'genre'
# print(s.head(10))

gen_md = md.drop('genres', axis=1).join(s)
# print(gen_md.head(10))

# in 13

def build_chart(genre, percentile=0.85):
    df = gen_md[gen_md['genre'] == genre]
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)
    
    qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][['title','year','vote_count','vote_average','popularity']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    
    qualified['wr'] = qualified.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(250)
    
    return qualified

# print(qualified.head(15))

# in 14
build_chart('Romance').head(15)
# print(build_chart('Romance').head(15))

# in 15
path = os.path.abspath('')
fname = '\data\links_small.csv'
links_small = pd.read_csv(path + fname, encoding='utf-8')
links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')
links_small.head()
# print(links_small.head())

# in 16
# Drop a row by index : 19730, 29503, 33587 행은 이상한 데이터들(md.iloc[19730], md.iloc[29503], md.iloc[33587])
md = md.drop([19730, 29503, 35587])

# in 17
#Check EDA Notebook for how and why I got these indices.
md['id'] = md['id'].astype('int')

# in 18
smd = md[md['id'].isin(links_small)]
smd.shape
# print(smd.shape)

# in 19
smd = md[md['id'].isin(links_small)]
# print(smd.shape)

# in 20
smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'] = smd['description'].fillna('')

smd['description'].head()
# print(smd['description'].head())

# in 21
# n-그램:단어장 생성에 사용할 토큰의 크기를 결정한다. 모노그램(1-그램)은 토큰 하나만 단어로 사용하며 바이그램(2-그램)은 두 개의 연결된 토큰을 하나의 단어로 사용한다.
# Stop Words:문서에서 단어장을 생성할 때 무시할 수 있는 단어를 말한다. 보통 영어의 관사나 접속사, 한국어의 조사 등이 여기에 해당한다. stop_words 인수로 조절할 수 있다.
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])

# in 22
# print(tfidf_matrix[10])

# in 23
tfidf_matrix.shape
# print(tfidf_matrix.shape)

# in 24
# linear_kernel는 두 벡터의 dot product 이다.
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# in 25
cosine_sim[0]
# print(cosine_sim[0])

# in 26
smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])

# print(titles.head(), indices.head())

# in 27

def get_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

# in 28
# get_recommendations('The Godfather').head(10)
# print(get_recommendations('The Godfather').head(10))

# in 29
# get_recommendations('Inception').head(10)
# print(get_recommendations('Inception').head(10))

# in 30
path = os.path.abspath('')
fname = '\data\credits.csv'
credits = pd.read_csv(path + fname, encoding='utf-8')
fname = '\data\keywords.csv'
keywords = pd.read_csv(path + fname, encoding='utf-8')

# in 31
credits['crew'][0]
# print(credits['crew'][0])

# in 32
keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')
md['id'] = md['id'].astype('int')

# in 33
md.shape
# print(md.shape)

# in 34
md = md.merge(credits, on='id')
md = md.merge(keywords, on='id')

# in 35
smd = md[md['id'].isin(links_small)]
smd.shape
# print(smd.shape)

# in 36
smd['cast'] = smd['cast'].apply(literal_eval)
smd['crew'] = smd['crew'].apply(literal_eval)
smd['keywords'] = smd['keywords'].apply(literal_eval)
smd['cast_size'] = smd['cast'].apply(lambda x: len(x))
smd['crew_size'] = smd['crew'].apply(lambda x: len(x))

# in 37

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# in 38
smd['director'] = smd['crew'].apply(get_director)

# in 39
# 출연진 중 상위에 노출되는 3명만 추출
smd['cast'] = smd['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
smd['cast'] = smd['cast'].apply(lambda x: x[:3] if len(x) >= 3 else x)

# in 40
smd['keywords'] = smd['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

# in 41
# 출연진의 이름에서 공백 삭제
smd['cast'] = smd['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])

# in 42
# 감독의 이름에서 공백 삭제 및 3번 언급?
smd['director'] = smd['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
smd['director'] = smd['director'].apply(lambda x: [x, x, x])

# in 43
s = smd.apply(lambda x: pd.Series(x['keywords']), axis=1).stack().reset_index(level=1, drop=True)
s.name = 'keyword'

# in 44
s = s.value_counts()
s[:5]
# print(s[:5])

# in 45
# 2번 이상 등장한 키워드만 추출
s = s[s > 1]

# in 46
# 어근 추출을 통해 동일 의미&다른 형태의 단어(dogs&dog, imaging&image 등)를 동일한 단어로 인식
stemmer = SnowballStemmer('english')
# print("dogs의 어근 : ", stemmer.stem('dogs'))
# print("dog의 어근 : ", stemmer.stem('dog'))

# in 47

def filter_keywords(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words

# in 48
# 키워드의 어근을 찾아서 공백 제거 후 세팅
smd['keywords'] = smd['keywords'].apply(filter_keywords)
smd['keywords'] = smd['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
smd['keywords'] = smd['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])

# in 49
smd['soup'] = smd['keywords'] + smd['cast'] + smd['director'] + smd['genres']
smd['soup'] = smd['soup'].apply(lambda x: ' '.join(x))

# in 50
count = CountVectorizer(analyzer='word', ngram_range=(1,2), min_df=0, stop_words='english')
count_matrix = count.fit_transform(smd['soup'])

# in 51
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# in 52
smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])

# in 53
# get_recommendations('The Dark Knight').head(10)
# print(get_recommendations('The Dark Knight').head(10))

# in 54
# get_recommendations('Mean Girls').head(10)
# print(get_recommendations('Mean Girls').head(10))

# in 55

def improved_recommendations(title):
    print(title)
    idx = indices[title]
    print(idx)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    print(movie_indices)

    movies = smd.iloc[movie_indices][['title','vote_count','vote_average','year']]
#     print(movies)
    
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)
    qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull())]
#     print(qualified)
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10)
    # print(qualified)
    return qualified

# in 56
# improved_recommendations('The Dark Knight')
# print(improved_recommendations('The Dark Knight'))

# in 57
# improved_recommendations('Mean Girls')
# print(improved_recommendations('Mean Girls'))

# in 58
# surprise 라이브러리의 Reader
reader = Reader()

# in 59
path = os.path.abspath('')
fname = '\data\\ratings_small.csv'
ratings = pd.read_csv(path + fname, encoding='utf-8')

# in 60
data = Dataset.load_from_df(ratings[['userId', 'movieId','rating']], reader)
# data.split(n_folds=5)

trainset = data.build_full_trainset()
testset = trainset.build_testset()

# in 61
svd = SVD()
# evaluate(svd, data, measures=['RMSE', 'MAE'])

####### 기존 커널대로 진행하면 오류나서 수정 #######
svd.fit(trainset)
predictions = svd.test(testset)
accuracy.rmse(predictions)
# print(accuracy.rmse(predictions))

# in 62
ratings[ratings['userId'] == 1]

# in 63
svd.predict(1, 302, 3)
# print(svd.predict(1, 302, 3))

# in 64

def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan

# in 65
path = os.path.abspath('')
fname = '\data\links_small.csv'
id_map = pd.read_csv(path + fname, encoding='utf-8')[['movieId', 'tmdbId']]
id_map['tmdbId'] = id_map['tmdbId'].apply(convert_int)
id_map.columns = ['movieId', 'id']
id_map = id_map.merge(smd[['title', 'id']], on='id').set_index('title')

# in 66
indices_map = id_map.set_index('id')

# in 67

def hybrid(userId, title):
    idx = indices[title]
    tmdbId = id_map.loc[title]['id']
    movie_id = id_map.loc[title]['movieId']
    
    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    
    movies = smd.iloc[movie_indices][['title','vote_count','vote_average','year','id']]
    movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, indices_map.loc[x]['movieId']).est)
    movies = movies.sort_values('est', ascending=False)
    return movies.head(10)

# in 68
# hybrid(1, 'Avatar')
# print(hybrid(1, 'Avatar'))

# in 69
# hybrid(500, 'Avatar')
print(hybrid(500, 'Avatar'))
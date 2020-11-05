Session = openSession()
session = Session()

class RecoMovieDao(RecoMovieDto):
    
    @staticmethod
    def bulk():
        print('***** [movies_recommendation] df 삽입 *****')
        recomoviedf = RecoMovieDf()
        df = recomoviedf.hook()
        print(df)
        session.bulk_insert_mappings(RecoMovieDto, df.to_dict(orient='records'))
        session.commit()
        session.close()
        print('***** [movies_recommendation] df 삽입 완료 *****')

    @staticmethod
    def count():
        return session.query(func.count(RecoMovieDto.movieid)).one()
    
    @classmethod
    def find_by_title(cls, title):
        print('##### find title #####')
        return session.query(RecoMovieDto).filter(RecoMovieDto.title_kor.like(title)).all()
    
    @classmethod
    def find_by_id(cls, movieid):
        print('##### find title #####')
        return session.query(RecoMovieDto).filter(RecoMovieDto.movieid.like(f'{movieid}')).one()

    @classmethod
    def find_all(cls):
        print('***** find all movie_reco *****')
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

# movieid,movie_l_title,movie_l_org_title,movie_l_genres,movie_l_year,movie_l_rating,movie_l_rating_count
    @staticmethod
    def register_movie(movie):
        print('##### new movie data registering #####')
        print(movie)
        newMovie = RecoMovieDao(movieid = movie['movieid'],
                            title_kor = movie['title_kor'],
                            title_naver_eng = movie['title_naver_eng'],
                            genres_kor = movie['genres_kor'],
                            keyword_kor = movie['keyword_kor'],
                            running_time_kor = movie['running_time_kor'],
                            year_kor = movie['year_kor'],
                            director_naver_kor = movie['director_naver_kor'],
                            actor_naver_kor = movie['actor_naver_kor'],
                            movie_l_rating = movie['movie_l_rating'],
                            movie_l_rating_count = movie['movie_l_rating_count'],
                            movie_l_popularity = movie['movie_l_popularity'],
                            link_naver = movie['link_naver'],
                            image_naver = movie['image_naver'])
        session.add(newMovie)
        session.commit()
        session.close()
        print('##### new movie data register complete #####')

    @staticmethod
    def modify_movie(movie):
        print('##### movie data modify #####')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        session.query(RecoMovieDto).filter(RecoMovieDto.movieid == movie['movieid']).update({RecoMovieDto.title_kor:movie['title_kor'],
                                                                                    RecoMovieDto.title_naver_eng:movie['title_naver_eng'],
                                                                                    RecoMovieDto.genres_kor:movie['genres_kor'],
                                                                                    RecoMovieDto.keyword_kor:movie['keyword_kor'],
                                                                                    RecoMovieDto.running_time_kor:movie['running_time_kor'],
                                                                                    RecoMovieDto.year_kor:movie['year_kor'],
                                                                                    RecoMovieDto.director_naver_kor:movie['director_naver_kor'],
                                                                                    RecoMovieDto.actor_naver_kor:movie['actor_naver_kor'],
                                                                                    RecoMovieDto.movie_l_rating:movie['movie_l_rating'],
                                                                                    RecoMovieDto.movie_l_rating_count:movie['movie_l_rating_count'],
                                                                                    RecoMovieDto.movie_l_popularity:movie['movie_l_popularity'],
                                                                                    RecoMovieDto.link_naver:movie['link_naver'],
                                                                                    RecoMovieDto.image_naver:movie['image_naver']})                                                        
        session.commit()
        session.close()
        print('##### movie data modify complete #####')

    @classmethod
    def delete_movie(cls,movieid):
        print('##### movie data delete #####')
        data = cls.query.get(movieid)
        db.session.delete(data)
        print('##### movie data delete complete #####')
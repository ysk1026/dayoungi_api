import json
import pandas as pd
from sqlalchemy import func

from com_dayoung_api.ext.db import db, openSession
from com_dayoung_api.cop.act.model.actor_kdd import Crawling
from com_dayoung_api.cop.act.model.actor_dto import ActorDto
from com_dayoung_api.cop.act.model.actor_dfo import ActorDfo

Session = openSession()
session = Session()
actor_preprocess = Crawling()

class ActorDao(ActorDto):
    @staticmethod
    def add(actor_name):
        crawl = Crawling(actor_name)
        df = crawl.crawl()
        actor = df.to_dict(orient="records")
        actor = actor[0]
        actor = ActorDto(**actor)
        Session = openSession()
        session = Session()
        print("---------------------------------------------")
        db.session.add(actor)
        db.session.commit()
        session.close()

    def bulk():
        df = actor_preprocess.crawl()
        print(df.head())
        session.bulk_insert_mappings(ActorDto, df.to_dict(orient="records"))
        session.commit()
        session.close()

    @staticmethod
    def count():
        return session.query(func.count(ActorDto.act_id)).one()

    @staticmethod
    def save(actor):
        db.session.add(actor)
        db.session.commit()

    @staticmethod
    def update(actor):
        db.session.add(actor)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        # this deletes actor from the whole database
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()
        session.close()

    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @classmethod
    def find_state_one(cls):
        return session.query(ActorDto).filter(ActorDto.state.like("1")).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filer_by(name == name)

    @classmethod
    def find_by_id(cls, act_id):
        return session.query(ActorDto).filter(ActorDto.act_id.like(f'{act_id}')).one()

    @classmethod
    def find_id_by_name(cls, name):
        # 여기 나중에 조금 고쳐야 할 함
        actor = session.query(ActorDto).filter(ActorDto.name.like(f'{name}')).one()
        print(actor.act_id)
        return actor.act_id

    @classmethod
    def delete_actor_by_setting_state_to_one(cls, id):
        # This does not delete the Actor from the database but rather
        # simply updates actor column "state" to 0 which will hide its
        # display from the user where as user will think that the
        # selected actor has been deleted
        session.query(ActorDto).filter(ActorDto.act_id == id).update({ActorDto.state: "0"}, synchronize_session=False)
        session.commit()
        session.close()

    @classmethod
    def add_actor_by_setting_state_to_one(cls, id):
        session.query(ActorDto).filter(ActorDto.act_id == id).update({ActorDto.state: "1"}, synchronize_session=False)
        session.commit()
        session.close()


if __name__ == "__main__":
    ActorDao.bulk()
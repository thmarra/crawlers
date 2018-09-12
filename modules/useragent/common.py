from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
from settings import useragent as conf
import random


class Common(object):
    url = None
    limit = 500
    db_enabled = True

    def __str__(self):
        return self.url

    def get_data(self):
        return []

    def update_database(self):
        if not self.db_enabled:
            return False

        new_data = self.get_data()
        # Add data to database
        db = Common._connect_mongo()
        # 1. Delete all that are currently set
        db.useragents.remove({})
        # 2. Insert new values
        db.useragents.insert_many(new_data)
        return True

    def random(self, as_json=True, **kwargs):
        if self.db_enabled:
            db = Common._connect_mongo()
            filters = {}

            if kwargs is not None:
                for key, value in kwargs.items():
                    if(key is '_id'):
                        filters.update({key: ObjectId(value)})
                    else:
                        filters.update({key: value})

            colection = db.useragents.find(filters)
            data = []
            for item in colection:
                data.append(item)
        else:
            data = self.get_data()

        if not len(data):
            return None

        opt = random.choice(data)

        if as_json:
            return dumps(opt)

        return "\"user-agent\": \"{}\"".format(opt['agent'])

    @staticmethod
    def _connect_mongo():
        try:
            client = MongoClient(
                host=conf.MONGO_HOST,
                port=int(conf.MONGO_PORT),
                # username=conf.MONGO_USER,
                # password=conf.MONGO_PASS,
                # authSource=conf.MONGO_AUTHSOURCE,
            )
            return client.browser_useragent
        except Exception as e:
            print(e)

import pymongo
from anthropod.core import settings, _configure_db


settings.MONGO_DATABASE += '_test'
settings.MONGO_USER_DATABASE += '_test'
_configure_db(settings.MONGO_HOST, settings.MONGO_PORT,
              settings.MONGO_DATABASE, settings.MONGO_USER_DATABASE)


def teardown():
    host = settings.MONGO_HOST
    port = settings.MONGO_PORT
    db_name = settings.MONGO_DATABASE

    assert db_name.endswith('_test')

    pymongo.MongoClient(host, port).drop_database(db_name)

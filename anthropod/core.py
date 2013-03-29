import pymongo

from django.conf import settings


class ErrorProxy(object):
    def __init__(self, error):
        self.error = error

    def __getattr__(self, attr):
        raise self.error


db = None


def _configure_db(host, port, db_name):
    global db
    try:
        conn = pymongo.MongoClient(host, port)
        db = conn[db_name]
    # return a dummy NoDB object if we couldn't connect
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ConnectionFailure) as e:
        db = ErrorProxy(e)
    return db


_configure_db(settings.MONGO_HOST,
              settings.MONGO_PORT,
              settings.MONGO_DATABASE)

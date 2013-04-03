import pymongo
from pymongo.son_manipulator import SONManipulator

from django.conf import settings


class ErrorProxy(object):
    def __init__(self, error):
        self.error = error

    def __getattr__(self, attr):
        raise self.error


db = None
_model_registry = {}
_model_registry_by_collection = {}


def _configure_db(host, port, db_name):

    global db

    class Transformer(SONManipulator):

        def transform_outgoing(
                self, son, collection,
                mapping=_model_registry_by_collection):

            try:
                return mapping[collection.name](son)
            except KeyError:
                return son

    try:
        conn = pymongo.MongoClient(host, port)
        db = conn[db_name]
        db.add_son_manipulator(Transformer())
    # return a dummy NoDB object if we couldn't connect
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ConnectionFailure) as e:
        db = ErrorProxy(e)
    return db


_configure_db(settings.MONGO_HOST,
              settings.MONGO_PORT,
              settings.MONGO_DATABASE)


from .models import *
from .collect.models import *

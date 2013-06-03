import uuid

from bson.objectid import ObjectId, InvalidId


def generate_id(type_):
    return 'ocd-%s/%s' % (type_, uuid.uuid1())

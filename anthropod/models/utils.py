from bson.objectid import ObjectId, InvalidId


def get_id(_id):
    '''Try to return an objectid. Should go away when we use mongo ids
    and store openstates ids under 'openstates_id'.
    '''
    try:
        return ObjectId(_id)
    except InvalidId:
        return _id

import json

from bson.objectid import ObjectId

from anthropod.core import _model_registry, _model_registry_by_collection


class ModelMeta(type):

    def __new__(meta, name, bases, attrs):
        cls = type.__new__(meta, name, bases, attrs)
        if name != 'ModelBase':
            _model_registry[name] = cls
            _model_registry_by_collection[cls.collection.name] = cls
        return cls


class ModelBase(dict):
    __metaclass__ = ModelMeta

    class DoesNotExist(Exception):
        pass

    @property
    def id(self):
        '''Return the object's mongo ID as bson.objectid.ObjectId instance.
        '''
        return self['_id']

    @property
    def id_string(self):
        '''Return the object's mongo ID as string.
        '''
        return str(self['_id'])

    def pretty_print(self):
        return json.dumps(self, cls=_PrettyPrintEncoder, indent=4,
                          sort_keys=True)


class _PrettyPrintEncoder(json.JSONEncoder):
    '''And encoder that stringifies bson.objectid.ObjectId instances.
    '''
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(_PrettyPrintEncoder, self).default(obj, **kwargs)

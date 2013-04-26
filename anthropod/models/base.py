import json

from bson.objectid import ObjectId

from anthropod.core import _model_registry, _model_registry_by_collection
from anthropod.models.utils import get_id


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

    def pretty_print(self):
        return json.dumps(self, cls=_PrettyPrintEncoder, indent=4,
                          sort_keys=True)

    @classmethod
    def find_one(cls, *args, **kwargs):
        '''Find one; raise DoesNotExist if not found.
        '''
        obj = cls.collection.find_one(*args, **kwargs)
        if obj is None:
            msg = 'No %s found for %r' % (cls.__name__, (args, kwargs))
            raise cls.DoesNotExist(msg)
        return obj

    @classmethod
    def find(cls, *args, **kwargs):
        objs = cls.collection.find(*args, **kwargs)
        if objs is None:
            msg = 'No orgnizations found for %r.' % ((args, kwargs),)
            raise cls.DoesNotExist(msg)
        return objs


class _PrettyPrintEncoder(json.JSONEncoder):
    '''And encoder that stringifies bson.objectid.ObjectId instances.
    '''
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(_PrettyPrintEncoder, self).default(obj, **kwargs)

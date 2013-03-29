

class Base(dict):
    def id(self):
        return self['_id']


class Person(Base):
    '''A model class to wrap person objects from mongo.
    '''


class Organization(Base):
    '''A model class to wrap organization objects from mongo.
    '''

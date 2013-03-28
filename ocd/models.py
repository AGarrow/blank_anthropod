

class Person(dict):
    '''A model class to wrap person objects from mongo.
    '''
    def id(self):
        return self['_id']

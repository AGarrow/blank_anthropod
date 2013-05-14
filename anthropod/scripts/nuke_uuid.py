from anthropod.core import db

for person in db.people.find():
    if 'uuid' in person:
        del person['uuid']
        db.people.save(person)

# from anthropod.core import db

# for person in db.people.find():
#     if 'uuid' in person:
#         del person['uuid']
#         db.people.save(person)

mongo ocd --eval "db.people.update({}, {$unset: {uuid: 1}}, false, true)"

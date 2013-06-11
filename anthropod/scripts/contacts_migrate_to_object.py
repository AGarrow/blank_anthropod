'''Migrate contact info from a list of 3-tuples to objects.
'''
from anthropod.core import db


def migrate_contacts(thing):
    contacts = thing['contact_details']
    fieldnames = ('type', 'value', 'note')
    contacts = [dict(zip(fieldnames, tpl)) for tpl in contacts]
    thing['contact_details'] = contacts
    return thing

for obj in db.people.find():
    db.people.save(migrate_contacts(obj))

for obj in db.organizations.find():
    db.people.save(migrate_contacts(obj))

for obj in db.memberships.find():
    db.people.save(migrate_contacts(obj))


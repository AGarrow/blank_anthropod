'''Deletes memberships whose person_id or organization_id isn't
a valid id for an existing person or org. We have some of those ids
present due to anthropod not previously deleting related memberships
if a person or org is deleted (fixed by ef74b92).
'''
from anthropod.core import db


person_ids = db.people.distinct('_id')
org_ids = db.organizations.distinct('_id')

spec = {
    '$or': [
        {'person_id': {'$nin': person_ids}},
        {'organization_id': {'$nin': org_ids}},
        ]
    }

membs = db.memberships.find(spec)
count = membs.count()
if count:
    print 'Found %d memberships with invalid ids.' % count
    yesno = raw_input('Delete them? (y/n): ')
    if yesno in 'Yy':
        db.memberships.remove(spec)
else:
    'Found no memberships with invalid ids.'

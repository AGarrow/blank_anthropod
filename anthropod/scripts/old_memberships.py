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

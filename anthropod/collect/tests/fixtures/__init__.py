'''This module loads data used by the tests.
'''
import os
import json
from os.path import join

from anthropod.core import db, user_db
from anthropod.utils import cd


def load_test_fixtures():
    # Load test users. Make user1 admin.
    user_db.profiles.save(dict(_id='user1', is_admin=True))

    # User2 has the full suite of permissions on the sole org and
    # person in the database but is not admin.
    user_db.permissions.save({
        u'ocd_id': "ocd-organization/1bfc9aac-b29b-11e2-9e8b-12313d2facc4",
        u'permissions': [
            'organizations.delete',
            'organizations.edit',
            ],
        u'username': u'user2'})
    user_db.permissions.save({
        'ocd_id': None,
        'permissions': ['organizations.create'],
        'username': 'user2',
        })

    # User 3 has no permissions at all and is not admin.
    pass

    # Load test data.
    fixtures = join('anthropod', 'collect', 'tests', 'fixtures')
    collections = {
        'organization': db.organizations,
        'person': db.people,
        }

    for folder, _, filenames in os.walk(fixtures):
        with cd(folder):
            for filename in filenames:
                if not filename.endswith('.json'):
                    continue
                if filename == 'test_auth.json':
                    continue
                with open(filename) as f:
                    data = json.load(f)
                    _type = data.get('_type')
                    collection = collections.get(_type, db.memberships)
                    collection.save(data)

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

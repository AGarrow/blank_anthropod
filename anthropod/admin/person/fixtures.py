import json

from anthropod.core import db


def load():

    orgs = db.organizations.find()
    if orgs.count() == 0:
        raise Exception('The organization fixtures need to be loaded before '
                        'the person fixtures.')

    person = json.loads('''
    {
    "addresses": [
        ["voice", "1-234-567-8901", "work"],
        ["tollfree", "1-800-555-5555", "home"],
        ["address", "123 Dupont Circle", "Work"]
    ],
    "links": [
        {
            "note": "Twitter",
            "url": "http://twitter.com/twneale"
        },
        {
            "note": "Facebook",
            "url": "http://facebook.com/thom"
        }
    ],
    "other_names": [
        {
            "note": "first",
            "name": "Thommy"
        },
        {
            "note": "last",
            "name": "O'Neil"
        }
    ],
    "source_url": "http://www.thomneale.com",
    "geography_id": "ocd:location:country-us:state-texas:city-plano",
    "position": "Nerd",
    "name": "Thom Neale"
    }''')

    org = next(orgs)
    person['organization_id'] = org['_id']
    db.people.insert(person)

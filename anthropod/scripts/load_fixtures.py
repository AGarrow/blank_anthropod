import sys
import json
from anthropod.core import db

def people()
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

def organizations():
    db.organizations.insert(json.loads('''
    {
        "name": "Boise City Council",
        "geography_id": "ocd:location:country-us:state-idaho:city-boise",
        "source_url": "http://mayor.cityofboise.org/city-council/"
    }'''))

def main():
    fixture_modules = sys.argv[1:] or ['organization', 'person']

    usage = ('usage: python ./scripts/load_fixtures.py '
             '[fixture_module1[, fixture_modeul2]...]')
    if not fixture_modules:
        print usage

    funcs = {'organization': organizations, 'person': people}

    for fixture_module in fixture_modules:
        print 'loaded fixtures for %r' % fixture_module
        funcs[fixture_modules]()


if __name__ == '__main__':
    main()

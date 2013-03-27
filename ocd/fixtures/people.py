import json

from ocd.core import db


def load():
    db.people.insert(json.loads('''
         {
    "addresses": [
        {
            "voice": "1-234-567-8901",
            "type": "work"
        },
        {
            "type": "home",
            "tollfree": "1-800-555-5555"
        },
        {
            "type": "Work",
            "address": "123 Dupont Circle"
        }
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
            "note": "first",
            "name": "Fool"
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
    }'''))

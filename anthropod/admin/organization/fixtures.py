import json

from anthropod.core import db


def load():
    db.organizations.insert(json.loads('''
    {
        "name": "Boise City Council",
        "geography_id": "ocd:location:country-us:state-idaho:city-boise",
        "source_url": "http://mayor.cityofboise.org/city-council/"
    }'''))

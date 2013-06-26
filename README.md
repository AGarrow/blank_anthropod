Anthropod
===========

To get started:

1. Create a new virtualenv.

    mkvirtualenv ocdtest

2. Clone the repo.

    git clone git@github.com:opencivicdata/anthropod.git && cd anthropod/

3. Add Larvae to dependencies
    #requirements.txt
    ...
    -e git+http://github.com/opencivicdata/larvae.git#egg=larvae

3. Install the dependencies.

    pip install -r requirements.txt

4. Create a local settings file
    
    #anthropod/settings/local.py
    from anthropod.settings.base import *


    # Put sensitive settings in local.py.
    LOCUST_URL = 'http://example.com/locust/'
    SECRET_KEY = 'some_secret'


5. Start the development server.

    python manage.py runserver --settings=anthropod.settings.dev

6. Edit people and organizations.

    http://localhost:8000/collect/organization/


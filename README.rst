Anthropod
===========

To get started:

1. Create a new virtualenv.

    mkvirtualenv ocdtest

2. Clone the repo.

    git clone git@github.com:opencivicdata/anthropod.git && cd anthropod/

3. Install the dependencies.

    pip install -r requirements.txt

4. Load some division ids.

    python manage.py loadgeo "https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-us/state-nc.csv" --settings=anthropod.settings.dev

5. Start the development server.

    python manage.py runserver --settings=anthropod.settings.dev

6. Edit people and organizations.

    http://localhost:8000/collect/organization/


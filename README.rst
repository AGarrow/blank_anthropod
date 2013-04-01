Anthropod
===========

To get started:

1. Create a new virtualenv.

    mkvirtualenv ocdtest

2. Clone the repo.

    git clone git@github.com:opencivicdata/anthropod.git
    cd anthropod/

3. Install the dependencies.

    pip install -r requirements.txt

4. Load the example fixtures.

    python anthropod/scripts/load_fixtures.py

5. Start the development server.

    python manage.py runserver --settings='anthropod.settings.dev'

6. View people in the database.

    http://localhost:8000/admin/person/


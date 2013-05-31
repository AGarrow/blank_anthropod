from pprint import pformat
from difflib import get_close_matches

from django.core.management.base import BaseCommand

from anthropod.core import db, user_db


class Command(BaseCommand):
    args = '<username1>[,<username2>[,<username3>]] <permission1> <permission2> ...'
    help = ('Grant permissions to a user. Multiple emails can be '
            'join with a comma.')
    can_import_settings = True

    def handle(self, usernames, *permissions, **options):

        # Complain if the collection name is mistyped.
        collection_names = db.collection_names()
        collection_names.remove('system.indexes')
        for permission in permissions:
            collection_name, operation = permission.split('.')
            if collection_name not in collection_names:
                suggestions = get_close_matches(collection_name, collection_names)
                suggestions = suggestions or collection_names
                suggestions = map(repr, suggestions)
                msg = ("Can't grant permissions on collection %r; "
                       "there is no such collection. Maybe you meant %s?")
                args = (collection_name, ' or '.join(suggestions))
                raise ValueError(msg % args)

        # Update the mongo permissions collection.
        permissions = dict.fromkeys(permissions, True)
        document = {'$set': permissions}
        for username in usernames.split(','):
            spec = {'user_id': username}
            msg = 'Granting user %r these permissions: %r'
            self.stdout.write(msg % (username, permissions))
            user_db.permissions.update(spec, document, upsert=True)

            # Show the new permissions.
            new_perms = user_db.permissions.find_one(spec)
            map(new_perms.pop, ('_id', 'user_id'))
            msg = "Permissions for %s now are:\n%s"
            msg = msg % (username, pformat(new_perms))
            self.stdout.write(msg, ending='\n\n')

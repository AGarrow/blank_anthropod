from pprint import pformat
from optparse import make_option
from difflib import get_close_matches

from django.core.management.base import BaseCommand

from anthropod.core import db, user_db


class Command(BaseCommand):
    args = '<username1>[,<usernameN>] <permission1> <permission2> ...'
    help = '''
    Grant or revoke permissions for one or more users. Multiple
    emails can be joined with a comma. Use --revoke to revoke
    instead of grant.'''.strip('\n')

    can_import_settings = True

    option_list = BaseCommand.option_list + (
    make_option('--revoke',
        action='store_true',
        dest='revoke',
        default=False,
        help='Revoke permissions instead of granting them.'),
    )

    def handle(self, usernames, *permissions, **options):

        # Granting or revoking?
        if options['revoke']:
            verb = 'revoke'
            action = '$unset'
        else:
            verb = 'grant'
            action = '$set'


        # Complain if the collection name is mistyped.
        collection_names = db.collection_names()
        collection_names.remove('system.indexes')
        for permission in permissions:
            if permission == 'all':
                continue
            collection_name, operation = permission.split('.')
            if collection_name not in collection_names:
                suggestions = get_close_matches(collection_name, collection_names)
                suggestions = suggestions or collection_names
                suggestions = map(repr, suggestions)
                msg = ("Can't %s permissions on collection %r; "
                       "there is no such collection. Maybe you meant %s?")
                args = (verb, collection_name, ' or '.join(suggestions))
                raise ValueError(msg % args)

        # Update the mongo permissions collection.
        permissions = dict.fromkeys(permissions, True)
        document = {action: permissions}
        for username in usernames.split(','):
            spec = {'user_id': username}
            msg = '%s user %r these permissions: %r'
            self.stdout.write(msg % (verb.title(), username, permissions))

            user_db.permissions.update(spec, document, upsert=True, multi=True)

            # Show the new permissions.
            new_perms = user_db.permissions.find_one(spec)
            map(new_perms.pop, ('_id', 'user_id'))
            msg = "Permissions for %s now are:\n%s"
            msg = msg % (username, pformat(new_perms))
            self.stdout.write(msg, ending='\n\n')

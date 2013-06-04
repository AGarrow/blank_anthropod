from optparse import make_option

from django.core.management.base import BaseCommand

from anthropod.core import db, user_db
from anthropod.collect.permissions import grant_permissions, revoke_permissions


class Command(BaseCommand):
    args = '<username1>[,<username2>] <permission1>[,<permission2>] <id1>[,<id2>]...'
    help = '''
    Grant or revoke one or more permissions for one or more usernames
    for one or more ocd_ids. Use --revoke to revoke.
    '''.strip('\n')

    can_import_settings = True

    option_list = BaseCommand.option_list + (
    make_option('--revoke',
        action='store_true',
        dest='revoke',
        default=False,
        help='Revoke permissions instead of granting them.'),
    )

    collection_names = db.collection_names()
    collection_names.remove('system.indexes')

    def handle(self, usernames, permissions, ocd_ids=None, **options):

        permissions = permissions.split(',')
        self.check_collection_names(permissions)
        self.check_usernames(usernames)

        # Granting or revoking?
        if options['revoke']:
            self.revoke(usernames, ocd_ids, permissions)
        else:
            self.grant(usernames, ocd_ids, permissions)

    def check_usernames(self, usernames):
        for username in usernames.split(','):
            if '@' not in username:
                msg = 'Usernames should be email addresses, not %r.'
                raise ValueError(msg % username)

    def check_collection_names(self, permissions):
        # Complain if the collection name is mistyped.
        for permission in permissions:
            collection_name, operation = permission.split('.')
            if collection_name not in self.collection_names:
                suggestions = map(repr, self.collection_names)
                msg = ("Can't grant permissions on collection %r; "
                       "there is no such collection. Choose from %s.")
                args = (collection_name, ' or '.join(suggestions))
                raise ValueError(msg % args)

    def grant(self, usernames, ocd_ids, permissions):
        for username in usernames.split(','):
            msg = 'Granting permissions: %r'
            if ocd_ids is None:
                self.stdout.write(msg % [username, permissions])
                grant_permissions(username, ocd_ids, *permissions)
                return
            for ocd_id in ocd_ids.split(','):
                self.stdout.write(msg % [username, ocd_id, permissions])
                grant_permissions(username, ocd_id, *permissions)

    def revoke(self, usernames, ocd_ids, permissions):
        for username in usernames.split(','):
            msg = 'Revoking permissions: %r'
            if ocd_ids is None:
                self.stdout.write(msg % [username, ocd_ids, permissions])
                revoke_permissions(username, ocd_ids, *permissions)
                return

            for ocd_id in ocd_ids.split(','):
                self.stdout.write(msg % [username, ocd_id, permissions])
                revoke_permissions(username, ocd_id, *permissions)

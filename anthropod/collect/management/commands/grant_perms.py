from optparse import make_option

from django.core.management.base import BaseCommand

from anthropod.core import user_db
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

    def handle(self, usernames, ocd_ids, permissions, **options):

        # Granting or revoking?
        if options['revoke']:
            self.revoke(usernames, ocd_ids, permissions.split(','))
        else:
            self.grant(usernames, ocd_ids, permissions.split(','))

    def grant(self, usernames, ocd_ids, permissions):
        for username in usernames.split(','):
            for ocd_id in ocd_ids.split(','):
                msg = 'Granting permissions: %r'
                self.stdout.write(msg % [username, ocd_id, permissions])
                grant_permissions(username, ocd_id, *permissions)

    def revoke(self, usernames, ocd_ids, permissions):
        for username in usernames.split(','):
            for ocd_id in ocd_ids.split(','):
                msg = 'Revoking permissions: %r'
                self.stdout.write(msg % [username, ocd_id, permissions])
                revoke_permissions(username, ocd_id, *permissions)

from optparse import make_option

from django.core.management.base import BaseCommand

from anthropod.collect.permissions import grant_admin, revoke_admin


class Command(BaseCommand):
    args = '<username1>[,<username2>]'
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

    def handle(self, usernames, **options):
        for username in usernames.split(','):
            if options['revoke']:
                revoke_admin(username)
                msg = 'Revoked admin status for %s'
                self.stdout.write(msg % username)
            else:
                msg = 'Granted admin status to %s'
                self.stdout.write(msg % username)
                grant_admin(username)

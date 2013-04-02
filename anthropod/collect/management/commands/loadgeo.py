from __future__ import print_function
import csv
import urllib2
from django.core.management.base import BaseCommand, CommandError

from anthropod.core import db

class Command(BaseCommand):
    args = '<csvurl>'
    help = 'Load a CSV of OCD divisions'

    def handle(self, *args, **options):
        for csvurl in args:
            print('Loading data from', csvurl)
            csvf = csv.reader(urllib2.urlopen(csvurl))
            counter = 0
            for name, _id in csvf:
                db.divisions.save({'_id': _id, 'name': name})
                counter += 1
            print('Loaded', counter, 'divisions')

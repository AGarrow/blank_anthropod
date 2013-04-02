from django.core.urlresolvers import reverse

from anthropod.core import db
from anthropod.models.base import ModelBase


class Person(ModelBase):
    collection = db.people

    def organization(self):
        organization_id = self['organization_id']
        org = db.organizations.find_one(organization_id)
        if org is None:
            msg = 'No organization with id %r was found in the database.'
            raise self.DoesNotExist(msg % organization_id)
        return org

    def display(self):
        return self['name']

    def detail_url(self):
        return reverse('person.detail', kwargs=dict(_id=self.id_string))


class Organization(ModelBase):
    collection = db.organizations

    def people(self, extra_spec=None):
        spec = dict(organization_id=self.id)
        if extra_spec is not None:
            spec.update(extra_spec)
        return db.people.find(spec)

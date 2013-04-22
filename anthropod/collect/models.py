from django.core.urlresolvers import reverse

from anthropod.core import db
from anthropod.models.base import ModelBase


class Person(ModelBase):
    collection = db.people

    def memberships(self):
        memberships = db.memberships.find({'person_id': self.id})
        if memberships is None:
            msg = 'No memerships found for person %r.'
            raise self.DoesNotExist(msg % self.id)
        return memberships

    def display(self):
        return self['name']

    def detail_url(self):
        return reverse('person.detail', kwargs=dict(_id=self.id_string))


class Organization(ModelBase):
    collection = db.organizations

    def memberships(self, spec=None, *args, **kwargs):
        spec = spec or {}
        spec.update(organization_id=self.id)
        return Membership.find(spec, *args, **kwargs)

    def members(self):
        person_ids = []
        for obj in self.memberships(fields=('person_id',)):
            person_ids.append(obj['person_id'])
        membs = db.people.find({'_id': {'$in': person_ids}})
        return membs

    def people(self, extra_spec=None):
        spec = dict(organization_id=self.id)
        if extra_spec is not None:
            spec.update(extra_spec)
        return db.people.find(spec)

    def display(self):
        return self['name']

    def detail_url(self):
        return reverse('organization.detail', kwargs=dict(_id=self.id_string))


class Membership(ModelBase):
    collection = db.memberships

    def organization(self):
        return Organization.find_one(self['organization_id'])

    def person(self):
        return Person.find_one(self['person_id'])

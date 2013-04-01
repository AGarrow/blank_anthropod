from anthropod.core import db
from anthropod.models.base import ModelBase


class Organization(ModelBase):
    collection = db.organizations

    def people(self, extra_spec=None):
        spec = dict(organization_id=self.id)
        if extra_spec is not None:
            spec.update(extra_spec)
        return db.people.find(spec)

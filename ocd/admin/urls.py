from django.conf.urls import patterns, url
from ocd.admin.views import CreatePerson, person


urlpatterns = patterns('',
    url(r'^create_person/', CreatePerson.as_view()),
    url(r'^person/(?P<_id>\w+)', person, name='person'),
)

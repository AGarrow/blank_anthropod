from django.conf.urls import patterns, url

from ocd.admin.views import CreatePerson, person, person_list


urlpatterns = patterns('',
    url(r'^person/list/', person_list, name="person.list"),
    url(r'^person/create/', CreatePerson.as_view(), name='person.create'),
    url(r'^person/(?P<_id>\w+)', person, name='person.detail'),
)

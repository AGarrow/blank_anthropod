from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from ocd.admin.views import CreatePerson, person, person_list


urlpatterns = patterns('',
    url(r'^person/list/', person_list),
    url(r'^person/create/', CreatePerson.as_view()),
    url(r'^person/(?P<_id>\w+)', person, name='person'),
)

urlpatterns += staticfiles_urlpatterns()

from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^person/', include('anthropod.admin.person.urls')),
    url(r'^organization/', include('anthropod.admin.organization.urls')),
)

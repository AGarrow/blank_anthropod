from django.conf.urls import patterns, include, url
from .views import person, organization


urlpatterns = patterns('anthropod.admin.views.person',
    url(r'^person/create/$', person.Edit.as_view(), name='person.create'),
    url(r'^person/edit/(?P<_id>\w+)/$', person.Edit.as_view(), name='person.edit'),
    url(r'^person/delete/$', 'delete', name='person.delete'),
    url(r'^person/really_delete/$', 'really_delete', name='person.really_delete'),
    url(r'^person/detail/(?P<_id>\w+)/$', 'detail', name='person.detail'),
    url(r'person/$', 'listing', name='person.list'),
)

urlpatterns += patterns('anthropod.admin.views.organization',
    url(r'^create/$', organization.Edit.as_view(), name='organization.create'),
    url(r'^edit/(?P<_id>\w+)/$', organization.Edit.as_view(), name='organization.edit'),
    url(r'^delete/$', 'delete', name='organization.delete'),
    url(r'^really_delete/$', 'really_delete', name='organization.really_delete'),
    url(r'^detail/(?P<_id>\w+)/$', 'detail', name='organization.detail'),
    url(r'$', 'listing', name='organization.list'),
)

from django.conf.urls import patterns, url
from .views import person, organization, geo


urlpatterns = patterns('anthropod.collect.views.person',
    url(r'^person/create/$', person.Edit.as_view(), name='person.create'),
    url(r'^person/edit/(?P<_id>\w+)/$', person.Edit.as_view(), name='person.edit'),
    url(r'^person/delete/$', 'delete', name='person.delete'),
    url(r'^person/really_delete/$', 'really_delete', name='person.really_delete'),
    url(r'^person/detail/(?P<_id>\w+)/$', 'detail', name='person.detail'),
    url(r'^person/$', 'listing', name='person.list'),
)

urlpatterns += patterns('anthropod.collect.views.organization',
    url(r'^orgs/create/$', organization.Edit.as_view(), name='organization.create'),
    url(r'^orgs/edit/(?P<_id>\w+)/$', organization.Edit.as_view(), name='organization.edit'),
    url(r'^orgs/delete/$', 'delete', name='organization.delete'),
    url(r'^orgs/really_delete/$', 'really_delete', name='organization.really_delete'),
    url(r'^orgs/detail/(?P<_id>\w+)/$', 'detail', name='organization.detail'),
    # url(r'^orgs/remove_person/(?P<organization_id>\w+)/(?P<person_id>\w+)/$',
    #     'remove_person', name='organization.remove_person'),
    url(r'^orgs/$', 'listing', name='organization.list'),
)

urlpatterns += patterns('anthropod.collect.views.geo',
    url(r'^geo/select/$', geo.Select.as_view(), name='geo.select'),
    url(r'^geo/child_id_jon/(?P<_id>.+)$', 'child_id_json', name='geo.child_id_json'),
    url(r'^geo/detail/(?P<_id>.+)$', 'detail', name='geo.detail'),
)


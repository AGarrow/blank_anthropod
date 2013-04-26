from django.conf.urls import patterns, url
from .views import person, person_memb
from .views import organization, org_memb
from .views import geo, membership


urlpatterns = patterns('anthropod.collect.views.person',
    url(r'^person/create/$', person.Edit.as_view(), name='person.create'),
    url(r'^person/edit/(?P<_id>\S+?)/$', person.Edit.as_view(), name='person.edit'),
    url(r'^person/jsonview/(?P<_id>\S+?)/$', 'jsonview', name='person.jsonview'),
    url(r'^person/delete/$', 'delete', name='person.delete'),
    url(r'^person/really_delete/$', 'really_delete', name='person.really_delete'),
    url(r'^person/json/$', 'all_json', name='person.json'),
    url(r'^person/$', 'listing', name='person.listing'),
)

urlpatterns += patterns('anthropod.collect.views.person_memb',
    url(r'^person/members/listing/(?P<_id>\S+?)/$', 'listing', name='person.memb.listing'),
    url(r'^person/members/delete/$', 'delete', name='person.memb.delete'),
    url(r'^person/members/really_delete/$', 'really_delete', name='person.memb.really_delete'),
    url(r'^person/members/select_geo/$',
        person_memb.SelectGeo.as_view(), name='person.memb.add.geo'),
    url(r'^person/members/select_org/$',
        person_memb.SelectOrg.as_view(), name='person.memb.add.org'),
)

urlpatterns += patterns('anthropod.collect.views.organization',
    url(r'^orgs/create/$', 'create', name='organization.create'),
    url(r'^orgs/create_from_place/(?P<geo_id>\S+)$', organization.Edit.as_view(), name='organization.create_from_place'),
    url(r'^orgs/edit/(?P<_id>\S+?)/$', organization.Edit.as_view(), name='organization.edit'),
    url(r'^orgs/delete/$', 'delete', name='organization.delete'),
    url(r'^orgs/really_delete/$', 'really_delete', name='organization.really_delete'),
    url(r'^orgs/jsonview/(?P<_id>\S+?)/$', 'jsonview', name='organization.jsonview'),
    url(r'^orgs/json_for_geo/(?P<geo_id>.+)$', 'json_for_geo', name='organization.json_for_geo'),
    url(r'^orgs/$', 'listing', name='organization.list'),
)

urlpatterns += patterns('anthropod.collect.views.org_memb',
    url(r'^orgs/members/listing/(?P<_id>\S+?)/$', 'listing', name='org.memb.listing'),
    url(r'^orgs/members/delete/$', 'delete', name='org.memb.delete'),
    url(r'^orgs/members/really_delete/$', 'really_delete', name='org.memb.really_delete'),
    url(r'^orgs/members/select_person/(?P<org_id>\S+?)/$',
        org_memb.SelectPerson.as_view(), name='org.memb.add.person'),
)

urlpatterns += patterns('anthropod.collect.views.geo',
    url(r'^geo/select/$', geo.Select.as_view(), name='geo.select'),
    url(r'^geo/child_id_json/(?P<_id>.+)$', 'child_id_json', name='geo.child_id_json'),
    url(r'^geo/detail/(?P<_id>.+)$', 'detail', name='geo.detail'),
)

urlpatterns += patterns('anthropod.collect.views.membership',
    url(r'^memb/edit/(?P<_id>\S+?)$', membership.Edit.as_view(), name='memb.edit'),
    url(r'^memb/jsonview/(?P<_id>\S+?)$', 'jsonview', name='memb.jsonview'),
    url(r'^memb/delete/(?P<_id>\S+?)$', 'delete', name='memb.delete'),
)

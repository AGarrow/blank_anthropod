from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from .views import person, person_memb
from .views import organization, org_memb
from .views import geo, membership


urlpatterns = patterns('anthropod.collect.views.person',
    url(r'^person/create/$', person.Edit.as_view(), name='person.create'),
    url(r'^person/edit/$', person.Edit.as_view(), name='person.edit'),
    url(r'^person/jsonview/(?P<_id>\S+?)/$', 'jsonview', name='person.jsonview'),
    url(r'^person/confirm_delete/$', 'confirm_delete', name='person.confirm_delete'),
    url(r'^person/delete/$', 'delete', name='person.delete'),
    url(r'^person/json/$', 'all_json', name='person.json'),
    url(r'^person/$', 'listing', name='person.listing'),
    url(r'^person/find/$', TemplateView.as_view(template_name='person/find.html'), name='person.find'),
)

urlpatterns += patterns('anthropod.collect.views.person_memb',
    url(r'^person/members/listing/(?P<_id>\S+?)/$', 'listing', name='person.memb.listing'),
    url(r'^person/members/confirm_delete/$', 'confirm_delete', name='person.memb.confirm_delete'),
    url(r'^person/members/delete/$', 'delete', name='person.memb.delete'),
    url(r'^person/members/select_geo/$',
        person_memb.SelectGeo.as_view(), name='person.memb.add.geo'),
    url(r'^person/members/select_org/$',
        person_memb.SelectOrg.as_view(), name='person.memb.add.org'),
)

urlpatterns += patterns('anthropod.collect.views.organization',
    url(r'^orgs/create/$', 'create', name='organization.create'),
    url(r'^orgs/create_from_place/(?P<geo_id>\S+)$', organization.Edit.as_view(), name='organization.create_from_place'),
    url(r'^orgs/create_member/', person.Edit.as_view(), name='organization.create_member'),
    url(r'^orgs/edit/(?P<_id>\S+?)/$', organization.Edit.as_view(), name='organization.edit'),
    url(r'^orgs/confirm_delete/$', 'confirm_delete', name='organization.confirm_delete'),
    url(r'^orgs/delete/$', 'delete', name='organization.delete'),
    url(r'^orgs/jsonview/(?P<_id>\S+?)/$', 'jsonview', name='organization.jsonview'),
    url(r'^orgs/json_for_geo/(?P<geo_id>.+)$', 'json_for_geo', name='organization.json_for_geo'),
    url(r'^orgs/$', 'listing', name='organization.list'),
)

urlpatterns += patterns('anthropod.collect.views.org_memb',
    url(r'^orgs/members/listing/(?P<_id>\S+?)/$', 'listing', name='org.memb.listing'),
    url(r'^orgs/confirm_members/delete/$', 'confirm_delete', name='org.memb.confirm_delete'),
    url(r'^orgs/members/delete/$', 'delete', name='org.memb.delete'),
    url(r'^orgs/members/select_person/(?P<org_id>\S+?)/$',
        org_memb.SelectPerson.as_view(), name='org.memb.add.person'),
)

urlpatterns += patterns('anthropod.collect.views.geo',
    url(r'^geo/select/$', geo.Select.as_view(), name='geo.select'),
    url(r'^geo/child_id_json/(?P<_id>.+)$', 'child_id_json', name='geo.child_id_json'),
    url(r'^geo/detail/(?P<_id>.+)$', 'detail', name='geo.detail'),
)

urlpatterns += patterns('anthropod.collect.views.membership',
    url(r'^memb/edit/', membership.Edit.as_view(), name='memb.edit'),
    url(r'^memb/jsonview/(?P<_id>\S+?)$', 'jsonview', name='memb.jsonview'),
    url(r'^memb/confirm_delete/$', 'confirm_delete', name='memb.confirm_delete'),
    url(r'^memb/delete/$', 'delete', name='memb.delete'),
)

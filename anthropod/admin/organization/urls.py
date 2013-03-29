from django.conf.urls import patterns, url

from anthropod.admin.organization.views import Edit


urlpatterns = patterns(
    'anthropod.admin.organization.views',
    url(r'^create/$', Edit.as_view(), name='organization.create'),
    url(r'^edit/(?P<_id>\w+)/$', Edit.as_view(), name='organization.edit'),
    url(r'^delete/$', 'delete', name='organization.delete'),
    url(r'^really_delete/$', 'really_delete', name='organization.really_delete'),
    url(r'^detail/(?P<_id>\w+)/$', 'detail', name='organization.detail'),
    url(r'$', 'listing', name='organization.list'),
)

from django.conf.urls import patterns, url

from anthropod.admin.person.views import Edit


urlpatterns = patterns(
    'anthropod.admin.person.views',
    url(r'^create/$', Edit.as_view(), name='person.create'),
    url(r'^edit/(?P<_id>\w+)/$', Edit.as_view(), name='person.edit'),
    url(r'^delete/$', 'delete', name='person.delete'),
    url(r'^really_delete/$', 'really_delete', name='person.really_delete'),
    url(r'^detail/(?P<_id>\w+)/$', 'detail', name='person.detail'),
    url(r'$', 'listing', name='person.list'),
)

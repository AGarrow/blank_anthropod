from django.conf.urls import patterns, url

import anthropod.admin.views.person


urlpatterns = patterns('^person/',

    url(r'/$',
        anthropod.admin.views.person.listing, name='person.list'),

    url(r'create/$',
        anthropod.admin.views.person.Edit.as_view(),
        name='person.create'),

    url(r'edit/(?P<_id>\w+)',
        anthropod.admin.views.person.Edit.as_view(),
        name='person.edit'),

    url(r'delete/',
        anthropod.admin.views.person.delete, name='person.delete'),

    url(r'really_delete/',
        anthropod.admin.views.person.really_delete,
        name='person.really_delete'),

    url(r'detail/(?P<_id>\w+)/$',
        anthropod.admin.views.person.detail, name='person.detail'),
)

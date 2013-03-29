from django.conf.urls import patterns, url

import anthropod.admin.views.person


urlpatterns = patterns('',

    url(r'^person/$',
        anthropod.admin.views.person.listing, name='person.list'),

    url(r'^person/create/$',
        anthropod.admin.views.person.Edit.as_view(),
        name='person.create'),

    url(r'^person/edit/(?P<_id>\w+)',
        anthropod.admin.views.person.Edit.as_view(),
        name='person.edit'),

    url(r'^person/delete/',
        anthropod.admin.views.person.delete, name='person.delete'),

    url(r'^person/really_delete/',
        anthropod.admin.views.person.really_delete,
        name='person.really_delete'),

    url(r'^person/detail/(?P<_id>\w+)/$',
        anthropod.admin.views.person.detail, name='person.detail'),
)

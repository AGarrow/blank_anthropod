from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'', include('sunlightauth.urls')),
    url(r'^collect/', include('anthropod.collect.urls')),
)

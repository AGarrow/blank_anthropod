from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^ocd/', include('ocd.admin.urls')),
)

from django.conf.urls import patterns, url

from .views import CombinedActivityFeed


urlpatterns = patterns('',
    url(r'^combined/', CombinedActivityFeed.as_view(), name='activity_stream_combined'),
)

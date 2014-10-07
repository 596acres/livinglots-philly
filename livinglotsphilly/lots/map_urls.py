from django.conf.urls import patterns, url

from .views import LotsMap


urlpatterns = patterns('',
    url(r'^', LotsMap.as_view()),
)

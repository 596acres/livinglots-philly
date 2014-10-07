from django.conf.urls import patterns, url

from .views import ContactCompleted

urlpatterns = patterns('',
    url('^$', ContactCompleted.as_view(), name='completed'),
)

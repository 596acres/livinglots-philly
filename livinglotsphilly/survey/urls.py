from django.conf.urls import patterns, url

from .views import SurveyView


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/submit/$', SurveyView.as_view(), name='survey_submit'),
)

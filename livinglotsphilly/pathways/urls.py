from django.conf.urls import patterns, url
from .views import PathwaysDetailView, PathwaysListView


urlpatterns = patterns('',
    url(r'^(?P<slug>[^/]+)/$', PathwaysDetailView.as_view(),
        name='pathway_detail'),

    url(r'', PathwaysListView.as_view(), name='pathway_list'),
)

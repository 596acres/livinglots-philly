from django.conf.urls.defaults import patterns, url

from libapps.organize.models import Organizer, Watcher

from .views import (LotDetailView, EditLotParicipantView, AddParticipantView,
                    LotsGeoJSON, LotsGeoJSONPolygon, AddParticipantSuccessView,
                    AddPhotoView, AddNoteView, AddFileView, LotsCountView,
                    LotsCountBoundaryView, LotsCSV, LotsKML)


urlpatterns = patterns('',
    url(r'^csv/', LotsCSV.as_view(), name='csv'),
    url(r'^geojson/', LotsGeoJSON.as_view(), name='geojson'),
    url(r'^kml/', LotsKML.as_view(), name='kml'),
    url(r'^geojson-polygon/', LotsGeoJSONPolygon.as_view(),
        name='lot_geojson_polygon'),
    url(r'^count/', LotsCountView.as_view(), name='lot_count'),
    url(r'^count-by-boundary/', LotsCountBoundaryView.as_view(),
        name='lot_count_by_boundary'),

    url(r'^(?P<pk>\d+)/$', LotDetailView.as_view(), name='lot_detail'),

    url(r'^(?P<pk>\d+)/organize/$',
        AddParticipantView.as_view(
            model=Organizer,
        ),
        name='add_organizer'),

    url(r'^(?P<pk>\d+)/watch/$',
        AddParticipantView.as_view(
            model=Watcher,
        ),
        name='add_watcher'),

    url(r'^(?P<pk>\d+)/organize/organizer/(?P<hash>[^/]{30,})/success/$',
        AddParticipantSuccessView.as_view(
            model=Organizer,
        ),
        name='add_organizer_success'),

    url(r'^(?P<pk>\d+)/organize/watcher/(?P<hash>[^/]{30,})/success/$',
        AddParticipantSuccessView.as_view(
            model=Watcher,
        ),
        name='add_watcher_success'),

    url(r'^organize/(?P<hash>[^/]{30,})/edit/$',
        EditLotParicipantView.as_view(),
        name='edit_participant'),

    url(r'^(?P<pk>\d+)/photos/add/$',
        AddPhotoView.as_view(),
        name='add_photo'),

    url(r'^(?P<pk>\d+)/notes/add/$',
        AddNoteView.as_view(),
        name='add_note'),

    url(r'^(?P<pk>\d+)/files/add/$', AddFileView.as_view(), name='add_file'),
)

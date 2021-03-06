var _ = require('underscore');
var L = require('leaflet');
var Spinner = require('spinjs');
var friendlyowners = require('./friendlyowners');
var singleminded = require('./singleminded');
var streetview = require('./streetview');
var welcome = require('./welcome');

require('./jquery.searchbar');

// Filter [de]serialization
require('jquery.deserialize');
require('jquery.serializeobject');

require('./leaflet.lotmap');
require('./overlaymenu');
require('jquery.debouncedresize');

require('leaflet.usermarker');


var MAX_LOTS_DOWNLOAD = 2000;

var currentViewType,
    lotsMap,
    mapViewportSet = false,
    visibleLotsCount = 0;


/*
 * Get bounds for searching
 */
function getBounds(map) {
    var bounds = map.options.maxBounds;
    var seBounds = bounds.getSouthEast();
    var nwBounds = bounds.getNorthWest();

    return [
        seBounds.lng,
        seBounds.lat,
        nwBounds.lng,
        nwBounds.lat
    ];
}


/*
 * Update counts
 */
function updateCounts() {
    lotsMap.fire('dataloading');
    var baseUrl = $('#map').data('countsbaseurl'),
        params = serializeFilters();

    singleminded.remember({
        name: 'counts',
        jqxhr: $.getJSON(baseUrl + params, function (data) {
            $.each(data, function (label, count) {
                $('.' + label).text(count);
            });
            visibleLotsCount = data['lots-count'];
            lotsMap.setVisibleLotsCount(visibleLotsCount);
        })
        .always(function () {
            lotsMap.fire('dataload');
        }),
    });
}


/*
 * Handle filter inputs
 */
function serializeFilters() {
    // If showing organizing lots only, filter to those
    var serialized = $('form:not(.non-filter)').serialize();
    if ($('form :input[name=organizing]').val() === 'only') {
        serialized += '&participant_types=organizers';
    }
    return serialized;
}

function deserializeFilters() {
    // Get filters from url query string
    var filters = window.location.search.slice(1);

    // Clear the form of any defaults, first
    if (filters.length > 1) {
        $(':checkbox').prop('checked', false);
    }

    // Drop filters into the form (which is spread over multiple forms)
    $('form').deserialize(filters);
}

function updateMapWithFilters() {
    // Trigger Chosen to update selects
    $('select').trigger('liszt:updated');

    // Update map viewport
    var bboxString = $(':input[name="centroid__within"]').val();
    if (bboxString) {
        mapViewportSet = true;
        lotsMap.fitBounds(L.geoJsonLatLngBounds(bboxString));
    }
    var zoomString = $(':input[name="zoom"]').val();
    var zoom = 16;
    if (zoomString) {
        zoom = parseInt(zoomString, 10);
    }
    var centroidString = $(':input[name="centroid"]').val();
    if (centroidString) {
        mapViewportSet = true;
        lotsMap.setView(JSON.parse(centroidString), zoom);
    }

    // Trigger boundaries update
    $('.filter-boundaries').filter(function () {
        return $(this).val() !== '';  
    }).change();
}

function exportView() {
    if (visibleLotsCount > MAX_LOTS_DOWNLOAD) {
        alert('Too many lots to download! Filter the map and try again once the number of lots is no more than ' + MAX_LOTS_DOWNLOAD + '.');
    }
    else {
        window.location = $(this).data('baseurl') + serializeFilters();
    }
    return false;
}

function initializeBoundaries(map) {
    // Check for expected layers, console a warning
    var url = window.location.protocol + '//' + window.location.host +
        Django.url('inplace:layer_upload');
    var expectedLayers = ['city council districts', 'planning districts', 'zipcodes'];
    _.each(expectedLayers, function (layer) {
        if ($('.filter-' + layer.replace(/ /g, '-')).length === 0) {
            console.warn('No ' + layer + '! Add some here: ' + url);
        }
    });

    $('.filter-boundaries').change(function () {
        // Clear other boundary filters
        $('.filter-boundaries').not('#' + $(this).attr('id')).val('');

        addBoundary(map, $(this).data('layer'), $(this).val());
    });
}

function addBoundary(map, layer, pk) {
    if (!pk || pk === '') {
        map.removeBoundaries();
    }
    var url = Django.url('inplace:boundary_detail', { pk: pk });
    $.getJSON(url, function (data) {
        map.updateBoundaries(data, { zoomToBounds: true });
    });
}

function onFilterChange() {
    updateCounts();
    var serializedFilters = $('.filters :input:not(.non-filter)').serializeObject();
    lotsMap.updateFilters(serializedFilters);
    lotsMap.fire('filterschange', { filters: serializedFilters, });
}

$(document).ready(function () {
    if ($('.home-map-page').length > 0) {
        var mapboxId = $('#map').data('mapboxid'),
            popupSpinner;

        // Deserialize filters to include in the map's options
        deserializeFilters();

        // Prepare our map
        lotsMap = L.map('map', {
            initialFilters: $('.filters :input:not(.non-filter)').serializeObject(),
            center: [39.991, -75.159],
            maxBounds: [
                [39.147, -76.358],
                [40.772, -73.952]
            ],
            zoom: 11,
            scrollWheelZoom: false,
            mapboxId: mapboxId,
            bingKey: 'ArBLp_jhvmrzT5Kg4_FXohJCKjbKmBW-nEEItp2dbceyHrJPMJJEqXDp8XsPy_cr',
            clickHandler: function (e, feature) {
                var featureId = null;
                if (feature) featureId = feature.id;
                var popupOptions = {
                    maxHeight: 150
                };
                if (L.Browser.mobile === true) {
                    popupOptions.maxWidth = 200;
                    popupOptions.minWidth = 200;
                }
                else {
                    popupOptions.minWidth = 300;
                }
                var popupContent = '<div id="popup-content" class="loading"></div>';
                if (e.targetType === 'utfgrid' && e.data !== null) {
                    featureId = e.data.id;
                    var popup = L.popup(popupOptions)
                        .setContent(popupContent)
                        .setLatLng(e.latlng)
                        .openOn(lotsMap);
                }
                else {
                    try {
                        e.target.bindPopup(popupContent, popupOptions).openPopup();
                    }
                    catch (exception) {}
                }
                var url = Django.url('inplace:lots_lot_detail_popup', { pk: featureId });
                if (featureId !== null) {
                    singleminded.remember({
                        name: 'clickHandler',
                        jqxhr: $.get(url, function (response) {
                            popupSpinner.stop();
                            $('#popup-content')
                                .html(response)
                                .removeClass('loading');
                        }),
                    });
                }
            },

            legendControl: true,
            legendFeatureTypes: [
                { name: 'public' },
                { name: 'private' },
                { name: 'in use' },
                { name: 'lots with activity' }
            ],

            loadingControl: true,

            enableLayersControl: true,

            enableChoropleth: true,
            choroplethBaseUrl: $('#map').data('choroplethbaseurl'),
            choroplethQueryString: 'parents_only=True',

            enablePolygons: true,
            polygonBaseUrl: $('#map').data('polygonbaseurl'),
            polygonInitialFilters: {
                parentsOnly: true
            },

            enableCentroids: true,
            centroidBaseUrl: $('#map').data('centroidbaseurl'),
            centroidInitialFilters: {
                parentsOnly: true
            },

            lotsCentroidThreshold: 2000,

            gridResolution: 8,

            enablePointPrivateTiles: true,
            pointPrivateTilesBaseUrl: $('#map').data('pointprivatetilesbaseurl'),
            pointPrivateGridBaseUrl: $('#map').data('pointprivategridbaseurl'),

            enablePointPublicTiles: true,
            pointPublicTilesBaseUrl: $('#map').data('pointpublictilesbaseurl'),
            pointPublicGridBaseUrl: $('#map').data('pointpublicgridbaseurl'),

            enablePointInUseTiles: true,
            pointInUseTilesBaseUrl: $('#map').data('pointinusetilesbaseurl'),
            pointInUseGridBaseUrl: $('#map').data('pointinusegridbaseurl'),

            parcelsUrl: $('#map').data('parcelsbaseurl'),

            // livinglots.emailparticipants
            emailOrganizersCountUrl: Django.url('extraadmin:mail_participants_count'),
            sendEmailUrl: Django.url('extraadmin:mail_participants')

        });

        /*
         * Map events
         */
        lotsMap.on('moveend', function (e) {
            var g = JSON.stringify(lotsMap.getBounds().toGeoJson());
            $(':input[name="centroid__within"]').val(
                JSON.stringify(lotsMap.getBounds().toGeoJson())
            );
            $(':input[name="centroid"]').val(
                JSON.stringify(lotsMap.getCenter())
            );
            $(':input[name="zoom"]').val(lotsMap.getZoom());

            updateCounts();
            var serializedFilters = $('.filters :input:not(.non-filter)').serializeObject();
            lotsMap.fire('filterschange', { filters: serializedFilters, });
        });

        lotsMap.on('lotclicked', function (data) {
            var event = data.event;
            streetview.load_streetview(event.latlng.lng, event.latlng.lat,
                                       $('#streetview-container'),
                                       $('#streetview-error'));
        });

        lotsMap.on('popupopen', function (e) {
            popupSpinner = new Spinner({}).spin($('#popup-content.loading')[0]);
        });

        lotsMap.on('popupclose', function (e) {
            $('#streetview-container').hide();
        });

        initializeBoundaries(lotsMap);

        lotsMap.on('boundarieschange', function () {
            var $activeBoundaries = $('.filter-boundaries').filter(function () {
                return $(this).val() !== '';
            });
            if ($activeBoundaries.length > 0) {
                $activeBoundaries.each(function () {
                    $('.map-tally-header-boundary-layer').text($(this).data('layer').slice(0, -1));
                    $('.map-tally-header-boundary-label').text($(this).find('option:selected').text());
                });
                $('body').addClass('boundary');
            }
            else {
                $('body').removeClass('boundary');
            }
        });

        lotsMap.whenReady(function (e) {
            // Ensure center / zoom / etc are correctly initialized
            updateMapWithFilters();
            onFilterChange();
        });

        /*
         * Filters events
         */
        $('.filters :input:not(.non-filter)').change(onFilterChange);

        /*
         * Handle export actions
         */
        $('.export-link').click(function (e) {
            e.preventDefault();
            window.location.search = serializeFilters();
        });

        $('.export-csv').click(exportView);
        $('.export-geojson').click(exportView);
        $('.export-kml').click(exportView);


        // Fire up searchbar
        $('.searchbar')
            .searchbar({
                bounds: getBounds(lotsMap),
                city: 'Philadelphia',
                state: 'PA',
                errorMessage: "Sorry, it doesn't seem that the address you " +
                    "entered is in Philadelphia. Try again?",
                warningSelector: '.warning',
            })
            .on('searchresultfound', function (e, data) {
                var latlng = [data.latitude, data.longitude];
                lotsMap.setView(latlng, 18);
                var usermarker = L.userMarker(latlng, { smallIcon: true })
                    .bindPopup('This is the address you searched for.');
                usermarker.addTo(lotsMap);
            });


        // Show/hide filters
        $('.map-filters-toggle').click(function () {
            $('.map-filters').toggle();
        });

        friendlyowners.init(lotsMap);
        welcome.init();

        $('.overlay-filter-button').overlaymenu({
            menu: '.overlaymenu-filter'
        });

        $('.overlay-news-button').overlaymenu({
            menu: '.overlaymenu-news'
        });

        $('.overlay-download-button').overlaymenu({
            menu: '.overlaymenu-download'
        });
    }
});

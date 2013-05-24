define(
    [
        // Dependencies we'll use the return values from
        'jquery',
        'leaflet',
        'django',
        'json2',

        // Internal plugins
        'jquery.activitystream',
        'jquery.searchbar',
        'jquery.singleminded',
        'jquery.streetview',

        // Filter [de]serialization
        'lib/jquery.deserialize.min',
        'lib/jquery.serializeobject.min',

        // Leaflet Map mixin
        'leaflet.lotmap',

    ], function($, L, Django, JSON) {

    var lotsMap;


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
        var baseUrl = $('#map').data('countsbaseurl');
        $('#map').singleminded({
            name: 'counts',
            jqxhr: $.getJSON(baseUrl + $('form').serialize(), function(data) {
                $.each(data, function(label, count) {
                    $('.' + label).text(count);
                });
            })
            .always(function() {
                lotsMap.fire('dataload');
            }),
        });
    }


    /*
     * Handle filter inputs
     */
    function serializeFilters() {
        return $('form').serialize();
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

        // Trigger Chosen to update selects
        $('select').trigger('liszt:updated');

        // Update map viewport
        var bboxString = $('#id_centroid__within').val();
        if (bboxString) {
            lotsMap.fitBounds(L.geoJsonLatLngBounds(bboxString));
        }
    }

    function updateViewType(viewType) {
        var viewTypeFilterSelector = '.view-type-' + viewType;

        // {En,Dis}able filters that should be {en,dis}abled for this view type
        $('.filter :input').prop('disabled', function(i, value) {
            return !$(this).parents('.filter').is(viewTypeFilterSelector);
        });

        // TODO for viewType===tiles, reset filters that are disabled 
        //  (ensures sanity and that counts are appropriate)
    }

    function onFilterChange() {
        if ($(this).attr('name') === 'view_type') {
            updateViewType($(this).val());
        }
        updateCounts();
        lotsMap.updateFilters($('form').serializeObject());
    }

    $(document).ready(function() {
        var key = $('#map').data('cloudmadekey'),
            style = $('#map').data('cloudmadestyle');


        // Prepare our map
        lotsMap = L.map('map', {
            center: [39.952335, -75.163789],
            maxBounds: [
                [39.147, -76.358],
                [40.772, -73.952],
            ],
            zoom: 11,
            cloudmadeKey: key,
            cloudmadeStyleId: style,
            bingKey: 'ArBLp_jhvmrzT5Kg4_FXohJCKjbKmBW-nEEItp2dbceyHrJPMJJEqXDp8XsPy_cr',
            clickHandler: function(e, feature) {
                var featureId = null;
                if (feature) featureId = feature.id;
                var popupOptions = {
                    minHeight: 250,
                    minWidth: 300,
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
                    catch (e) {}
                }
                var url = Django.url('inplace:lots_lot_detail_popup', { pk: featureId });
                if (featureId !== null) {
                    $('#map').singleminded({
                        name: 'clickHandler',
                        jqxhr: $.get(url, function(response) {
                            $('#popup-content')
                                .html(response)
                                .removeClass('loading');
                        }),
                    });
                }
            },

            messageControl: true,
            messageDefault: 'Zoom in for details',

            loadingControl: true,

            enableLayersControl: true,

            enableChoropleth: true,
            choroplethBaseUrl: $('#map').data('choroplethbaseurl'),
            choroplethQueryString: 'parents_only=True',

            enablePolygons: true,
            polygonBaseUrl: $('#map').data('polygonbaseurl'),
            polygonInitialFilters: { 
                parentsOnly: true,
            },

            gridResolution: 8,

            enablePointPrivateTiles: true,
            pointPrivateTilesBaseUrl: $('#map').data('pointprivatetilesbaseurl'),
            pointPrivateGridBaseUrl: $('#map').data('pointprivategridbaseurl'),

            enablePointPublicTiles: true,
            pointPublicTilesBaseUrl: $('#map').data('pointpublictilesbaseurl'),
            pointPublicGridBaseUrl: $('#map').data('pointpublicgridbaseurl'),

        });

        /*
         * Map events
         */
        lotsMap.on('moveend', function(e) {
            var g = JSON.stringify(lotsMap.getBounds().toGeoJson())
            $(':input[name="centroid__within"]').val(
                JSON.stringify(lotsMap.getBounds().toGeoJson())
            );
            updateCounts();
        });

        lotsMap.on('lotclicked', function(data) {
            var event = data.event;
            $('#streetview-container').data('streetview').load_streetview(
                event.latlng.lng, event.latlng.lat);
        });

        lotsMap.on('popupclose', function(e) {
            $('#streetview-container').hide();
        });

        // Load filters from search string in URL, update map/counts accordingly
        deserializeFilters();
        onFilterChange();

        // Update map and UI with the current view
        var currentView = $(':input[name=view_type]').val();
        updateViewType(currentView);
        lotsMap.changeView(currentView);

        /*
         * Filters events
         */
        $('.filters :input:not(.non-filter)').change(onFilterChange);


        /*
         * Prepare streetview
         */
        $('#streetview-container').streetview({
            errorSelector: '#streetview-error',
        });


        /*
         * Handle export actions
         */
        $('.export-link').click(function() {
            // TODO make shorter urls
            window.location.search = serializeFilters();
        });

        $('.export-csv').click(function() {
            window.location = $(this).data('baseurl') + serializeFilters();
            return false;
        });

        $('.export-geojson').click(function() {
            window.location = $(this).data('baseurl') + serializeFilters();
            return false;
        });

        $('.export-kml').click(function() {
            window.location = $(this).data('baseurl') + serializeFilters();
            return false;
        });


        // Fire up the activitystream
        $('.activity-stream-container').activitystream();


        // Fire up searchbar
        $('.searchbar')
            .searchbar({
                bounds: getBounds(lotsMap),
                city: 'Philadelphia',
                state: 'PA',
                errorMessage: "Sorry, it doesn't seem that the address you " +
                    "entered is in Philadelphia. Try again?",
                loadingSelector: '.loading',
                warningSelector: '.warning',
            })
            .on('searchresultfound', function(e, data) {
                lotsMap.setView([data.latitude, data.longitude], 15);
            });

    });

    return lotsMap;
});

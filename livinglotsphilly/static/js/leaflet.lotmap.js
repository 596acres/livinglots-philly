/*
 * L.LotMap -- mixin for L.Map that adds layers for vacant to vibrant.
 */

var L = require('leaflet');
var _ = require('underscore');
var lotStyles = require('./lotstyles');
var singleminded = require('./singleminded');

require('leaflet.bing');
require('leaflet.label');
require('leaflet.loading');
require('leaflet.utfgrid');
require('livinglots.emailparticipants');
require('livinglots.lotlayer');
require('livinglots-map/src/livinglots.boundaries');

require('./leaflet.geojsonbounds');
require('./leaflet.legend');
require('./leaflet.organizermarker');

L.PhillyLotLayer = L.LotLayer.extend({
    options: {
        getTileQueryString: function () {
            var filters = L.extend({}, this._map.filters),
                omitKeys = ['centroid__within'];
            return $.param(_.omit(filters, omitKeys), true);
        },

        onEachFeature: function (feature, layer) {
            layer.on('click', function (event) {
                layer._map.options.clickHandler(event, feature);
                layer._map.fire('lotclicked', {
                    event: event,
                    lot: feature,
                });
            });
        },

        style: function (feature) {
            return lotStyles.forLayer(feature.properties.layer);
        }
    }
});

L.PolygonLotLayer = L.PhillyLotLayer.extend({
    options: L.extend(L.PhillyLotLayer.prototype.options, {
        maxZoom: 19,
        minZoom: 16,
    })
});

L.polygonLotLayer = function (url, options) {
    var opts = L.extend({}, L.PolygonLotLayer.prototype.options, options);
    return new L.PolygonLotLayer(url, opts);
};

L.Map.include({

    /*
    options: {
        bingKey: String,
        centroidBaseUrl: String,
        centroidInitialFilters: Object,
        enableLayersControl: Boolean,
        enableChoropleth: Boolean,
        enablePointTiles: Boolean,
        enablePolygons: Boolean,
        polygonBaseUrl: String,
        polygonInitialFilters: Object,
        mapboxId: String,
        messageControl: Boolean,
        messageDefault: String,
        lotsCentroidThreshold: Integer,
    },
    */

    choroplethHsl: {
        hue: 140,
        saturation: 42,
        lightness: 90,
    },

    choroplethStyle: {
        fillOpacity: 0.7,
        color: 'white',
        opacity: 0.8,
        weight: 2,
    },

    tileLayers: {
        'public': [],
        'private': [],
        'not in use': [],
        'in use': [],
    },

    choroplethBoundaryLayerName: null,
    filters: {},
    viewType: 'tiles',
    visibleLotsCount: 0,


    _lotMapInitialize: function () {
        // Add base layers
        this.addSatelliteLayer(false);
        this.addStreetsLayer();

        // Add overlays
        //this.addCentroidLayer();
        this.addChoroplethLayer();
        this.addPolygonLayer();
        this.addTilesLayers();
        this.addOrganizersLayer();

        // Add controls
        this.addLayersControl();
        this.addEmailParticipantsControl();

        // Add events
        this.addZoomEvents();

        // Update filters when they change
        this.on('filterschange', function (event) {
            this.filters = event.filters;
        }, this);
    },


    /*
    * Base layers
    */

    addStreetsLayer: function () {
        if (Django.context.debug) {
            this.streets = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(this);
        }
        else {
            this.streets = L.tileLayer('https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                mapboxId: this.options.mapboxId
            }).addTo(this);
        }
    },

    addSatelliteLayer: function (add) {
        this.satellite = new L.BingLayer(this.options.bingKey);
        if (add) this.satellite.addTo(this);
    },


    /*
    * Overlay layers
    */


    /*
    * Tiles layers
    */

    addTilesLayers: function () {
        this.addPointPrivateTilesLayer();
        this.addPointPrivateGridLayer();
        this.addPointPublicTilesLayer();
        this.addPointPublicGridLayer();
        this.addPointInUseTilesLayer();
        this.addPointInUseGridLayer();
    },

    addGridLayer: function (baseUrl) {
        if (!baseUrl) return;
        var instance = this;
        var url = baseUrl + '{z}/{x}/{y}.json?callback={cb}';
        var gridLayer = new L.UtfGrid(url, {
            resolution: this.options.gridResolution,
        });
        if (instance.options.clickHandler) {
            gridLayer.on('click', function (e) {
                e.targetType = 'utfgrid';
                instance.options.clickHandler(e);
            });
        }
        instance.addLayer(gridLayer);
        return gridLayer;
    },

    addPointPrivateTilesLayer: function () {
        if (!(this.options.enablePointPrivateTiles && this.viewType === 'tiles')) return;
        if (!this.options.pointPrivateTilesBaseUrl) return;

        var url = this.options.pointPrivateTilesBaseUrl + '{z}/{x}/{y}.png';
        this.tilesPointPrivate = L.tileLayer(url, {
            zIndex: 10,
            // TODO maxZoom
        }).addTo(this);
        this.tileLayers.private.push(this.tilesPointPrivate);
        this.tileLayers['not in use'].push(this.tilesPointPrivate);
    },

    addPointPrivateGridLayer: function () {
        if (!(this.options.enablePointPrivateTiles && this.viewType === 'tiles')) return;
        this.gridPointPrivate = this.addGridLayer(this.options.pointPrivateGridBaseUrl);
        this.tileLayers.private.push(this.gridPointPrivate);
        this.tileLayers['not in use'].push(this.gridPointPrivate);
        this.addLayer(this.gridPointPrivate);
    },

    addPointPublicTilesLayer: function () {
        if (!(this.options.enablePointPublicTiles && this.viewType === 'tiles')) return;
        if (!this.options.pointPublicTilesBaseUrl) return;

        var url = this.options.pointPublicTilesBaseUrl + '{z}/{x}/{y}.png';
        this.tilesPointPublic = L.tileLayer(url, {
            zIndex: 12,
            // TODO maxZoom
        }).addTo(this);
        this.tileLayers.public.push(this.tilesPointPublic);
        this.tileLayers['not in use'].push(this.tilesPointPublic);
    },

    addPointPublicGridLayer: function () {
        if (!(this.options.enablePointPublicTiles && this.viewType === 'tiles')) return;
        this.gridPointPublic = this.addGridLayer(this.options.pointPublicGridBaseUrl);
        this.tileLayers.public.push(this.gridPointPublic);
        this.tileLayers['not in use'].push(this.gridPointPublic);
    },

    addPointInUseTilesLayer: function () {
        if (!(this.options.enablePointInUseTiles && this.viewType === 'tiles')) return;
        if (!this.options.pointInUseTilesBaseUrl) return;

        var url = this.options.pointInUseTilesBaseUrl + '{z}/{x}/{y}.png';
        this.tilesPointInUse = L.tileLayer(url, {
            zIndex: 14,
            // TODO maxZoom
        }).addTo(this);
        this.tileLayers['in use'].push(this.tilesPointInUse);
    },

    addPointInUseGridLayer: function () {
        if (!(this.options.enablePointInUseTiles && this.viewType === 'tiles')) return;
        this.gridPointInUse = this.addGridLayer(this.options.pointInUseGridBaseUrl);
        this.tileLayers['in use'].push(this.gridPointInUse);
    },

    showTiles: function () {
        var instance = this;
        if (instance.filters.organizing === 'only') return;
        if (instance.viewType !== 'tiles') return;
        var filtered = _.size(instance.filters) > 0,
            activeOwnerTypes = instance.getActiveOwnerTypes(instance.filters),
            projects = instance.filters.projects;

        _.each(_.keys(instance.tileLayers), function (layer) {
            // Always show if there are no current filters
            if (!filtered) {
                instance.showTilesByLayer(layer);
                return;
            }

            // Handle 'in use' layers
            if (layer === 'in use' && (projects === 'include' || projects === 'only')) {
                instance.showTilesByLayer(layer);
                return;
            }

            // Handle project layer
            if (_.contains(activeOwnerTypes, layer) && projects !== 'only') {
                instance.showTilesByLayer(layer);
                return;
            }

            if (layer !== 'not in use') {
                instance.hideTilesByLayer(layer);
                return;
            }
        });
    },

    hideTiles: function () {
        var instance = this;
        _.each(_.keys(instance.tileLayers), function (layer) {
            instance.hideTilesByLayer(layer);
        });
    },

    showTilesByLayer: function (name) {
        var instance = this;
        _.each(instance.tileLayers[name], function (layer) {
            if (layer) {
                instance.addLayer(layer);
            }
        });
    },

    hideTilesByLayer: function (name) {
        var instance = this;
        _.each(instance.tileLayers[name], function (layer) {
            if (layer) {
                instance.removeLayer(layer);
            }
        });
    },

    getActiveOwnerTypes: function (filters) {
        var activeOwnerTypes = filters.owner__owner_type__in;
        if (!activeOwnerTypes) {
            return [];
        }
        else if (!_.isArray(activeOwnerTypes)) {
            return [activeOwnerTypes,];
        }
        return activeOwnerTypes;
    },

    /*
    * Update which tiles are shown by owner type
    */
    reloadTiles: function (filters) {
        var instance = this;
        this.filters = filters;
        if (filters.organizing === 'only') {
            this.hideTiles();
        }
        else {
            this.showTiles();
        }
    },


    /*
    * Polygons
    */

    addPolygonLayer: function (queryString) {
        if (!queryString) {
            queryString = this.options.polygonQueryString;
        }
        if (!(this.options.enablePolygons && this.options.polygonBaseUrl)) return;
        if (!this.polygons) {
            this.polygons = L.polygonLotLayer(this.options.polygonBaseUrl, {});
        }
        this.polygons.addTo(this);
    },


    /*
     * Centroids
     */

    addCentroidLayer: function (queryString) {
        if (!(this.options.enableCentroids && this.options.centroidBaseUrl)) return;
        if (!this.centroids) {
            this.centroids = L.centroidLotLayer(this.options.centroidBaseUrl);
        }
        this.centroids.addTo(this);
    },

    showCentroidLayer: function () {
        this.addLayer(this.centroids);
    },

    hideCentroidLayer: function () {
        if (this.centroids) {
            this.removeLayer(this.centroids);
        }
    },


    /*
     * Organizers
     */

    addOrganizersLayer: function () {
        var instance = this,
            url = instance.options.centroidBaseUrl + '?' + [
                'projects=include',
                'participant_types=organizers',
                'owner__owner_type__in=private',
                'owner__owner_type__in=public'
            ].join('&');
        $.getJSON(url, function (data) {
            instance.organizers = L.geoJson(data, {
                onEachFeature: function (feature, layer) {
                    layer.on('click', function (event) {
                        instance.options.clickHandler(event, feature);
                        instance.fire('lotclicked', {
                            event: event,
                            lot: feature,
                        });
                    });
                },
                pointToLayer: function (feature, latlng) {
                    return L.organizerMarker(latlng);
                },
                style: function (feature) {
                    var style = lotStyles.forLayer(feature.properties.layer);
                    style.clickable = true;
                    return style;
                }
            }).addTo(instance);
        });

        // When filters change, update this layer too
        this.on('filterschange', function (event) {
            if (this.organizers) {
                // Handle owners
                var ownerFilters = event.filters.owner__owner_type__in,
                    projectsFilter = event.filters.projects;
                if (!ownerFilters) {
                    ownerFilters = [];
                }
                else if (!_.isArray(ownerFilters)) {
                    ownerFilters = [ownerFilters];
                }
                this.organizers.eachLayer(function (layer) {
                    var lotLayer = layer.feature.properties.layer;
                    if (lotLayer === 'in use' || _.contains(ownerFilters, lotLayer)) {
                        layer.show();
                    }
                    else {
                        layer.hide();
                    }

                    // Handle projects
                    if (event.filters.projects === 'only' && lotLayer !== 'in use') {
                        // Hide everything not 'in use'
                        layer.hide();
                    }
                    else if (projectsFilter === 'exclude' && lotLayer === 'in use') {
                        // Hide everything 'in use'
                        layer.hide();
                    }
                });
            }
        }, this);
    },


    /*
    * Choropleth
    */

    showChoropleth: function () {
        var instance = this;
        if (!instance.choropleth) {
            instance.addChoroplethBoundaries(instance.filters.choropleth_boundary_layer);
        }
        else {
            instance.addLayer(instance.choropleth);
        }
    },

    hideChoropleth: function () {
        var instance = this;
        if (instance.choropleth) {
            instance.removeLayer(instance.choropleth);
        }
    },

    reloadChoropleth: function (filters) {
        this.addChoroplethLayer(filters);
    },

    clearChoropleth: function () {
        var instance = this;
        instance.hideChoropleth();
        instance.choropleth = null;
        instance.choroplethLayers = {};
    },

    addChoroplethBoundaries: function (layer_name) {
        var instance = this;
        instance.choroplethBoundaryLayerName = layer_name;
        var url = Django.url('inplace:layer_view', { name: layer_name });
        instance.choroplethLayers = {};
        instance.fire('dataloading');
        singleminded.remember({
            name: 'addChoroplethBoundaries',
            jqxhr: $.getJSON(url, function (data) {
                instance.choropleth = L.geoJson(data, {
                    onEachFeature: function (feature, layer) {
                        var boundaryLabel = feature.properties.boundary_label;
                        instance.choroplethLayers[boundaryLabel] = layer;

                        layer.on({
                            click: function () {
                                // Zoom to this polygon? Maybe show other
                                // details besides count (breakdown, area,
                                // etc.)? TODO
                            },
                        });
                    },
                });
                instance.updateChoroplethStyles(null);
                if (instance.getZoom() < 16 && instance.viewType === 'choropleth') {
                    instance.choropleth.addTo(instance);
                }

                instance.updateChoropleth($.param(instance.filters, true));
            })
            .always(function () {
                instance.fire('dataload');
            }),
        });
    },

    getChoroplethColor: function (count, maxCount) {
        var instance = this;
        var hue = instance.choroplethHsl.hue,
            saturation = instance.choroplethHsl.saturation,
            lightness = instance.choroplethHsl.lightness;

        if (maxCount > 0) {
            // Keep lightness between 30 and 90
            lightness -= (count / maxCount) * 60;
        }
        return 'hsl(' + hue + ', ' + saturation + '%, ' + lightness + '%)';
    },

    getChoroplethStyle: function (count, maxCount) {
        var instance = this;
        var style = instance.choroplethStyle;
        style.fillColor = instance.getChoroplethColor(count, maxCount);
        return style;
    },

    updateChoroplethStyles: function (counts) {
        var instance = this;
        if (!instance.choroplethLayers) return;
        var maxCount = 0;

        if (counts && counts !== null) {
            $.each(counts, function (layerLabel, count) {
                maxCount = Math.max(maxCount, count);
            });
        }

        $.each(instance.choroplethLayers, function (label, layer) {
            var style = {};
            if (counts && counts !== null) {
                style = instance.getChoroplethStyle(counts[label], maxCount);
            }
            else {
                style = instance.getChoroplethStyle(0, 0);
            }
            layer.setStyle(style);
        });

    },

    updateChoroplethLabels: function (counts) {
        var instance = this;

        $.each(counts, function (layerLabel, count) {
            var layer = instance.choroplethLayers[layerLabel];
            var label = layer._label;
            var content = instance.choroplethBoundaryLayerName.slice(0, -1);
            content += ' ' + layerLabel + '<br/ >' + count + ' lots';
            if (label) {
                layer.updateLabelContent(content);
            }
            else {
                layer.bindLabel(content);
            }
        });
    },

    addChoroplethLayer: function (filters) {
        var instance = this;
        if (!instance.options.enableChoropleth) return;

        var newLabel;
        var queryString = instance.options.choroplethQueryString;
        if (filters) {
            newLabel = filters.choropleth_boundary_layer;
            queryString = $.param(filters, true);
        }

        // If boundaries don't yet exist or are new, load them
        if ((!instance.choropleth && newLabel) ||
            (newLabel && newLabel !== instance.choroplethBoundaryLayerName)) {
            instance.clearChoropleth();
            instance.addChoroplethBoundaries(newLabel);
        }
        else {
            instance.updateChoropleth(queryString);
        }
    },

    updateChoropleth: function (queryString) {
        var instance = this;

        // Update colors and labels
        var url = instance.options.choroplethBaseUrl + '?' + queryString;
        instance.fire('dataloading');
        singleminded.remember({
            name: 'addChoroplethLayer',
            jqxhr: $.getJSON(url, function (data) {
                instance.updateChoroplethStyles(data);
                instance.updateChoroplethLabels(data);
            })
            .always(function () {
                instance.fire('dataload');
            }),
        });

    },

    setVisibleLotsCount: function (count) {
        this.visibleLotsCount = count;
        this.pickChoroplethLayer();
    },

    /*
     * Determine the choropleth / summary view layer that should be
     * displayed. If it won't be too many lots, show centroids.
     */
    pickChoroplethLayer: function () {
        var instance = this;
        if (instance.viewType === 'choropleth') {
            if (instance.visibleLotsCount <= instance.options.lotsCentroidThreshold) {
                instance.hideChoropleth();
                instance.showCentroidLayer();
            }
            else {
                instance.hideCentroidLayer();
                instance.showChoropleth();
            }
        }
    },


    /*
    * Controls
    */

    addLayersControl: function () {
        if (!this.options.enableLayersControl) return;
        var baseLayers = {
            'Streets': this.streets,
            'Satellite': this.satellite,
        };
        var overlays = {};
        var layersControl = L.control.layers(baseLayers, overlays).addTo(this);
    },

    addEmailParticipantsControl: function () {
        if (Django.user.is_superuser ||
                Django.user.has_perm('phillyorganize.email_organizers')) {
            L.control.emailParticipants({}).addTo(this);
        }
    },


    /*
    * Events
    */

    addZoomEvents: function () {
        this.on('zoomend', function () {
            var zoom = this.getZoom();
            if (zoom >= 16) {
                this.hideChoropleth();
            }

            if (zoom >= 17) {
                this.hideTiles();

                if (this.organizers) {
                    this.removeLayer(this.organizers);
                }
            }
            else {
                this.showTiles();

                if (this.organizers) {
                    this.addLayer(this.organizers);
                }
            }
        }, this);
    },


    /*
    * Filters
    */

    updateFilters: function (filters) {
        this.filters = filters;

        // If the view type is changing, let the map know
        if (filters.view_type && filters.view_type !== this.viewType) {
            this.changeView(filters.view_type);
        }

        // Now, reload everything
        this.reloadChoropleth(filters);
        this.reloadTiles(filters);

        this.fire('moveend').fire('zoomend');
    },

    changeView: function (viewType) {
        this.viewType = viewType;
        this.fire('viewtypechange', { viewType: viewType });
        if (viewType === 'tiles') {
            // Show tiles
            this.showTiles();

            // Hide everything else
            this.hideChoropleth();
        }
        else if (viewType === 'choropleth') {
            // Show choropleth
            this.showChoropleth();

            // Hide everything else
            this.hideTiles();
        }
    },

    /*
     * Parcels
     */
    getParcelPopupContent: function (layer, feature) {
        var content = '<div class="friendlyowners-popup"><h1>',
            address = feature.properties.address || 'unknown address',
            url = Django.url('friendlyowners:add') + '?' + $.param({ parcels: feature.id });
        content += address + '</h1><div><a href="' + url + '" target="_blank" class="btn btn-default">Add parcel</a></div></div>';
        return content;
    },

    /*
     * Get params, encoded to be added to a query string when getting counts
     * for lots on a map or other occasions.
     */
    getParamsQueryString: function (extend) {
        var params = L.extend({}, this.filters, extend);
        return $.param(params, true);
    }

});

L.Map.addInitHook('_lotMapInitialize');

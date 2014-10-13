/*
 * Module for all pages derived from the base lot page.
 */
var L = require('leaflet');
var lotStyles = require('./lotstyles');
var streetview = require('./streetview');
require('bootstrap_tooltip');

var lotPk;

function styleLayer(feature) {
    var style = lotStyles.forLayer(feature.properties.layer);
    if (+feature.properties.pk !== lotPk) {
        style.fillOpacity = 0.3;
        style.weight = 0.5;
    }
    else {
        style.fillOpacity = 1;
        style.weight = 3;
    }
    return style;
}

function addBaseLayer(map) {
    if (Django.context.debug) {
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);
    }
    else {
        L.tileLayer('https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            mapboxId: $('#map').data('mapboxid')
        }).addTo(map);
    }
}

$(document).ready(function () {
    if ($('.lot-base-page').length > 0) {
        var $streetviewContainer = $('#streetview-container'),
            $streetviewError = $('#streetview-error'),
            lon = $('body').data('lon'),
            lat = $('body').data('lat');

        lotPk = $('body').data('lotpk');

        // Set up streetview
        streetview.load_streetview(lon, lat, $streetviewContainer, $streetviewError);

        // Set up lot map
        var map = new L.Map('map', {
            center: { lat: lat, lng: lon },
            mapboxId: $('#map').data('mapboxid'),
            zoom: 17
        });

        addBaseLayer(map);

        $.get($('#map').data('url'), function (data) {
            var feature_layer = new L.GeoJSON(data, { style: styleLayer })
                .addTo(map);
        });

        $('.lot-page-tooltip').tooltip({ container: 'body' });
    }
});

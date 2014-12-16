var friendlyowners = require('livinglots.parcels');
var L = require('leaflet');

$(document).ready(function () {
    if ($('.add-friendlyowner').length > 0) {
        var parcelMap = L.map('friendlyowner-parcel-map', {}),
            parcelPk = $(':input[name=parcels]').val(),
            url = Django.url('waterdept:waterparcel_detail_geojson', { pk: parcelPk });
        $.getJSON(url, function (data) {
            console.log(data);
            var parcelLayer = L.geoJson(data, {
                style: function () {
                    return {
                        clickable: false,
                        color: 'green',
                        fillColor: 'green'
                    };
                }
            }).addTo(parcelMap);
            parcelMap.fitBounds(parcelLayer.getBounds());
        });
    }
});

module.exports = {
    init: function (map) {
        $('.map-friendlyowners-activate').click(function () {
            if (map.getZoom() < 17) {
                alert('Zoom in a bit more to pick a parcel');
            }
            $('.map-friendlyowners').addClass('active');
            friendlyowners.init(map);
            return false;
        });

        $('.map-friendlyowners-cancel').click(function () {
            $('.map-friendlyowners').removeClass('active');
            friendlyowners.exit(map);
            return false;
        });
    }
};

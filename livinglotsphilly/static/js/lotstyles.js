var _ = require('underscore');

var layerFills = {
    'in use': '#830F94',
    'public': '#D38022',
    'private': '#287A68'
};

var defaultStyle = {
    fillOpacity: 0.7,
    color: 'white',
    opacity: 0.8,
    weight: 1
};

function forLayer(layer) {
    var style = $.extend({}, defaultStyle);
    if (layerFills[layer]) {
        style.fillColor = layerFills[layer];
    }
    return style;
}

module.exports = {
    forLayer: forLayer,

    layers: function () {
        var layers = {};
        _.each(layerFills, function (fill, name) {
            layers[name] = forLayer(name);
        });
        return layers;
    }
};

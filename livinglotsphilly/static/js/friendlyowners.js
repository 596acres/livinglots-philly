var friendlyowners = require('livinglots.friendlyowners');

module.exports = {
    init: function (map) {
        $('.map-friendlyowners').click(function () {
            if (map.getZoom() < 16) {
                alert('Zoom in a bit more first');
            }
            else {
                friendlyowners.init(map);
            }
            return false;
        });
    }
};

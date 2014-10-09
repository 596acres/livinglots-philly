var geocode = require('./geocode').geocode;
var Spinner = require('spinjs');

function addCityAndState(query, options) {
    var city = options.city.toLowerCase();
    if (query.toLowerCase().indexOf(city) <= 0) {
        query += ', ' + city;
    }

    var state = options.state.toLowerCase();
    if (query.toLowerCase().indexOf(state) <= 0) {
        query += ', ' + state;
    }
    return query;
}

function searchByAddress($elem, options) {
    $elem.find(options.warningSelector).hide();

    var $submit = $elem.find(':input[type=submit]').attr('disabled', 'disabled'),
        spinner = new Spinner({}).spin($submit[0]);

    var query = $elem.find('input[type="text"]').val();
    query = addCityAndState(query, options);

    geocode(query, options.bounds, options.state, function (result, status) {
        // Done searching
        $submit.removeAttr('disabled');
        spinner.stop();

        // Is result valid?
        if (result === null) {
            $elem.find(options.warningSelector)
                .text(options.errorMessage)
                .show();
            return;
        }

        // Let the world know!
        var found_location = result.geometry.location;
        $elem.trigger('searchresultfound', [{
            longitude: found_location.lng(),
            latitude: found_location.lat(),
            query_address: query,
            found_address: result.formatted_address,
        }]);
    });
}

var defaultOptions = {
    bounds: null,
    city: null,
    state: null,
    errorMessage: null,
    warningSelector: null,
};

(function ($) {
    $.fn.searchbar = function (passedOptions) {
        var options = $.extend({}, defaultOptions, passedOptions),
            $elem = this;

        this.keypress(function (e) {
            if (e.keyCode === '13') {
                e.preventDefault();
                instance.searchByAddress();
                return false;
            }
        });
        this.find('form').submit(function (e) {
            e.preventDefault();
            searchByAddress($elem, options);
            return false;
        });
        return this;
    };
} (jQuery));

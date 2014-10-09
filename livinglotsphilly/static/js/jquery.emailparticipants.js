require('jquery.form');
var Spinner = require('spinjs');


var defaultOptions = {
    filterContainer: null
};

function show($container) {
    var spinner = new Spinner({}).spin($container[0]);
    $container.show()
        .load(Django.url('extraadmin:mail_participants'), function() {
            spinner.stop();
            _initializeForm($container);
            _updateCounts($container);
        });
}

function hide($container) {
    $container.hide();
}

function _initializeForm($container) {
    _updateCounts($container);
    var spinner = new Spinner({});
    $container.find('form')
        .ajaxForm({
            target: $container,
            success: function() {
                // Initialize again in case the form was sent back due 
                // to validation
                _initializeForm($container);
                spinner.stop();
            },
        })
        .submit(function() {
            spinner.spin($container[0]);
        });
}

function _updateCounts($container) {
    var url = Django.url('extraadmin:mail_participants_count') + '?' +
        $container.find(':input[name=filters]').val();
    $.getJSON(url, function(data) {
        $container.find('.organizer-count').text(data.organizers);
        $container.find('.watcher-count').text(data.watchers);
    });
}

function _updateFilters($container, filters) {
    $container.find(':input[name=filters]').val($.param(filters, true));
}


(function ($) {
    $.fn.emailparticipants = function (passedOptions) {
        var options = $.extend({}, defaultOptions, passedOptions),
            $elem = this;

        // Add our container
        var $container = $('<div></div>').addClass('email-participants-container');
        $elem.after($container);

        options.filterContainer.on('filterschange', function(e) {
            _updateFilters($container, e.filters);
            _updateCounts($container);
        });

        // Show form on click
        $elem.click(function() {
            if (!$container.is(':visible')) {
                show($container);
            }
            else {
                hide($container);
            }
            return false;
        });
    };
} (jQuery));

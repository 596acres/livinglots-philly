var _ = require('underscore');
var Spinner = require('spinjs');
require('jquery.timeago');


function createActivityItem(activity) {
    var $item = $('<div></div>')
        .addClass('activity-stream-list-item')
        .addClass(activity.type);

    // Append HTML of the activity
    $item.append($.parseHTML(activity.html));

    // Append timeago timestamp
    $item.append($('<time></time>')
        .addClass('timeago')
        .attr('datetime', activity.time));

    return $item;
}

function loadActivities($elem, filters, page) {
    var params = _.extend({}, filters, { 'page': page }),
        url = Django.url('activity_stream_combined') + '?' + $.param(params),
        spinner = new Spinner({}).spin($elem[0]);

    $.getJSON(url, function (activities) {
        spinner.stop();

        // Append activities to our stream
        $.each(activities, function (i, activity) {
            $elem.append(createActivityItem(activity));
        });

        // Fix timestamps up
        $('.timeago').timeago();
    });
}

function initActivityStream($elem, filters) {
    var page = 1;
    loadActivities($elem, filters, page);
    $elem.scroll(function () {
        var height = $(this).innerHeight(),
            distanceToBottom = $(this)[0].scrollHeight - height - $(this).scrollTop();
        if (distanceToBottom < height) {
            loadActivities($elem, filters, ++page);
        }    
    });
}

(function ($) {
    $.fn.activitystream = function (options) {
        initActivityStream(this, options);
        return this;
    };
} (jQuery));

/*
 * Module for the add organizer page.
 */
function toggle_cbo_fields(show) {
    var $cbo_fields = $(':input[name="facebook_page"],:input[name="url"]').parents('.control-group');
    if (show) {
        $cbo_fields.show();
    }
    else {
        $cbo_fields.hide();
    }
}

function is_cbo() {
    return ($(':input[name="type"] :selected').text() === 'community based organization');
}

$(document).ready(function () {
    if ($('.add-organizer-page').length > 0) {
        toggle_cbo_fields(is_cbo());

        $(':input[name="type"]').change(function () {
            toggle_cbo_fields(is_cbo());
        });
    }
});

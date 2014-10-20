//
// main.js
//
// Scripts that should run on every page.
//

require('./jquery.activitystream');
require('chosen');
require('bootstrap_dropdown');
require('fancybox');
require('noisy');


/*
 * Global form-related scripts
 */
$(document).ready(function () {
    /*
     * Disable submit buttons on forms once they have been submitted once.
     */
    $('form').submit(function () {
        $(this).find('input[type="submit"]').attr('disabled', 'disabled');
    });

    $('body').noisy({
        'intensity' : 0.5,
        'size' : 100,
        'opacity' : 0.15,
        'fallback' : '',
        'monochrome' : false
    });

    /*
     * Collapse the collapsible sections
     */
    // Slide up those sections not initially expanded
    $('.collapsible-section:not(.is-expanded) .collapsible-section-text').slideUp();

    // Prepare headers for clicking
    $('.collapsible-section-header').click(function () {
        var $section = $(this).parent(),
            $sectionText = $section.find('.collapsible-section-text');
        $section.toggleClass('is-expanded');
        $sectionText.slideToggle();
    });

    /*
     * Fancy the fancyboxes
     */
    $('.fancybox').fancybox();

    /*
     * Activate the activitystreams
     */
    $('.activity-stream-container').activitystream();

});


/*
 * Page-specific modules
 */
require('./mappage');
require('./lotbasepage');
require('./addorganizerpage');
require('./mailparticipantspage');

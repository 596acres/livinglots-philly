requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'jquery': '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min',
        'jquery.infinitescroll': 'lib/jquery.infinitescroll.min',
        'fancybox': 'lib/fancybox/jquery.fancybox.pack',
        'leaflet': '//cdn.leafletjs.com/leaflet-0.5.1/leaflet',
        'async': 'lib/async',
    },
    shim: {
        'leaflet': {
            exports: 'L',
        },
        'lib/leaflet.lvector': {
            deps: ['leaflet'],
            exports: 'lvector',
        },
        'Leaflet.Bing': ['leaflet'],
        'lib/leaflet.label': ['leaflet'],
        'chosen.jquery.min': ['jquery'],
        'chosen.jquery_ready': ['jquery', 'chosen.jquery.min'],
    },
});

// Load the main app module to start the app
requirejs(['main']);

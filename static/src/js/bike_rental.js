odoo.define('bike_rental.frontend', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.BikeRentalWidget = publicWidget.Widget.extend({
        selector: '#rentalForm',
        events: {
            'submit': '_onSubmit',
        },

        start: function () {
            var self = this;
            self._super.apply(this, arguments);
            console.log("BikeRentalWidget started");
            if (!$('link[href*="bike_rental.css"]').length) {
                $('head').append('<link rel="stylesheet" href="/bike_rental/static/src/css/bike_rental.css">');
                console.log("Loaded bike_rental.css manually");
            }
            return this._loadAssets();
        },

        _loadAssets: function () {
            var self = this;
            var $script = $('script[src*="bike_rental.js"]');
            if ($script.length) {
                console.log("bike_rental.js loaded successfully");
            } else {
                console.error("bike_rental.js not found in DOM");
            }
        },

        _onSubmit: function (ev) {
            var $form = $(ev.currentTarget);
            var duration = $form.find('#modalDuration').val();
            var startDate = $form.find('#modalStartDate').val();
            if (parseInt(duration) < 1) {
                ev.preventDefault();
                alert(_t('Duration must be at least 1 day.'));
            }
            if (new Date(startDate) < new Date()) {
                ev.preventDefault();
                alert(_t('Start date cannot be in the past.'));
            }
        },
    });

    return publicWidget.registry.BikeRentalWidget;
});

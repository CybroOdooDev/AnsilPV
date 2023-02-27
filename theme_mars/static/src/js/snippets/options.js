odoo.define('theme_mars.mars_pie_chart_options', function (require) {
    'use strict';
    const core = require('web.core');
    const utils = require('web.utils');
    const options = require('web_editor.snippets.options');

    options.registry.pieChartSnippets = options.Class.extend({
         init: function () {
                this._super(...arguments);
                this.progressBarValue()
                this._computeWidgetState()
         },
         progressBarValue: function (previewMode, widgetValue, params) {

             let value = parseInt(widgetValue);
             value = utils.confine(value, 0, 100);
             const $progressBar = this.$target.find('.charts');
             const $progressBarText = this.$target.find('.percent');
             // Target precisely the XX% not only XX to not replace wrong element
             // eg 'Since 1978 we have completed 45%' <- don't replace 1978
             $progressBarText.text($progressBarText.text().replace(/[0-9]+%/, value + '%'));
             $progressBar.attr("data-percent", value);
         },

         _computeWidgetState: function (methodName, params) {
             switch (methodName) {
                 case 'progressBarValue': {
                     return this.$target.find('.progress-bar').attr('data-percent') + '%';
                 }
             }
             return this._super(...arguments);
         },

    });
});

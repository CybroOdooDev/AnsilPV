odoo.define('theme_mars.theme_mars', function (require) {
	"use strict";

var $window = $('#wrapwrap');

function run()
{
	var fName = arguments[0],
		aArgs = Array.prototype.slice.call(arguments, 1);
	try {
		fName.apply('#wrapwrap', aArgs);
	} catch(err) {
	}
};

/* chart
================================================== */
function _chart ()
{
	$('.b-skills').appear(function() {
		setTimeout(function() {
			$('.charts').easyPieChart({
                         delay: 5000,
                         barColor: '#369670',
                         trackColor: '#f2f2f2',
                         scaleColor: false,
                         lineWidth: 5,
                         trackWidth: 5,
                         size: 100,
                         animate:3000,

                         lineCap: 'square',
                         onStep: function (from, to, percent) {
                             this.el.children[0].innerHTML = Math.round(percent);
                         }
                    });

		}, 100);
	});
};



$(document).ready(function() {
	run(_chart);

	/* Progress Bar */
    var delay = 500;
    $(".progress-bar").each(function (i) {
        $(this).delay(delay * i).animate({ width: $(this).attr('aria-valuenow') + '%' }, delay);
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: delay,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now) + '%');
            }
        });
    });
});

});
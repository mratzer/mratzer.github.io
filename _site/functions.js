let marrat = (function () {
	"use strict";

	function toggleScheme() {
		for (let styleSheet = 0; styleSheet < document.styleSheets.length; styleSheet++) {
			for (let sheetRule = 0; sheetRule < document.styleSheets[styleSheet].cssRules.length; sheetRule++) {
				let rule = document.styleSheets[styleSheet].cssRules[sheetRule];

				if (rule && rule.media && rule.media.mediaText.includes('prefers-color-scheme')) {
					let oldMediaText = rule.media.mediaText;
					let newMediaText;

					if (oldMediaText.includes('light')) {
						newMediaText = oldMediaText.replace('light', 'dark');
					}
					if (oldMediaText.includes('dark')) {
						newMediaText = oldMediaText.replace('dark', 'light');
					}
					rule.media.deleteMedium(oldMediaText);
					rule.media.appendMedium(newMediaText);
				}
			}
		}
	}

	function createSchemeToggler() {
		let schemeToggler = document.createElement('p');

		schemeToggler.className = 'scheme-toggler';
		schemeToggler.innerHTML = '&#9681;';
		schemeToggler.title = 'Switch color scheme';
		schemeToggler.addEventListener('click', function(e) {
			toggleScheme();
		});

		return schemeToggler;
	}

	return {
		createSchemeToggler: createSchemeToggler
	};

}());

window.onload = function (ev) {
	"use strict";

	let schemeToggler = marrat.createSchemeToggler();

	if (schemeToggler) {
		document.getElementsByTagName('header')[0].appendChild(schemeToggler);
	}
};

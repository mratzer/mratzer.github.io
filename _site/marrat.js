const marrat = (function () {
	"use strict";

	let lastScroll = 0;

	const scheme = loadSchemeData();

	function loadSchemeData() {
		const rules = [];

		for (let styleSheet = 0; styleSheet < document.styleSheets.length; styleSheet++) {
			for (let sheetRule = 0; sheetRule < document.styleSheets[styleSheet].cssRules.length; sheetRule++) {
				const rule = document.styleSheets[styleSheet].cssRules[sheetRule];

				if (rule && rule.media && rule.media.mediaText.includes('prefers-color-scheme')) {
					rules.push(rule);
				}
			}
		}

		const systemScheme = getSystemScheme();

		return {
			rules: rules,
			system: systemScheme,
			current: systemScheme
		};
	}

	function getSystemScheme() {
		if(window.matchMedia('(prefers-color-scheme: dark)').matches) {
			return 'dark';
		} else {
			return 'light';
		}
	}

	function loadAndApplyScheme() {
		const storedScheme = localStorage.getItem("scheme");

		if (storedScheme && storedScheme != scheme.system) {
			toggleScheme();
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

	function toggleScheme() {
		scheme.rules.forEach((rule) => {
			const oldMediaText = rule.media.mediaText;
			let newMediaText;

			if (oldMediaText.includes('light')) {
				newMediaText = oldMediaText.replace('light', 'dark');
			}
			if (oldMediaText.includes('dark')) {
				newMediaText = oldMediaText.replace('dark', 'light');
			}
			rule.media.deleteMedium(oldMediaText);
			rule.media.appendMedium(newMediaText);
		});

		if (scheme.current === 'light') {
			scheme.current = 'dark';
		} else {
			scheme.current = 'light';
		}

		if (scheme.current === scheme.system) {
			localStorage.removeItem("scheme");
		} else {
			localStorage.setItem("scheme", scheme.current);
		}
	}

	function addHeaderToggler(header) {
		header.classList.add('sticky');

		window.addEventListener('scroll', () => {
			const currentScroll = window.scrollY;

			if (currentScroll > lastScroll && currentScroll > 100) {
				header.classList.add('hidden');
			} else {
				header.classList.remove('hidden');
			}

			lastScroll = currentScroll;
		}, {
			passive: true
		});
	}

	return {
		loadAndApplyScheme: loadAndApplyScheme,
		createSchemeToggler: createSchemeToggler,
		addHeaderToggler: addHeaderToggler
	};

}());

window.onload = function (ev) {
	"use strict";

	const header = document.getElementsByTagName('header')[0];

	if (header) {
		const schemeToggler = marrat.createSchemeToggler();

		if (schemeToggler) {
			header.appendChild(schemeToggler);
		}

		marrat.addHeaderToggler(header);
	}
};

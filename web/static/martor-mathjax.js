jQuery(function ($) {
	$(document).on("martor:preview", function (e, $content) {
		function update_math() {
			MathJax.typesetPromise([$content[0]]).then(function () {
				$content.find(".tex-image").hide();
				$content.find(".tex-text").show();
			});
		}

		if (!("MathJax" in window)) {
			window.MathJax = {
				tex: {
					inlineMath: [
						["$", "$"],
						["\\(", "\\)"],
					],
				},
				options: {
					enableMenu: false,
				},
				startup: {
					typeset: false,
				},
			};

			$.ajax({
				type: "GET",
				url: "https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-chtml.min.js",
				dataType: "script",
				cache: true,
				success: update_math,
			});
		} else {
			update_math();
		}
	});
});

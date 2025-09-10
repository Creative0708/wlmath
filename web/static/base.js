const inputs = Array.from(document.querySelectorAll("input[type=password]"));
let toggled = false;
for (const input of inputs) {
	const container = document.createElement("div");
	const visibilityButton = document.createElement("button");
	container.className = "password-visibility-container";
	visibilityButton.type = "button";

	visibilityButton.addEventListener("click", () => {
		toggled = !toggled;
		inputs.forEach((input) => (input.type = toggled ? "text" : "password"));
	});

	input.parentElement.replaceChild(container, input);
	container.append(input, visibilityButton);
}

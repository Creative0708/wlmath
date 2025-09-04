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
document.querySelectorAll("th.sortable").forEach((header) => {
  header.addEventListener("click", () => {
	const table = header.closest("table");
	const tbody = table.querySelector("tbody");
	const rows = Array.from(tbody.querySelectorAll("tr"));
	const index = Array.from(header.parentNode.children).indexOf(header);
	const asc = !header.classList.contains("asc");

	rows.sort((a, b) => {
	  const valA = a.children[index].innerText.trim();
	  const valB = b.children[index].innerText.trim();
	  return asc
		? valA.localeCompare(valB, undefined, { numeric: true })
		: valB.localeCompare(valA, undefined, { numeric: true });
	});

	tbody.innerHTML = "";
	rows.forEach((row) => tbody.appendChild(row));

	header.classList.toggle("asc", asc);
	header.classList.toggle("desc", !asc);
  });
});
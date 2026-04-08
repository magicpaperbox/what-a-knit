const categorySelect = document.getElementById("category");

if (categorySelect) {
    const subcategorySelect = document.getElementById("subcategory");

    function updateSubcategories() {
        const chosen = categorySelect.value;
        if (!chosen || !subcategories[chosen]) return;

        subcategorySelect.innerHTML = "";
        const optional = document.createElement("option");
        optional.value = "";
        optional.textContent = "-";
        subcategorySelect.appendChild(optional);
        for (const sub of subcategories[chosen]) {
            const option = document.createElement("option");
            option.value = sub;
            option.textContent = sub;
            subcategorySelect.appendChild(option);

        }

        // If we are editing, check if there is a saved subtype to select
        const savedSubtype = subcategorySelect.getAttribute('data-selected');
        if (savedSubtype) {
            subcategorySelect.value = savedSubtype;
            subcategorySelect.removeAttribute('data-selected');
        }
    }


    categorySelect.addEventListener("change", updateSubcategories);

    // Run once on page load (for Edit form)
    if (categorySelect.value) {
        updateSubcategories();
    }


    // Show/hide pattern details (language + designer)
    const hasPatternSelect = document.getElementById("has_pattern");
    const patternDetails = document.getElementById("pattern-details");

    hasPatternSelect.addEventListener("change", function () {
        if (hasPatternSelect.value === "yes") {
            patternDetails.hidden = false;
        } else {
            patternDetails.hidden = true;
        }
    });
}

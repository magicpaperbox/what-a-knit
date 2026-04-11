const patternsDataElement = document.getElementById("patterns-data");

if (patternsDataElement) {
    const patterns = JSON.parse(patternsDataElement.textContent);
    const initialSelectedPatternsElement = document.getElementById("initial-selected-patterns");
    const initialSelectedPatterns = initialSelectedPatternsElement
        ? JSON.parse(initialSelectedPatternsElement.textContent)
        : [];
    const searchInput = document.getElementById("patterns-search");
    const resultsContainer = document.getElementById("pattern-search-results");
    const selectedPatternsContainer = document.getElementById("selected-patterns");
    const hiddenInputContainer = document.getElementById("pattern-hidden-inputs");
    const selectedPatternsLabel = document.getElementById("selected-patterns-label");

    function updateLabelVisibility() {
        if (selectedPatternsContainer.childElementCount === 0) {
            selectedPatternsLabel.style.display = "none";
        }
        if (selectedPatternsContainer.childElementCount > 0) {
            selectedPatternsLabel.style.display = "block";
        }
    }

    function isPatternSelected(pattern) {
        const existingHiddenInput = hiddenInputContainer.querySelector(`input[name="pattern_id"][value="${pattern.id}"]`);
        return !!existingHiddenInput;
    }

    function deleteSelectedPattern(selectedElement, hiddenResultElement) {
        selectedElement.remove();
        hiddenResultElement.remove();
        updateLabelVisibility();
    }

    function registerSelectedElement(pattern) {
        const existingHiddenInput = hiddenInputContainer.querySelector(`input[name="pattern_id"][value="${pattern.id}"]`);
        if (existingHiddenInput) {
            return;
        }

        const hiddenResultElement = document.createElement("input");
        hiddenResultElement.type = "hidden";
        hiddenResultElement.name = "pattern_id";
        hiddenResultElement.value = pattern.id;
        hiddenInputContainer.appendChild(hiddenResultElement);

        const selectedElement = document.createElement("div");
        selectedElement.textContent = pattern.name;

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "x";
        deleteButton.type = "button";
        deleteButton.addEventListener("click", function () {
            deleteSelectedPattern(selectedElement, hiddenResultElement);
        });
        selectedElement.appendChild(deleteButton);

        selectedPatternsContainer.appendChild(selectedElement);
        updateLabelVisibility();
    }

    function createResultElement(pattern) {
        const resultElement = document.createElement("div");
        resultElement.textContent = pattern.name;

        resultElement.addEventListener("click", function () {
            resultElement.remove();
            registerSelectedElement(pattern);
        });
        return resultElement;
    }

    updateLabelVisibility();
    for (const pattern of initialSelectedPatterns) {
        registerSelectedElement(pattern);
    }

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.trim().toLowerCase();

        resultsContainer.innerHTML = "";

        if (query === "") {
            return;
        }

        const matchingPatterns = patterns.filter(function (pattern) {
            return pattern.name.toLowerCase().includes(query) && !isPatternSelected(pattern);
        });

        if (matchingPatterns.length === 0) {
            resultsContainer.innerHTML = "Nie mam nic";
            return;
        }

        for (const pattern of matchingPatterns.slice(0, 10)) {
            const resultElement = createResultElement(pattern);
            resultsContainer.appendChild(resultElement);
        }
    });

    searchInput.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            resultsContainer.innerHTML = "";
        }
    });
}

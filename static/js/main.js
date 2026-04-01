// ========== THEME TOGGLE ==========

function toggleTheme() {
    document.body.classList.toggle('dark');

    const isDark = document.body.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    const toggleText = document.querySelector('.toggle-text');
    toggleText.textContent = isDark ? 'Light mode' : 'Dark mode';
}

// On page load: restore saved theme
const saved = localStorage.getItem('theme');
if (saved === 'dark') {
    document.body.classList.add('dark');
    const toggleText = document.querySelector('.toggle-text');
    if (toggleText) toggleText.textContent = 'Light mode';
}

// ========== ADD PATTERN FORM ==========

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
            patternDetails.style.display = "block";
        } else {
            patternDetails.style.display = "none";
        }
    });
}

// ========== DELETE MODAL ==========
function openDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) modal.style.display = 'flex';
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) modal.style.display = 'none';
}

// Close modal if clicking outside the content box
window.addEventListener('click', function (event) {
    const modal = document.getElementById('deleteModal');
    // Check if modal exists
    if (modal && event.target === modal) {
        closeDeleteModal();
    }
});


// ========== PATTERN SEARCH ==========
const patternsDataElement = document.getElementById("patterns-data");

if (patternsDataElement) {
    const patterns = JSON.parse(patternsDataElement.textContent);
    const searchInput = document.getElementById("patterns-search");
    const resultsContainer = document.getElementById("pattern-search-results");
    const selectedPatternsContainer = document.getElementById("selected-patterns");
    const hiddenInputContainer = document.getElementById("pattern-hidden-inputs");
    const selectedPatternsLabel = document.getElementById("selected-patterns-label");

    function showHideLabel() {
        if (selectedPatternsContainer.childElementCount === 0) {
            selectedPatternsLabel.style.display = "none";
        }
        if (selectedPatternsContainer.childElementCount > 0) {
            selectedPatternsLabel.style.display = "block";
        }
    }

    showHideLabel();
    searchInput.addEventListener("input", function () {
        const query = searchInput.value.trim().toLowerCase();

        resultsContainer.innerHTML = "";

        if (query === "") {
            return;
        }

        const matchingPatterns = patterns.filter(function (pattern) {
            return pattern.name.toLowerCase().includes(query);
        });

        if (matchingPatterns.length === 0) {
            resultsContainer.innerHTML = "Nie mam nic";
            return;
        }

        for (const pattern of matchingPatterns.slice(0, 10)) {
            const resultElement = createResultElement(pattern);
            resultsContainer.appendChild(resultElement);
        }

        function createResultElement(pattern) {
            const resultElement = document.createElement("div");
            resultElement.textContent = pattern.name;

            resultElement.addEventListener("click", function () {
                resultElement.remove()
                registerSelectedElement(pattern);
            });
            return resultElement;
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
            showHideLabel();
        }

        function deleteSelectedPattern(selectedElement, hiddenResultElement) {
            selectedElement.remove();
            hiddenResultElement.remove();
            showHideLabel();
        }
    });
}


// ========== NUMBER STEPPERS ==========
const numberSteppers = document.querySelectorAll(".number-stepper");

function countStepDecimals(stepValue) {
    if (!stepValue || stepValue === "any") {
        return 0;
    }
    const stepText = String(stepValue);
    if (!stepText.includes(".")) {
        return 0;
    }
    return stepText.split(".")[1].length;
}

function clampValue(value, min, max) {
    let result = value;
    if (min !== null) {
        result = Math.max(result, min);
    }
    if (max !== null) {
        result = Math.min(result, max);
    }
    return result;
}

numberSteppers.forEach(function (stepper) {
    const input = stepper.querySelector('input[type="number"]');
    const decrementButton = stepper.querySelector('[data-stepper-action="decrement"]');
    const incrementButton = stepper.querySelector('[data-stepper-action="increment"]');
    let repeatInterval = null;

    if (!input || !decrementButton || !incrementButton) {
        return;
    }

    function startRepeating(direction) {
        if (repeatInterval !== null) {
            clearInterval(repeatInterval);
        }
        updateInput(direction);
        repeatInterval = setInterval(function () {
            updateInput(direction);
        }, 100);
    }

    function stopRepeating() {
        clearInterval(repeatInterval);
        repeatInterval = null;
    }

    function updateInput(direction) {
        const step = input.step && input.step !== "any" ? Number(input.step) : 1;
        const min = input.min !== "" ? Number(input.min) : null;
        const max = input.max !== "" ? Number(input.max) : null;
        const currentValue = input.value === "" ? 0 : Number(input.value);

        if (Number.isNaN(currentValue)) {
            return;
        }

        const nextValue = clampValue(currentValue + direction * step, min, max);
        const decimals = countStepDecimals(step);
        input.value = String(Number(nextValue.toFixed(decimals)));

        input.dispatchEvent(new Event("input", {bubbles: true}));
        input.dispatchEvent(new Event("change", {bubbles: true}));
    }

    decrementButton.addEventListener("pointerdown", function () {
        startRepeating(-1);
    });

    decrementButton.addEventListener("pointerup", function () {
        stopRepeating();
    });

    decrementButton.addEventListener("pointerleave", function () {
        stopRepeating();
    });

    incrementButton.addEventListener("pointerdown", function () {
        startRepeating(1);
    });

    incrementButton.addEventListener("pointerup", function () {
        stopRepeating();
    });

    incrementButton.addEventListener("pointerleave", function () {
        stopRepeating();
    });
});

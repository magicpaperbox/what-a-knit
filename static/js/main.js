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
// This code only runs on pages that have the form (e.g. /add)

const typeSelect = document.getElementById("type");

if (typeSelect) {
    const subtypeSelect = document.getElementById("subtype");

    // Subcategory options based on selected category
    const subcategories = {
        "sweater": ["raglan", "yoke", "set-in sleeve", "top-down", "bottom-up", "flat", "steek"],
        "cardigan": ["raglan", "yoke", "set-in sleeve", "top-down", "bottom-up", "flat", "steek"],
        "vest": ["raglan", "yoke", "top-down", "bottom-up", "flat", "slipover"],
        "blouse": ["raglan", "yoke", "set-in sleeve", "top-down", "bottom-up", "flat", "long-sleeve", "short-sleeve"],
        "socks": ["heel-flap", "short-row", "afterthought", "toe-up", "cuff-down", "leg-warmers"],
        "pants": ["flat", "in-round", "afterthought", "top-down", "bottom-up", "tights"],
        "skirt": ["mini", "midi", "maxi"],
        "dress": ["mini", "midi", "maxi"],
        "hat": ["beanie", "beret", "balaclava", "bonnet"],
        "scarf": ["shawl", "cowl", "triangular", "crescent", "hood", "collar"],
        "gloves": ["mittens", "classic", "fingerless"],
        "accessories": ["pillow", "blanket", "rug", "towel", "washcloth", "pot-holder", "basket", "keychain", "case", "christmas", "decoratives"],
        "bag": ["shopper", "shoulder-bag", "hand-bag", "backpack"],
        "plushies": ["animals", "food", "others"]
    };

    // Function to update subcategories based on chosen category
    function updateSubcategories() {
        const chosen = typeSelect.value;
        if (!chosen || !subcategories[chosen]) return;

        // Clear existing options
        subtypeSelect.innerHTML = "";

        // Add default 'select' option if needed, or just list subcategories
        // In this logic, we just list subcategories directly

        for (const sub of subcategories[chosen]) {
            const option = document.createElement("option");
            option.value = sub;
            option.textContent = sub;
            subtypeSelect.appendChild(option);
        }

        // If we are editing, check if there is a saved subtype to select
        const savedSubtype = subtypeSelect.getAttribute('data-selected');
        if (savedSubtype) {
            subtypeSelect.value = savedSubtype;
            // Clear the attribute so it doesn't persist if user changes category manually later
            // (optional, but good practice)
            subtypeSelect.removeAttribute('data-selected');
        }
    }

    // Event listener for change
    typeSelect.addEventListener("change", updateSubcategories);

    // Run once on page load (for Edit form)
    if (typeSelect.value) {
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

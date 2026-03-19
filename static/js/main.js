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

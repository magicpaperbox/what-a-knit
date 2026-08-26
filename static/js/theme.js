// ========== THEME TOGGLE ==========

const root = document.documentElement;

function getSavedTheme() {
    try {
        return localStorage.getItem('theme');
    } catch (error) {
        return null;
    }
}

function saveTheme(theme) {
    try {
        localStorage.setItem('theme', theme);
    } catch (error) {
        return;
    }
}

function updateToggleText(isDark) {
    const toggleText = document.querySelector('.toggle-text');
    if (toggleText) {
        toggleText.textContent = isDark ? 'Light mode' : 'Dark mode';
    }
}

function applyTheme(isDark) {
    root.classList.toggle('dark', isDark);
    updateToggleText(isDark);
}

function toggleTheme() {
    const isDark = !root.classList.contains('dark');

    applyTheme(isDark);
    saveTheme(isDark ? 'dark' : 'light');
}

// On page load: restore saved theme
applyTheme(getSavedTheme() === 'dark');

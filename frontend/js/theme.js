/**
 * STTIMS Theme (Light / Dark)
 * Persists the choice in localStorage under 'sttims-theme'.
 *
 * NOTE: this file also runs a small inline snippet in each page's <head>
 * (see the <script> just before dark-mode.css) so the theme is applied
 * BEFORE first paint - otherwise dark-mode users get a white flash.
 */

const THEME_KEY = 'sttims-theme';

function getStoredTheme() {
    try {
        return localStorage.getItem(THEME_KEY);
    } catch (e) {
        return null;
    }
}

function storeTheme(theme) {
    try {
        localStorage.setItem(THEME_KEY, theme);
    } catch (e) {
        // localStorage can be unavailable (private mode, blocked cookies).
        // The theme still applies for this page load, it just won't persist.
        console.warn('Could not save theme preference:', e);
    }
}

function getCurrentTheme() {
    return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
}

function applyTheme(theme) {
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
    updateToggleIcon(theme);
}

function updateToggleIcon(theme) {
    const icon = document.getElementById('themeToggleIcon');
    const btn = document.getElementById('themeToggle');
    if (icon) {
        icon.className = theme === 'dark' ? 'fas fa-sun fa-lg' : 'fas fa-moon fa-lg';
    }
    if (btn) {
        btn.setAttribute('title', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
        btn.setAttribute('aria-label', btn.getAttribute('title'));
    }
}

function toggleTheme() {
    const next = getCurrentTheme() === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    storeTheme(next);
}

document.addEventListener('DOMContentLoaded', function () {
    // The head snippet already set data-theme; just sync the icon
    // and wire up the button.
    updateToggleIcon(getCurrentTheme());

    const btn = document.getElementById('themeToggle');
    if (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            toggleTheme();
        });
    }
});

console.log('🌙 theme.js loaded successfully');

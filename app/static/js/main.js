// Wait for the document to be fully loaded before running the script.
document.addEventListener('DOMContentLoaded', () => {

    // --- Theme (Dark/Light Mode) Toggler ---
    const themeToggleBtn = document.getElementById('theme-toggle');
    const getPreferredTheme = () => {
        // Check for a saved theme in localStorage, or use the system preference
        return localStorage.getItem('theme') || 'light';
    };

    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        // Update the icon based on the theme
        themeToggleBtn.innerHTML = theme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    };

    // Set the initial theme on page load
    setTheme(getPreferredTheme());

    // Event listener for the theme toggle button
    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });

    // --- Back to Top Button Logic ---
    const backToTopButton = document.getElementById('back-to-top-btn');

    // Show or hide the button based on scroll position
    window.onscroll = () => {
        if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
            backToTopButton.style.display = "block";
        } else {
            backToTopButton.style.display = "none";
        }
    };

    // Scroll to the top when the button is clicked
    backToTopButton.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

});
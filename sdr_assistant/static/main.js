document.addEventListener('DOMContentLoaded', function() {
    // Check for auth token
    const token = localStorage.getItem('auth_token');
    const username = localStorage.getItem('username');
    
    if (token && username) {
        const usernameElement = document.getElementById('username');
        if (usernameElement) {
            usernameElement.textContent = username;
        }
    } else {
        // Redirect to login if not on login page and no token
        if (!window.location.pathname.includes('login.html') && !window.location.pathname.endsWith('/')) {
            window.location.href = '/login.html';
        }
    }
    
    // Logout functionality
    const logoutButton = document.getElementById('logout-btn');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('auth_token');
            localStorage.removeItem('username');
            window.location.href = '/login.html';
        });
    }
});

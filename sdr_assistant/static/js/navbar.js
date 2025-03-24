// Navbar functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get current page filename
    const currentPage = window.location.pathname.split('/').pop() || 'home.html';
    
    // Set appropriate navigation link as active
    let activeNavId = 'nav-home'; // Default
    
    if (currentPage === 'home.html' || currentPage === '') {
        activeNavId = 'nav-home';
    } else if (currentPage === 'index.html') {
        activeNavId = 'nav-research';
    } else if (currentPage === 'accounts.html') {
        activeNavId = 'nav-accounts';
    } else if (currentPage === 'library.html') {
        activeNavId = 'nav-library';
    } else if (currentPage === 'dashboard.html') {
        activeNavId = 'nav-dashboard';
    } else if (currentPage.includes('account-detail')) {
        activeNavId = 'nav-accounts';
    }
    
    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class to the current page nav link
    const activeNavLink = document.getElementById(activeNavId);
    if (activeNavLink) {
        activeNavLink.classList.add('active');
    }
    
    // Handle user info display
    if (localStorage.getItem('loggedIn') === 'true') {
        document.getElementById('loginButton').classList.add('d-none');
        document.getElementById('userInfo').classList.remove('d-none');
    }
});

// Simulated login function
function login() {
    localStorage.setItem('loggedIn', 'true');
    document.getElementById('loginButton').classList.add('d-none');
    document.getElementById('userInfo').classList.remove('d-none');
}

// Simulated logout function
function logout() {
    localStorage.removeItem('loggedIn');
    document.getElementById('loginButton').classList.remove('d-none');
    document.getElementById('userInfo').classList.add('d-none');
    
    // Redirect to home page
    window.location.href = 'home.html';
}

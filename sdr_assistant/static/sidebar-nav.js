/**
 * Sidebar Navigation JavaScript
 * Handles sidebar functionality including mobile toggle and active state
 */

document.addEventListener('DOMContentLoaded', function() {
    // Set active nav item based on current page
    setActiveNavItem();
    
    // Mobile sidebar toggle functionality
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(event) {
        if (window.innerWidth < 768) {
            const isClickInsideSidebar = sidebar && sidebar.contains(event.target);
            const isClickOnToggle = sidebarToggle && sidebarToggle.contains(event.target);
            
            if (!isClickInsideSidebar && !isClickOnToggle && sidebar && sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
            }
        }
    });
    
    // Create new task functionality
    window.createNewTask = function() {
        // This function will be called when the "Create new task" button is clicked
        console.log('Create new task clicked');
        // Add your task creation logic here
        alert('Creating a new task...');
    };
});

/**
 * Sets the active navigation item based on the current page URL
 */
function setActiveNavItem() {
    const currentPage = window.location.pathname.split('/').pop();
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href === currentPage || 
            (currentPage === '' && href === 'home.html') || 
            (currentPage === 'index.html' && href === 'index.html')) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

/**
 * Logout function
 */
function logout() {
    console.log('User logged out');
    // Add your logout logic here
    alert('Logging out...');
    // Redirect to login page or home page
    // window.location.href = 'home.html';
}

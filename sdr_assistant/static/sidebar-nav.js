// Sidebar Navigation JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Set active nav item based on current page
    setActiveNavItem();
    
    // Mobile toggle functionality
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
    }
    
    // Close sidebar when clicking outside (mobile only)
    document.addEventListener('click', function(event) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggle = sidebarToggle && sidebarToggle.contains(event.target);
        
        if (!isClickInsideSidebar && !isClickOnToggle && window.innerWidth <= 768 && sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
        }
    });
});

// Function to set the active navigation item based on current URL
function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        
        // Remove active class from all items
        item.classList.remove('active');
        
        // Check if the href matches the current path
        if (href && (currentPath.endsWith(href) || 
            (href === 'index.html' && (currentPath.endsWith('/') || currentPath.endsWith('/sdr_assistant/'))))) {
            item.classList.add('active');
        }
    });
}

// Function to create a new task (placeholder)
function createNewTask() {
    console.log('Creating new task...');
    // Implement task creation functionality here
    alert('New task creation feature coming soon!');
}

/**
 * Component Inclusion Script
 * 
 * This script helps include standardized components like headers and footers
 * across all pages to ensure consistent navigation and branding.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Include standard header in all pages
    includeComponent('header', 'components/header.html');
});

/**
 * Loads a component into a specified element
 * @param {string} targetId - ID of element to load component into
 * @param {string} componentPath - Path to the component HTML file
 */
function includeComponent(targetId, componentPath) {
    const element = document.getElementById(targetId);
    if (!element) return;
    
    fetch(componentPath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            element.innerHTML = html;
        })
        .catch(error => {
            console.error(`Error loading component ${componentPath}:`, error);
        });
}

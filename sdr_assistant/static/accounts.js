/**
 * SDR Research Assistant - Accounts Page
 * 
 * This file contains the client-side logic for the Accounts page of the SDR Research Assistant.
 * It handles loading accounts from Airtable and displaying them in a gallery view.
 */

// DOM Elements
const accountsGrid = document.getElementById('accountsGrid');
const accountSearch = document.getElementById('accountSearch');
const industryFilter = document.getElementById('industryFilter');
const userName = document.getElementById('userName');

// Variables
let allAccounts = [];

// Set user name
if (userName) {
    userName.textContent = 'Albert Perez';
}

/**
 * Initializes the page when loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    loadAccounts();
    setupEventListeners();
    setupAccountCardEvents();
});

/**
 * Loads account data from the backend API
 * Populates the account gallery with the results
 */
async function loadAccounts() {
    try {
        const response = await fetch('/api/accounts/details');
        const accounts = await response.json();
        
        allAccounts = accounts;
        renderAccounts(accounts);
    } catch (error) {
        console.error('Error loading accounts:', error);
        showError('Failed to load accounts. Please try again later.');
    }
}

/**
 * Sets up event listeners for search and filter inputs
 */
function setupEventListeners() {
    // Search functionality
    accountSearch.addEventListener('input', filterAccounts);
    
    // Industry filter
    industryFilter.addEventListener('change', filterAccounts);
}

/**
 * Filters accounts based on search input and industry filter
 */
function filterAccounts() {
    const searchTerm = accountSearch.value.toLowerCase();
    const industry = industryFilter.value;
    
    const filteredAccounts = allAccounts.filter(account => {
        const matchesSearch = !searchTerm || 
            account.name.toLowerCase().includes(searchTerm) || 
            (account.industry && account.industry.toLowerCase().includes(searchTerm));
        
        const matchesIndustry = !industry || account.industry === industry;
        
        return matchesSearch && matchesIndustry;
    });
    
    renderAccounts(filteredAccounts);
}

/**
 * Renders the account cards in the grid
 * 
 * @param {Array} accounts - Array of account objects to render
 */
function renderAccounts(accounts) {
    accountsGrid.innerHTML = '';
    
    if (accounts.length === 0) {
        accountsGrid.innerHTML = '<div class="no-results">No accounts found matching your criteria</div>';
        return;
    }
    
    accounts.forEach(account => {
        const card = document.createElement('div');
        card.className = 'account-card';
        card.setAttribute('data-account', account.name);
        
        const logoPlaceholder = getInitials(account.name);
        const industry = account.industry || 'Unknown Industry';
        const employees = account.employees || 'Unknown';
        const location = account.location || 'Unknown Location';
        const colorHex = getRandomColor(account.name);
        
        card.innerHTML = `
            <div class="account-logo" style="background-color: ${colorHex}">
                ${logoPlaceholder}
            </div>
            <h3 class="account-name">${account.name}</h3>
            <div class="account-industry">${industry}</div>
            <div class="account-details">
                <div class="account-detail">
                    <span class="detail-label">Employees:</span>
                    <span class="detail-value">${employees}</span>
                </div>
                <div class="account-detail">
                    <span class="detail-label">HQ:</span>
                    <span class="detail-value">${location}</span>
                </div>
            </div>
            <a href="/?account=${encodeURIComponent(account.name)}" class="view-account-btn">
                <span>View</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
            </a>
        `;
        
        accountsGrid.appendChild(card);
    });
}

/**
 * Shows an error message in the accounts grid
 * 
 * @param {string} message - The error message to display
 */
function showError(message) {
    accountsGrid.innerHTML = `<div class="error-message">${message}</div>`;
}

/**
 * Gets the initials from a name for the logo placeholder
 * 
 * @param {string} name - The name to extract initials from
 * @returns {string} - The initials (max 2 characters)
 */
function getInitials(name) {
    return name
        .split(' ')
        .map(word => word[0])
        .join('')
        .substring(0, 2)
        .toUpperCase();
}

/**
 * Generates a consistent color based on the account name
 * 
 * @param {string} name - The account name
 * @returns {string} - A hex color code
 */
function getRandomColor(name) {
    // Generate a simple hash from the name
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    // Convert to hex color
    let color = '#';
    for (let i = 0; i < 3; i++) {
        const value = (hash >> (i * 8)) & 0xFF;
        color += ('00' + value.toString(16)).substr(-2);
    }
    
    return color;
}

/**
 * Add click event to each account card to navigate to research page
 */
function setupAccountCardEvents() {
    const accountCards = document.querySelectorAll('.account-card');
    accountCards.forEach(card => {
        card.addEventListener('click', () => {
            const accountName = card.getAttribute('data-account');
            window.location.href = `/?account=${accountName}`;
        });
    });
}

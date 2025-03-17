/**
 * SDR Assistant - Account Detail Page
 * 
 * This file contains the client-side logic for the account detail page.
 * It handles loading account data, displaying information, and user interactions
 * for a specific account.
 */

// DOM Elements - will be initialized when document is fully loaded
let accountName;
let accountIndustry;
let accountSize;
let accountLocation;
let heatScore;
let tacticalStrategy;

// Configurable settings
const DEMO_MODE = true; // Set to false to use real API calls
const API_BASE_URL = '/api';

/**
 * Initialize the DOM elements when document is loaded
 */
function initDOMElements() {
    // Account header elements
    accountName = document.getElementById('accountName');
    accountIndustry = document.getElementById('accountIndustry');
    accountSize = document.getElementById('accountSize');
    accountLocation = document.getElementById('accountLocation');
    heatScore = document.getElementById('heatScore');
    
    // Main sections
    tacticalStrategy = document.getElementById('tacticalStrategy');
    
    console.log("DOM elements initialized for account detail page");
}

/**
 * Check if user is logged in
 */
function checkUserLogin() {
    const userInfo = document.getElementById('userInfo');
    const loginButton = document.getElementById('loginButton');
    const userName = document.getElementById('userName');
    
    if (DEMO_MODE) {
        // In demo mode, just show the user as logged in
        userInfo.classList.remove('d-none');
        loginButton.classList.add('d-none');
        userName.textContent = 'Albert Perez';
        return;
    }
    
    const token = localStorage.getItem('auth_token');
    if (token) {
        // User is logged in
        fetch(`${API_BASE_URL}/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.name) {
                userInfo.classList.remove('d-none');
                loginButton.classList.add('d-none');
                userName.textContent = data.name;
            }
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
            // Default fallback for demo
            userInfo.classList.remove('d-none');
            loginButton.classList.add('d-none');
            userName.textContent = 'Albert Perez';
        });
    } else {
        // No token found, user needs to log in
        userInfo.classList.add('d-none');
        loginButton.classList.remove('d-none');
    }
}

/**
 * Load account data from API or use mock data in demo mode
 */
function loadAccountData() {
    // Get account ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const accountId = urlParams.get('id');
    
    if (!accountId) {
        showNotification('No account ID specified', 'error');
        return;
    }
    
    if (DEMO_MODE) {
        // Use mock data in demo mode
        const mockAccount = getMockAccountData(accountId);
        updateAccountUI(mockAccount);
        return;
    }
    
    // Fetch from API
    fetch(`${API_BASE_URL}/accounts/${accountId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load account data');
            }
            return response.json();
        })
        .then(data => {
            updateAccountUI(data);
        })
        .catch(error => {
            console.error('Error loading account data:', error);
            showNotification('Failed to load account data', 'error');
            
            // Fallback to mock data
            const mockAccount = getMockAccountData(accountId);
            updateAccountUI(mockAccount);
        });
}

/**
 * Update the UI with account data
 */
function updateAccountUI(account) {
    // Update account header
    accountName.textContent = account.name;
    accountIndustry.textContent = account.industry;
    accountSize.textContent = account.size;
    accountLocation.textContent = account.location;
    
    // Update heat score
    heatScore.textContent = account.heatScore;
    
    // Set heat score color based on value
    heatScore.classList.remove('heat-score-high', 'heat-score-medium', 'heat-score-low');
    if (account.heatScore >= 80) {
        heatScore.classList.add('heat-score-high');
    } else if (account.heatScore >= 50) {
        heatScore.classList.add('heat-score-medium');
    } else {
        heatScore.classList.add('heat-score-low');
    }
    
    // Update tactical strategy content
    if (account.tacticalStrategy) {
        tacticalStrategy.innerHTML = account.tacticalStrategy;
    }
    
    // Update research tabs (would implement for real API)
    
    // Update sentiment analysis (would implement for real API)
    
    console.log(`Account data loaded for ${account.name}`);
}

/**
 * Get mock account data for demo mode
 */
function getMockAccountData(accountId) {
    // Mock data for demo purposes
    const mockAccounts = {
        '1': {
            id: '1',
            name: 'Acme Corporation',
            industry: 'Technology',
            size: '1000-5000 employees',
            location: 'San Francisco, CA',
            heatScore: 85,
            tacticalStrategy: `
                <p><strong>Champions-Based Approach:</strong> With the recent layoffs at the company, focus on identifying and engaging new decision-makers who have taken over responsibilities.</p>
                <p><strong>Value Proposition:</strong> Emphasize how our solution can help the company do more with fewer resources, highlighting ROI and time-saving benefits.</p>
                <p><strong>Key Actions:</strong></p>
                <ul>
                    <li>Connect with Jane Smith (VP of Engineering) who is now overseeing developer productivity initiatives</li>
                    <li>Reference their recent blog post about improving developer efficiency</li>
                    <li>Mention specific metrics from similar clients who improved productivity by 32% after implementation</li>
                </ul>
            `
        },
        '2': {
            id: '2',
            name: 'TechX Solutions',
            industry: 'Information Technology',
            size: '501-1000 employees',
            location: 'Austin, TX',
            heatScore: 72,
            tacticalStrategy: `
                <p><strong>Land and Expand Strategy:</strong> Focus on securing a small initial implementation with their R&D team.</p>
                <p><strong>Value Proposition:</strong> Position our solution as enhancing their existing tech stack, not replacing it. Emphasize seamless integration capabilities.</p>
                <p><strong>Key Actions:</strong></p>
                <ul>
                    <li>Schedule a technical demo with their lead architect</li>
                    <li>Provide case studies of similar-sized companies in their industry</li>
                    <li>Create a custom ROI calculator based on their specific workflow inefficiencies</li>
                </ul>
            `
        },
        '3': {
            id: '3',
            name: 'MediHealth Systems',
            industry: 'Healthcare',
            size: '5000+ employees',
            location: 'Boston, MA',
            heatScore: 93,
            tacticalStrategy: `
                <p><strong>Compliance-First Approach:</strong> Their industry requires strict adherence to regulatory standards.</p>
                <p><strong>Value Proposition:</strong> Emphasize how our solution maintains HIPAA compliance while improving developer productivity.</p>
                <p><strong>Key Actions:</strong></p>
                <ul>
                    <li>Share our security and compliance documentation upfront</li>
                    <li>Connect with their compliance officer to address specific concerns</li>
                    <li>Offer a phased implementation approach to minimize disruption</li>
                </ul>
            `
        }
    };
    
    // Return requested account or first account as fallback
    return mockAccounts[accountId] || mockAccounts['1'];
}

/**
 * Show a notification message to the user
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification-toast`;
    notification.role = 'alert';
    notification.innerHTML = message;
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Show notification with animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

/**
 * Initialize when the DOM is fully loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize DOM elements
    initDOMElements();
    
    // Check user login status
    checkUserLogin();
    
    // Load account data
    loadAccountData();
    
    // Initialize event listeners for actions
    initEventListeners();
    
    console.log('Account detail page initialized');
});

/**
 * Initialize event listeners for interactive elements
 */
function initEventListeners() {
    // Add event listeners for tab switches, buttons, etc.
    const refreshButton = document.querySelector('.btn-outline-primary');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            loadAccountData();
            showNotification('Account data refreshed', 'success');
        });
    }
    
    // Other event listeners would be added here
}

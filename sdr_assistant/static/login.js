/**
 * SDR Research Assistant - Login Page
 * 
 * This file contains the client-side logic for the login page.
 * It handles user authentication, form validation, and redirects.
 */

// DOM Elements
const loginForm = document.querySelector('.login-form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const rememberMeCheckbox = document.getElementById('rememberMe');
const loginButton = document.getElementById('loginButton');

/**
 * Initializes the page when loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    // Check for existing session
    checkExistingSession();
    
    // Set up event listeners
    loginButton.addEventListener('click', handleLogin);
    
    // Enable form submission with Enter key
    passwordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleLogin();
        }
    });
});

/**
 * Checks if user already has an active session
 * Redirects to main page if a valid session exists
 */
function checkExistingSession() {
    const token = localStorage.getItem('auth_token');
    
    if (token) {
        // Valid token exists
        redirectToMainPage();
    }
}

/**
 * Handles the login button click
 * Validates form inputs and attempts to authenticate user
 */
async function handleLogin() {
    // Reset any previous error states
    resetErrors();
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    // Show loading state
    setLoading(true);
    
    try {
        // Attempt to authenticate
        const response = await authenticateUser(emailInput.value, passwordInput.value);
        
        if (response.success) {
            // Save token
            localStorage.setItem('auth_token', response.token);
            if (response.user && response.user.name) {
                localStorage.setItem('user_name', response.user.name);
            }
            
            // Redirect to main page
            redirectToMainPage();
        } else {
            showError(response.message || 'Invalid email or password');
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('An error occurred during login. Please try again.');
    } finally {
        setLoading(false);
    }
}

/**
 * Authenticates user with the backend API
 * 
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<Object>} - Authentication response
 */
async function authenticateUser(email, password) {
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });
        
        return await response.json();
    } catch (error) {
        console.error('Authentication error:', error);
        throw error;
    }
}

/**
 * Validates the login form
 * 
 * @returns {boolean} - Whether the form is valid
 */
function validateForm() {
    let isValid = true;
    
    // Validate email
    if (!emailInput.value || !isValidEmail(emailInput.value)) {
        showInputError(emailInput, 'Please enter a valid email address');
        isValid = false;
    }
    
    // Validate password
    if (!passwordInput.value) {
        showInputError(passwordInput, 'Please enter your password');
        isValid = false;
    }
    
    return isValid;
}

/**
 * Checks if an email is valid
 * 
 * @param {string} email - Email to validate
 * @returns {boolean} - Whether the email is valid
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Shows an error for a specific input
 * 
 * @param {HTMLElement} inputElement - The input element with an error
 * @param {string} message - Error message to display
 */
function showInputError(inputElement, message) {
    inputElement.classList.add('input-error');
    
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    
    inputElement.parentNode.appendChild(errorElement);
}

/**
 * Shows a general login error
 * 
 * @param {string} message - Error message to display
 */
function showError(message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'login-error';
    errorElement.textContent = message;
    
    // Insert at top of form
    loginForm.insertBefore(errorElement, loginForm.firstChild);
}

/**
 * Resets all error states
 */
function resetErrors() {
    // Remove error classes
    document.querySelectorAll('.input-error').forEach(el => {
        el.classList.remove('input-error');
    });
    
    // Remove error messages
    document.querySelectorAll('.error-message, .login-error').forEach(el => {
        el.remove();
    });
}

/**
 * Sets the loading state of the login button
 * 
 * @param {boolean} isLoading - Whether the form is in loading state
 */
function setLoading(isLoading) {
    if (isLoading) {
        loginButton.textContent = 'Signing in...';
        loginButton.disabled = true;
    } else {
        loginButton.textContent = 'Sign In';
        loginButton.disabled = false;
    }
}

/**
 * Redirects to the main application page
 */
function redirectToMainPage() {
    window.location.href = '/';
}

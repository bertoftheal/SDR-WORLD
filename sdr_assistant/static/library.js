/**
 * SDR Research Assistant - Knowledge Library
 * 
 * This file contains the client-side logic for the Knowledge Library page.
 * It handles loading, filtering, and displaying saved insights and research.
 */

// DOM Elements
const libraryEntries = document.getElementById('libraryEntries');
const librarySearch = document.getElementById('librarySearch');
const categoryLinks = document.querySelectorAll('.library-categories li');
const tagsList = document.getElementById('tagsList');
const username = document.getElementById('username');

// Check for auth token
const token = localStorage.getItem('auth_token');
const storedUsername = localStorage.getItem('username');

// Set user name if logged in
if (username && storedUsername) {
    username.textContent = storedUsername;
}

// Variables
let allEntries = [];
let allTags = new Set();

/**
 * Initializes the page when loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    loadLibraryEntries();
    setupEventListeners();
});

/**
 * Loads knowledge library entries from the backend API
 */
function loadLibraryEntries() {
    // Show loading state
    libraryEntries.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading library entries...</p>
        </div>
    `;
    
    // Fetch library entries from the API
    fetch('/api/library', {
        headers: {
            'Authorization': token ? `Bearer ${token}` : ''
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to load library entries');
        }
        return response.json();
    })
    .then(data => {
        allEntries = data;
        generateTagsList(data);
        renderEntries(data);
    })
    .catch(error => {
        console.error('Error loading library entries:', error);
        showError('Failed to load library entries. Please try again later.');
    });
}

/**
 * Sets up event listeners for search, filters, and category links
 */
function setupEventListeners() {
    // Search input event listener
    if (librarySearch) {
        librarySearch.addEventListener('input', () => {
            filterEntries();
        });
    }
    
    // Category filter links
    categoryLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Remove active class from all links
            categoryLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            link.classList.add('active');
            
            // Filter entries
            filterEntries();
        });
    });
}

/**
 * Filters library entries based on search input and category selection
 */
function filterEntries() {
    const searchTerm = librarySearch ? librarySearch.value.toLowerCase() : '';
    const activeCategory = document.querySelector('.library-categories li.active');
    const category = activeCategory ? activeCategory.getAttribute('data-category') : 'all';
    
    let filteredEntries = allEntries;
    
    // Filter by search term
    if (searchTerm) {
        filteredEntries = filteredEntries.filter(entry => {
            return entry.account.toLowerCase().includes(searchTerm) ||
                   (entry.industry_insights && entry.industry_insights.toLowerCase().includes(searchTerm)) ||
                   (entry.company_insights && entry.company_insights.toLowerCase().includes(searchTerm)) ||
                   (entry.forward_thinking && entry.forward_thinking.toLowerCase().includes(searchTerm)) ||
                   (entry.talk_track && entry.talk_track.toLowerCase().includes(searchTerm)) ||
                   (entry.tags && entry.tags.some(tag => tag.toLowerCase().includes(searchTerm)));
        });
    }
    
    // Filter by category
    if (category && category !== 'all') {
        filteredEntries = filteredEntries.filter(entry => {
            // Map category values to entry properties
            const categoryMap = {
                'industry_insights': 'industry_insights',
                'company_insights': 'company_insights',
                'forward_thinking': 'forward_thinking',
                'talk_track': 'talk_track'
            };
            
            const propertyName = categoryMap[category];
            return propertyName && entry[propertyName] && entry[propertyName].trim() !== '';
        });
    }
    
    // Render filtered entries
    renderEntries(filteredEntries);
}

/**
 * Generates a list of tags from all entry tags
 * 
 * @param {Array} entries - Array of library entries
 */
function generateTagsList(entries) {
    // Clear the tags set
    allTags.clear();
    
    // Collect all unique tags
    entries.forEach(entry => {
        if (entry.tags && Array.isArray(entry.tags)) {
            entry.tags.forEach(tag => {
                allTags.add(tag);
            });
        }
    });
    
    // Sort tags alphabetically
    const sortedTags = Array.from(allTags).sort();
    
    // Render tags
    if (tagsList) {
        tagsList.innerHTML = '';
        
        if (sortedTags.length === 0) {
            tagsList.innerHTML = '<div class="empty-tags">No tags available</div>';
            return;
        }
        
        sortedTags.forEach(tag => {
            const tagElement = document.createElement('span');
            tagElement.className = 'library-tag';
            tagElement.textContent = tag;
            
            // Add click event to filter by tag
            tagElement.addEventListener('click', () => {
                librarySearch.value = tag;
                filterEntries();
            });
            
            tagsList.appendChild(tagElement);
        });
    }
}

/**
 * Renders the library entries in the content area
 * 
 * @param {Array} entries - Array of entry objects to render
 */
function renderEntries(entries) {
    if (!libraryEntries) return;
    
    // Clear the entries container
    libraryEntries.innerHTML = '';
    
    // Handle empty results
    if (entries.length === 0) {
        libraryEntries.innerHTML = `
            <div class="empty-library">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <h3>No library entries found</h3>
                <p>Try changing your search or filter criteria</p>
            </div>
        `;
        return;
    }
    
    // Sort entries by date (newest first)
    entries.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    // Add each entry to the container
    entries.forEach(entry => {
        const entryCard = document.createElement('div');
        entryCard.className = 'library-entry';
        
        // Format date
        const entryDate = new Date(entry.date);
        const formattedDate = entryDate.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        entryCard.innerHTML = `
            <div class="library-entry-header">
                <h3 class="library-entry-title">${entry.account}</h3>
                <div class="library-entry-date">${formattedDate}</div>
            </div>
            <div class="library-entry-content">
                ${entry.industry_insights ? `
                <div class="library-entry-section">
                    <h4>Industry Insights</h4>
                    <div class="entry-text">${formatContent(entry.industry_insights)}</div>
                </div>` : ''}
                
                ${entry.company_insights ? `
                <div class="library-entry-section">
                    <h4>Company Insights</h4>
                    <div class="entry-text">${formatContent(entry.company_insights)}</div>
                </div>` : ''}
                
                ${entry.forward_thinking ? `
                <div class="library-entry-section">
                    <h4>Forward Thinking</h4>
                    <div class="entry-text">${formatContent(entry.forward_thinking)}</div>
                </div>` : ''}
                
                ${entry.talk_track ? `
                <div class="library-entry-section">
                    <h4>Talk Track</h4>
                    <div class="entry-text">${formatContent(entry.talk_track)}</div>
                </div>` : ''}
            </div>
            <div class="library-entry-footer">
                ${renderTags(entry.tags)}
                <div class="library-entry-actions">
                    <button class="icon-button" title="View Research" onclick="location.href='/?account=${encodeURIComponent(entry.account)}'">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                    </button>
                </div>
            </div>
        `;
        
        libraryEntries.appendChild(entryCard);
    });
}

/**
 * Formats content text with proper HTML
 * 
 * @param {string} content - The text content to format
 * @returns {string} - Formatted HTML
 */
function formatContent(content) {
    if (!content || content.trim() === '') {
        return '<p>No information available.</p>';
    }
    
    // Convert newlines to paragraphs
    return content.split('\n\n').map(paragraph => {
        if (paragraph.trim() === '') return '';
        
        // Check if it's a list item
        if (paragraph.match(/^\d+\.\s/)) {
            return `<div class="content-item">${paragraph}</div>`;
        } else {
            return `<p>${paragraph}</p>`;
        }
    }).join('');
}

/**
 * Renders the tags for an entry
 * 
 * @param {Array} tags - Array of tag strings
 * @returns {string} - HTML string for the tags
 */
function renderTags(tags) {
    if (!tags || !Array.isArray(tags) || tags.length === 0) {
        return '<div class="library-entry-tags"></div>';
    }
    
    const tagElements = tags.map(tag => {
        return `<span class="entry-tag">${tag}</span>`;
    }).join('');
    
    return `<div class="library-entry-tags">${tagElements}</div>`;
}

/**
 * Shows an error message in the library entries area
 * 
 * @param {string} message - The error message to display
 */
function showError(message) {
    if (libraryEntries) {
        libraryEntries.innerHTML = `
            <div class="error-message">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3>Error</h3>
                <p>${message}</p>
            </div>
        `;
    }
}

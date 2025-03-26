/**
 * Company Metadata Functions
 * 
 * This file contains functions for fetching and updating company metadata
 * from the Perplexity API via our backend service.
 */

let metadataCache = {};

/**
 * Fetch company metadata and update UI elements
 * @param {string} companyName - The name of the company to fetch metadata for
 * @returns {Promise} - A promise that resolves when metadata is updated
 */
function fetchCompanyMetadata(companyName) {
    // Check cache first
    if (metadataCache[companyName]) {
        console.log('Using cached metadata for:', companyName);
        updateCompanyMetadataUI(metadataCache[companyName]);
        return Promise.resolve(metadataCache[companyName]);
    }

    // Show loading state for metadata elements
    const metadataElements = document.querySelectorAll('.meta-value');
    metadataElements.forEach(el => {
        el.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i>';
        el.classList.add('updating');
    });
    
    // Update company name in the header
    const companyNameHeader = document.querySelector('.company-name');
    if (companyNameHeader) {
        companyNameHeader.textContent = companyName;
        companyNameHeader.classList.add('animate-update');
        setTimeout(() => companyNameHeader.classList.remove('animate-update'), 500);
    }
    
    console.log('Fetching metadata for:', companyName);
    
    // Get authentication token - this may be different in your app
    const token = localStorage.getItem('token') || sessionStorage.getItem('token') || '';
    
    // Make API request to get metadata
    return fetch('/api/company-metadata', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({ companyName: companyName })
    })
    .then(response => {
        if (!response.ok) {
            console.error(`HTTP error! Status: ${response.status}, Text: ${response.statusText}`);
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Company metadata received:', data);
        
        // Update the UI with the metadata
        if (data.success && data.metadata) {
            // Cache the metadata
            metadataCache[companyName] = data.metadata;
            // Update UI
            updateCompanyMetadataUI(data.metadata);
            return data.metadata;
        } else {
            console.error('Metadata API returned success=false:', data.message || 'Unknown error');
            throw new Error(data.message || 'Failed to fetch metadata');
        }
        return null;
    })
    .catch(error => {
        console.error('Error fetching company metadata:', error);
        showNotification('Error fetching company details', 'error');
        
        // Reset the updating state
        metadataElements.forEach(el => {
            el.classList.remove('updating');
        });
        
        return null;
    });
}

/**
 * Update UI elements with company metadata
 * @param {Object} metadata - Company metadata object
 */
function updateCompanyMetadataUI(metadata) {
    console.log('Updating company metadata UI with:', metadata);
    
    // Debug which elements are available on the page
    console.log('Company description elements on page:', {
        byId: document.getElementById('companyOverview'),
        byClass: document.querySelector('.company-description'),
        byTag: document.querySelector('p.mb-0')
    });
    
    // Find all metadata value elements by their index or labels
    const metaValues = document.querySelectorAll('.meta-value');
    
    // Map metadata fields to likely indices
    if (metaValues.length >= 4) {
        // Headquarters is usually the first item
        if (metadata.headquarters && metaValues[0]) {
            metaValues[0].textContent = metadata.headquarters;
            metaValues[0].classList.add('animate-update');
            setTimeout(() => metaValues[0].classList.remove('animate-update'), 500);
        }
        
        // Employees count is usually the second item
        if (metadata.employees && metaValues[1]) {
            metaValues[1].textContent = metadata.employees;
            metaValues[1].classList.add('animate-update');
            setTimeout(() => metaValues[1].classList.remove('animate-update'), 500);
        }
        
        // Market cap is usually the third item
        if (metadata.market_cap && metaValues[2]) {
            metaValues[2].textContent = metadata.market_cap;
            metaValues[2].classList.add('animate-update');
            setTimeout(() => metaValues[2].classList.remove('animate-update'), 500);
        }
        
        // Founded year is usually the fourth item
        if (metadata.founded && metaValues[3]) {
            metaValues[3].textContent = metadata.founded;
            metaValues[3].classList.add('animate-update');
            setTimeout(() => metaValues[3].classList.remove('animate-update'), 500);
        }
    }
    
    // Remove the updating class from all elements
    metaValues.forEach(el => {
        el.classList.remove('updating');
    });
    
    // Update company description/overview if available
    if (metadata.description && metadata.description !== 'Unknown') {
        // Try multiple selectors to find the company description paragraph
        const companyOverview = document.getElementById('companyOverview') || 
                              document.querySelector('.company-description') || 
                              document.querySelector('p.mb-0');
        
        if (companyOverview) {
            console.log('Updating company overview with:', metadata.description);
            companyOverview.innerHTML = metadata.description;
            companyOverview.classList.add('animate-update');
            setTimeout(() => companyOverview.classList.remove('animate-update'), 500);
            
            // Also update any other paragraphs that might be company descriptions
            const companyDescriptions = document.querySelectorAll('.company-description p, .card-body p');
            companyDescriptions.forEach(el => {
                if (el !== companyOverview) {
                    el.innerHTML = metadata.description;
                    el.classList.add('animate-update');
                    setTimeout(() => el.classList.remove('animate-update'), 500);
                }
            });
        } else {
            console.error('Could not find company description element to update');
        }
    } else {
        console.warn('No valid description in metadata:', metadata.description);
    }
}

// Export functions for use in other scripts
window.fetchCompanyMetadata = fetchCompanyMetadata;
window.updateCompanyMetadataUI = updateCompanyMetadataUI;

// Update company name header when input field changes
document.addEventListener('DOMContentLoaded', () => {
    const accountInput = document.getElementById('accountSelect');
    const companyNameHeader = document.querySelector('.company-name');
    
    if (accountInput && companyNameHeader) {
        // Update company name header on input
        accountInput.addEventListener('input', () => {
            const companyName = accountInput.value.trim();
            if (companyName) {
                companyNameHeader.textContent = companyName;
                // Optional: Add a subtle animation
                companyNameHeader.classList.add('animate-update');
                setTimeout(() => companyNameHeader.classList.remove('animate-update'), 500);
            }
        });
        
        // Also update when generateBtn is clicked for complete metadata fetch
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                const companyName = accountInput.value.trim();
                if (companyName) {
                    fetchCompanyMetadata(companyName);
                }
            });
        }
    }
});

// Add event listener to ensure DOM is loaded before attempting to find elements
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded - company-metadata.js initialized');
    // Initialize any necessary elements or attach event listeners here
});

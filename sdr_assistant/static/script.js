/**
 * SDR Research Assistant - Frontend JavaScript
 * 
 * This file contains the client-side logic for the SDR Research Assistant application.
 * It handles UI interactions, API calls, and updates the DOM with the research results.
 * 
 * Main Functions:
 * - Loading accounts from the backend
 * - Generating research for selected accounts
 * - Saving research to Airtable
 * - Updating the UI based on application state
 */

// DOM Elements
const accountSelect = document.getElementById('accountSelect');
const generateBtn = document.getElementById('generateBtn');
const saveBtn = document.getElementById('saveToAirtable');
const industryInsights = document.getElementById('industryInsights');
const companyInsights = document.getElementById('companyInsights');
const visionInsights = document.getElementById('visionInsights');
const recommendedTalkTrack = document.getElementById('recommendedTalkTrack');
const userName = document.getElementById('userName');
const username = document.getElementById('username');

// Check if user is logged in
function checkUserLogin() {
    const token = localStorage.getItem('auth_token');
    if (token) {
        // User is logged in
        fetch('/api/user', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.name) {
                userName.textContent = data.name;
                username.textContent = data.name;
            }
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
        });
    } else {
        // No token found, user needs to log in
        userName.textContent = 'Albert Perez'; // Default for demo
        username.textContent = 'Sign In';
    }
}

/**
 * Loads account data from the backend API
 * Populates the account selection dropdown with the results
 * If API call fails, logs error to console
 */
async function loadAccounts() {
    try {
        const response = await fetch('/api/accounts');
        const accounts = await response.json();
        
        // Clear existing options except the placeholder
        accountSelect.innerHTML = '<option value="">Select an account...</option>';
        
        // Add new options
        accounts.forEach(account => {
            const option = document.createElement('option');
            option.value = account.name;
            option.textContent = account.name;
            accountSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading accounts:', error);
    }
}

/**
 * Generates research for the selected account
 * Makes API call to backend to generate insights using Perplexity and OpenAI
 * Updates UI with the generated insights
 * Handles loading states and errors
 */
async function generateResearch() {
    const accountName = accountSelect.value;
    if (!accountName) {
        alert('Please select an account');
        return;
    }
    
    // Update UI to loading state
    setLoadingState(true);
    
    try {
        const response = await fetch('/api/research', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ accountName })
        });
        
        const data = await response.json();
        
        // Update insights
        industryInsights.innerHTML = formatInsightsText(data.industryInsights) || 'Error generating industry insights';
        companyInsights.innerHTML = formatInsightsText(data.companyInsights) || 'Error generating company insights';
        visionInsights.innerHTML = formatInsightsText(data.visionInsights) || 'Error generating vision insights';
        recommendedTalkTrack.innerHTML = formatInsightsText(data.recommendedTalkTrack) || 'Error generating talk track';
        
    } catch (error) {
        console.error('Error generating research:', error);
        setError('An error occurred while generating research');
    } finally {
        setLoadingState(false);
    }
}

/**
 * Saves the current research to Airtable
 * Collects insights from the DOM and sends to backend
 * Displays alert upon success or failure
 */
async function saveToAirtable() {
    const accountName = accountSelect.value;
    if (!accountName) {
        alert('Please select an account');
        return;
    }
    
    // Collect the current insights from the DOM
    const data = {
        accountName,
        industryInsights: industryInsights.innerHTML,
        companyInsights: companyInsights.innerHTML,
        visionInsights: visionInsights.innerHTML,
        recommendedTalkTrack: recommendedTalkTrack.innerHTML
    };
    
    try {
        const response = await fetch('/api/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Research saved successfully to Airtable!');
        } else {
            alert(`Error saving research: ${result.message}`);
        }
    } catch (error) {
        console.error('Error saving to Airtable:', error);
        alert('An error occurred while saving to Airtable');
    }
}

// Helper functions
/**
 * Sets the loading state of the UI
 * Disables interactive elements and shows loading text when isLoading is true
 * Re-enables elements when isLoading is false
 * 
 * @param {boolean} isLoading - Whether the app is in a loading state
 */
function setLoadingState(isLoading) {
    const elements = [generateBtn, saveBtn, accountSelect];
    elements.forEach(el => {
        if (isLoading) {
            el.classList.add('loading');
            el.disabled = true;
        } else {
            el.classList.remove('loading');
            el.disabled = false;
        }
    });
    
    const contentAreas = [industryInsights, companyInsights, visionInsights, recommendedTalkTrack];
    
    if (isLoading) {
        generateBtn.innerHTML = 'Fetching Research <span class="dots"></span>';
        
        contentAreas.forEach(area => {
            area.classList.add('loading');
            area.innerHTML = '<div class="loading-message">Researching with AI, please wait...</div>';
        });
        
        // Add specific messages for each area
        industryInsights.innerHTML = '<div class="loading-message">Analyzing industry trends...</div>';
        companyInsights.innerHTML = '<div class="loading-message">Gathering company insights...</div>';
        visionInsights.innerHTML = '<div class="loading-message">Developing forward-thinking vision...</div>';
        recommendedTalkTrack.innerHTML = '<div class="loading-message">Crafting your talk track...</div>';
    } else {
        generateBtn.innerHTML = 'Generate Research';
        
        contentAreas.forEach(area => {
            area.classList.remove('loading');
        });
    }
}

/**
 * Sets all insight elements to display an error message
 * 
 * @param {string} message - The error message to display
 */
function setError(message) {
    industryInsights.textContent = message;
    companyInsights.textContent = message;
    visionInsights.textContent = message;
    recommendedTalkTrack.textContent = message;
}

/**
 * Formats the insight text to properly display headers as bold and handle links
 * 
 * @param {string} text - The text to format
 * @returns {string} - Formatted HTML string
 */
function formatInsightsText(text) {
    if (!text) return '';
    
    // Replace **Header** patterns with bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Replace bracket citations with nothing (remove them)
    text = text.replace(/\[\d+\]/g, '');
    
    return text;
}

// Event listeners
generateBtn.addEventListener('click', generateResearch);
saveBtn.addEventListener('click', saveToAirtable);

// Initialize the application
checkUserLogin();
loadAccounts();

document.addEventListener('DOMContentLoaded', function() {
    // Check for auth token
    const token = localStorage.getItem('auth_token');
    const username = localStorage.getItem('username');
    
    if (token && username) {
        document.getElementById('username').textContent = username;
    }
    
    // Check for account parameter in URL
    const urlParams = new URLSearchParams(window.location.search);
    const accountParam = urlParams.get('account');
    
    const accountSelect = document.getElementById('accountSelect');
    const generateBtn = document.getElementById('generateBtn');
    const saveToLibraryBtn = document.getElementById('saveToLibrary');
    
    // Load accounts from API
    loadAccounts();
    
    // If account parameter is present, select it and trigger research
    if (accountParam) {
        const interval = setInterval(() => {
            if (accountSelect.options.length > 1) {
                selectAccountByName(accountParam);
                clearInterval(interval);
            }
        }, 100);
    }
    
    // Add event listeners
    generateBtn.addEventListener('click', generateResearch);
    saveToLibraryBtn.addEventListener('click', saveToLibrary);
    
    // Functions
    function loadAccounts() {
        fetch('/api/accounts')
            .then(response => response.json())
            .then(data => {
                // Sort accounts alphabetically
                data.sort((a, b) => a.name.localeCompare(b.name));
                
                // Add accounts to dropdown
                data.forEach(account => {
                    const option = document.createElement('option');
                    option.value = account.name;
                    option.textContent = account.name;
                    accountSelect.appendChild(option);
                });
                
                // If account parameter is present, select it
                if (accountParam) {
                    selectAccountByName(accountParam);
                }
            })
            .catch(error => {
                console.error('Error loading accounts:', error);
            });
    }
    
    function selectAccountByName(name) {
        for (let i = 0; i < accountSelect.options.length; i++) {
            if (accountSelect.options[i].value === name) {
                accountSelect.selectedIndex = i;
                break;
            }
        }
    }
    
    function generateResearch() {
        const selectedAccount = accountSelect.value;
        if (!selectedAccount) {
            alert('Please select an account');
            return;
        }
        
        // Show loading state
        document.getElementById('industryInsights').innerHTML = '<div class="loading-placeholder"></div>';
        document.getElementById('companyInsights').innerHTML = '<div class="loading-placeholder"></div>';
        document.getElementById('visionInsights').innerHTML = '<div class="loading-placeholder"></div>';
        document.getElementById('recommendedTalkTrack').innerHTML = '<div class="loading-placeholder"></div>';
        
        // Disable button during loading
        generateBtn.disabled = true;
        
        // Make API request
        fetch('/api/research', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : ''
            },
            body: JSON.stringify({ account: selectedAccount })
        })
        .then(response => response.json())
        .then(data => {
            // Update the insights with the data
            document.getElementById('industryInsights').innerHTML = formatContent(data.industry_insights);
            document.getElementById('companyInsights').innerHTML = formatContent(data.company_insights);
            document.getElementById('visionInsights').innerHTML = formatContent(data.forward_thinking);
            document.getElementById('recommendedTalkTrack').innerHTML = formatContent(data.talk_track);
            
            // Re-enable the button
            generateBtn.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            
            // Show error message
            document.getElementById('industryInsights').innerHTML = 'Error generating research. Please try again.';
            document.getElementById('companyInsights').innerHTML = 'Error generating research. Please try again.';
            document.getElementById('visionInsights').innerHTML = 'Error generating research. Please try again.';
            document.getElementById('recommendedTalkTrack').innerHTML = 'Error generating research. Please try again.';
            
            // Re-enable the button
            generateBtn.disabled = false;
        });
    }
    
    function saveToLibrary() {
        const selectedAccount = accountSelect.value;
        if (!selectedAccount) {
            alert('Please select an account and generate research first');
            return;
        }
        
        const industryInsights = document.getElementById('industryInsights').innerText;
        const companyInsights = document.getElementById('companyInsights').innerText;
        const forwardThinking = document.getElementById('visionInsights').innerText;
        const talkTrack = document.getElementById('recommendedTalkTrack').innerText;
        
        // Check if content has been generated
        if (industryInsights.includes('Select an account') || 
            industryInsights.includes('loading-placeholder')) {
            alert('Please generate research before saving to library');
            return;
        }
        
        // Prepare data for saving
        const libraryEntry = {
            account: selectedAccount,
            industry_insights: industryInsights,
            company_insights: companyInsights,
            forward_thinking: forwardThinking,
            talk_track: talkTrack,
            date: new Date().toISOString(),
            tags: ['auto-generated']
        };
        
        // Save to library
        fetch('/api/library', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : ''
            },
            body: JSON.stringify(libraryEntry)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to save to library');
            }
            return response.json();
        })
        .then(data => {
            alert('Successfully saved to library!');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to save to library. Please try again.');
        });
    }
    
    function formatContent(content) {
        if (!content || content.trim() === '') {
            return '<p>No information available.</p>';
        }
        
        // Process the content in stages for better formatting
        
        // First, identify and convert major sections (numbered sections like "1. AI Adoption Trends:")
        const sectionsRegex = /(^|\n)(\d+\. [A-Z][^\n:]+):/g;
        content = content.replace(sectionsRegex, '$1**$2:**');
        
        // Handle any other bold headers (text already between ** **)
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Handle paragraphs and lists
        return content.split('\n\n').map(paragraph => {
            if (paragraph.trim() === '') return '';
            
            // If the paragraph contains a strong tag at the beginning, it's a section header
            if (paragraph.startsWith('<strong>') && paragraph.indexOf('</strong>') > 0) {
                // Extract the header text
                const headerText = paragraph.match(/<strong>(.*?)<\/strong>/)?.[1] || '';
                const remainingContent = paragraph.replace(/<strong>.*?<\/strong>:?\s*/, '');
                
                // If there's content after the header, format it
                if (remainingContent.trim()) {
                    return `<div class="section-container">
                              <h3 class="section-header">${headerText}</h3>
                              <div class="section-content">${formatParagraphContent(remainingContent)}</div>
                            </div>`;
                } else {
                    return `<h3 class="section-header">${headerText}</h3>`;
                }
            }
            
            // Check if paragraph starts with a number followed by a period (numbered list)
            else if (paragraph.match(/^\d+\.\s/)) {
                // Convert to proper HTML list if it contains multiple items
                if (paragraph.includes('\n')) {
                    return formatNumberedList(paragraph);
                }
                return `<div class="content-item">${paragraph}</div>`;
            } 
            // Check if paragraph has bullet points (lines starting with - or *)
            else if (paragraph.includes('\n-') || paragraph.includes('\n*') || paragraph.startsWith('-') || paragraph.startsWith('*')) {
                return formatBulletList(paragraph);
            } 
            // Headers (lines ending with : might be headers)
            else if (paragraph.includes('\n') && paragraph.split('\n')[0].endsWith(':')) {
                const lines = paragraph.split('\n');
                const header = lines.shift(); // Remove the first line
                return `<div class="sub-section">
                          <h4 class="sub-header">${header}</h4>
                          <div class="sub-content">${formatParagraphContent(lines.join('\n'))}</div>
                        </div>`;
            }
            else {
                return `<p>${paragraph}</p>`;
            }
        }).join('');
    }
    
    // Helper function to format bullet lists
    function formatBulletList(paragraph) {
        const items = paragraph.split('\n');
        let listHTML = '<ul class="insight-list">';
        let headerText = '';
        
        // Check if the first item is a header (not starting with - or *)
        if (items.length > 0 && !items[0].trim().startsWith('-') && !items[0].trim().startsWith('*')) {
            headerText = items.shift();
        }
        
        // Process remaining items as list items
        items.forEach(item => {
            if (item.trim().startsWith('-') || item.trim().startsWith('*')) {
                const cleanItem = item.replace(/^[-*]\s/, '');
                listHTML += `<li>${cleanItem}</li>`;
            } else if (item.trim() !== '') {
                // If we encounter non-bullet text in the middle, treat it as a sub-header
                listHTML += `<li class="list-subheader">${item}</li>`;
            }
        });
        
        listHTML += '</ul>';
        
        // If we had a header, prepend it
        if (headerText) {
            return `<div class="list-container">
                      <h4 class="list-header">${headerText}</h4>
                      ${listHTML}
                    </div>`;
        }
        
        return listHTML;
    }
    
    // Helper function to format numbered lists
    function formatNumberedList(paragraph) {
        const items = paragraph.split('\n');
        let listHTML = '<ol class="numbered-list">';
        let headerText = '';
        
        // Check if the first item should be treated as a header
        if (items.length > 0 && items[0].match(/^\d+\.\s[A-Z]/) && !items[0].trim().endsWith(':')) {
            // Keep it as the first list item, but don't extract as header
            const cleanItem = items[0].replace(/^\d+\.\s/, '');
            listHTML += `<li><strong>${cleanItem}</strong></li>`;
            items.shift();
        }
        
        // Process remaining items
        items.forEach(item => {
            if (item.match(/^\d+\.\s/)) {
                const cleanItem = item.replace(/^\d+\.\s/, '');
                listHTML += `<li>${cleanItem}</li>`;
            } else if (item.trim() !== '') {
                // Non-numbered lines become part of the previous item or sub-points
                listHTML += `<li class="sub-point">${item}</li>`;
            }
        });
        
        listHTML += '</ol>';
        
        return listHTML;
    }
    
    // Helper function to format paragraph content, handling inline lists
    function formatParagraphContent(text) {
        if (!text || text.trim() === '') return '';
        
        // Split by new lines but maintain structure
        const lines = text.split('\n');
        let formattedContent = '';
        let inList = false;
        let listItems = [];
        
        lines.forEach(line => {
            const trimmedLine = line.trim();
            
            // Check if line is a bullet point
            if (trimmedLine.startsWith('-') || trimmedLine.startsWith('*')) {
                if (!inList) {
                    inList = true;
                    listItems = [];
                }
                listItems.push(trimmedLine.replace(/^[-*]\s/, ''));
            } 
            // Check if line is a numbered item
            else if (trimmedLine.match(/^\d+\.\s/)) {
                if (!inList) {
                    inList = true;
                    listItems = [];
                }
                listItems.push(trimmedLine.replace(/^\d+\.\s/, ''));
            }
            // Regular line
            else {
                // If we were in a list, close it
                if (inList) {
                    formattedContent += '<ul class="insight-list">';
                    listItems.forEach(item => {
                        formattedContent += `<li>${item}</li>`;
                    });
                    formattedContent += '</ul>';
                    inList = false;
                }
                
                // Add the regular line
                if (trimmedLine !== '') {
                    formattedContent += `<p>${trimmedLine}</p>`;
                }
            }
        });
        
        // Close any open list
        if (inList) {
            formattedContent += '<ul class="insight-list">';
            listItems.forEach(item => {
                formattedContent += `<li>${item}</li>`;
            });
            formattedContent += '</ul>';
        }
        
        return formattedContent;
    }
});

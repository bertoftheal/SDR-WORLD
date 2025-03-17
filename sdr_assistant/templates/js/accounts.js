/**
 * Accounts Page JavaScript
 * 
 * This file contains the client-side logic for the SDR World Accounts page.
 * It handles account data loading, filtering, and research display.
 */

// DOM Elements
let accountsContainer;
let accountDetailsContainer;
let accountSearchInput;
let accountSearchBtn;
let statusFilter;
let industryFilter;
let sortFilter;
let resetFiltersBtn;
let backToAccountsBtn;
let generateResearchBtn;

// Current selected account
let currentAccountId = null;

// Initialize when document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initDOMElements();
    checkUserLogin();
    loadAccounts();
    setupEventListeners();
});

// Initialize DOM Elements
function initDOMElements() {
    accountsContainer = document.getElementById('accountsContainer');
    accountDetailsContainer = document.getElementById('accountDetailsContainer');
    accountSearchInput = document.getElementById('accountSearchInput');
    accountSearchBtn = document.getElementById('accountSearchBtn');
    statusFilter = document.getElementById('statusFilter');
    industryFilter = document.getElementById('industryFilter');
    sortFilter = document.getElementById('sortFilter');
    resetFiltersBtn = document.getElementById('resetFilters');
    backToAccountsBtn = document.getElementById('backToAccounts');
    generateResearchBtn = document.getElementById('generateResearchBtn');
}

// Check if user is logged in
function checkUserLogin() {
    const userName = document.getElementById('userName');
    if (!userName) return;
    
    // For demo, use static name
    userName.textContent = 'Albert Perez';
}

// Setup Event Listeners
function setupEventListeners() {
    if (!accountSearchBtn || !accountsContainer) return;
    
    // Search functionality
    accountSearchBtn.addEventListener('click', filterAccounts);
    if (accountSearchInput) {
        accountSearchInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                filterAccounts();
            }
        });
    }
    
    // Filter change events
    if (statusFilter) statusFilter.addEventListener('change', filterAccounts);
    if (industryFilter) industryFilter.addEventListener('change', filterAccounts);
    if (sortFilter) sortFilter.addEventListener('change', filterAccounts);
    
    // Reset filters
    if (resetFiltersBtn) resetFiltersBtn.addEventListener('click', resetFilters);
    
    // Navigation between accounts list and details
    if (backToAccountsBtn) backToAccountsBtn.addEventListener('click', showAccountsList);
    
    // Research generation
    if (generateResearchBtn) generateResearchBtn.addEventListener('click', generateResearch);
    
    // Initialize tabs if they exist
    const tabsElement = document.getElementById('researchTabs');
    if (tabsElement) {
        const triggerTabList = tabsElement.querySelectorAll('button');
        triggerTabList.forEach(triggerEl => {
            triggerEl.addEventListener('click', event => {
                event.preventDefault();
                const tabTarget = document.querySelector(triggerEl.dataset.bsTarget);
                if (tabTarget) {
                    // Hide all tab panes
                    document.querySelectorAll('.tab-pane').forEach(pane => {
                        pane.classList.remove('show', 'active');
                    });
                    // Show the selected tab pane
                    tabTarget.classList.add('show', 'active');
                    
                    // Update active state on tabs
                    triggerTabList.forEach(el => el.classList.remove('active'));
                    triggerEl.classList.add('active');
                }
            });
        });
    }
    
    // Add event listeners to view account buttons after accounts are loaded
    document.querySelectorAll('.view-account-btn').forEach(button => {
        button.addEventListener('click', function() {
            const accountId = this.getAttribute('data-account-id');
            showAccountDetails(accountId);
        });
    });
}

// Load accounts from API or demo data
function loadAccounts() {
    console.log("Loading accounts...");
    if (!accountsContainer) return;
    
    // In demo mode, use static data
    const accounts = [
        {
            id: "nvidia",
            name: "NVIDIA",
            industry: "Technology",
            location: "Santa Clara, CA",
            logo: "https://logo.clearbit.com/nvidia.com",
            status: "researched",
            lastResearch: "2025-03-10",
            description: "NVIDIA is a technology company known for designing graphics processing units (GPUs) for gaming and professional markets, as well as system on a chip units (SoCs) for the mobile computing and automotive market."
        },
        {
            id: "google",
            name: "Google",
            industry: "Technology",
            location: "Mountain View, CA",
            logo: "https://logo.clearbit.com/google.com",
            status: "researched",
            lastResearch: "2025-03-05",
            description: "Google LLC is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, a search engine, cloud computing, software, and hardware."
        },
        {
            id: "microsoft",
            name: "Microsoft",
            industry: "Technology",
            location: "Redmond, WA",
            logo: "https://logo.clearbit.com/microsoft.com",
            status: "researched",
            lastResearch: "2025-03-01",
            description: "Microsoft Corporation is an American multinational technology company that develops, manufactures, licenses, supports, and sells computer software, consumer electronics, personal computers, and related services."
        },
        {
            id: "amazon",
            name: "Amazon",
            industry: "Retail",
            location: "Seattle, WA",
            logo: "https://logo.clearbit.com/amazon.com",
            status: "pending",
            lastResearch: null,
            description: "Amazon.com, Inc. is an American multinational technology company which focuses on e-commerce, cloud computing, digital streaming, and artificial intelligence."
        },
        {
            id: "jpmorgan",
            name: "JP Morgan Chase",
            industry: "Finance",
            location: "New York, NY",
            logo: "https://logo.clearbit.com/jpmorganchase.com",
            status: "pending",
            lastResearch: null,
            description: "JPMorgan Chase & Co. is an American multinational investment bank and financial services holding company headquartered in New York City."
        }
    ];
    
    displayAccounts(accounts);
}

// Display accounts in the UI
function displayAccounts(accounts) {
    if (!accountsContainer) return;
    accountsContainer.innerHTML = '';
    
    accounts.forEach(account => {
        const accountCard = document.createElement('div');
        accountCard.className = 'col';
        accountCard.innerHTML = `
            <div class="account-card card h-100 shadow-sm">
                <div class="card-body">
                    <div class="d-flex mb-3">
                        <div class="account-logo me-3">
                            ${account.logo ? 
                              `<img src="${account.logo}" alt="${account.name}" width="60" height="60">` : 
                              `<i class="fas fa-building fa-2x text-muted"></i>`}
                        </div>
                        <div>
                            <h5 class="card-title mb-1">${account.name}</h5>
                            <div class="text-muted small">${account.industry}</div>
                        </div>
                        <div class="ms-auto">
                            <span class="badge ${account.status === 'researched' ? 'badge-research' : 'badge-pending'}">
                                ${account.status === 'researched' ? 'Researched' : 'Pending'}
                            </span>
                        </div>
                    </div>
                    <p class="card-text small mb-3 text-truncate">${account.description}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="fas fa-map-marker-alt me-1"></i>${account.location}
                        </small>
                        ${account.lastResearch ? 
                          `<small class="text-muted">Last updated: ${formatDate(account.lastResearch)}</small>` : 
                          ''}
                    </div>
                </div>
                <div class="card-footer bg-transparent">
                    <div class="d-grid">
                        <button class="btn btn-outline-secondary view-account-btn" data-account-id="${account.id}">
                            <i class="fas fa-eye me-2"></i>View Account
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        accountsContainer.appendChild(accountCard);
    });
    
    // Add event listeners to view account buttons
    document.querySelectorAll('.view-account-btn').forEach(button => {
        button.addEventListener('click', function() {
            const accountId = this.getAttribute('data-account-id');
            showAccountDetails(accountId);
        });
    });
}

// Show account details
function showAccountDetails(accountId) {
    // Instead of showing inline details, redirect to the dedicated account detail page
    window.location.href = `account-detail.html?id=${accountId}`;
}

// Show accounts list
function showAccountsList() {
    if (!accountDetailsContainer || !accountsContainer) return;
    
    // Hide details and show accounts list
    accountDetailsContainer.classList.remove('active');
    accountsContainer.parentElement.style.display = '';
}

// Filter accounts
function filterAccounts() {
    if (!accountSearchInput) return;
    
    const searchTerm = accountSearchInput.value.toLowerCase();
    const status = statusFilter ? statusFilter.value : 'all';
    const industry = industryFilter ? industryFilter.value : 'all';
    const sort = sortFilter ? sortFilter.value : 'name-asc';
    
    // Implement filtering logic here
    console.log(`Filtering accounts - Search: ${searchTerm}, Status: ${status}, Industry: ${industry}, Sort: ${sort}`);
    
    // For now, just reload all accounts
    loadAccounts();
}

// Reset filters
function resetFilters() {
    if (accountSearchInput) accountSearchInput.value = '';
    if (statusFilter) statusFilter.value = 'all';
    if (industryFilter) industryFilter.value = 'all';
    if (sortFilter) sortFilter.value = 'name-asc';
    
    // Reload accounts
    loadAccounts();
}

// Load account details
function loadAccountDetails(accountId) {
    console.log(`Loading details for account ID: ${accountId}`);
    
    // For demo purposes, load static data based on account ID
    if (accountId === 'nvidia') {
        loadNvidiaDetails();
    } else {
        // Generic placeholder
        const nameEl = document.getElementById('accountDetailName');
        const industryEl = document.getElementById('accountDetailIndustry');
        const infoEl = document.getElementById('accountDetailInfo');
        const contactEl = document.getElementById('accountDetailContact');
        
        if (nameEl) nameEl.textContent = 'Selected Account';
        if (industryEl) industryEl.textContent = 'Industry Placeholder';
        if (infoEl) infoEl.textContent = 'No detailed information available.';
        if (contactEl) contactEl.textContent = 'No contact information available.';
    }
}

// Generate research for current account
function generateResearch() {
    if (!currentAccountId) return;
    
    const generateBtn = document.getElementById('generateResearchBtn');
    if (!generateBtn) return;
    
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
    
    // Simulate API call with timeout
    setTimeout(() => {
        // Update UI with research results
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Generate Research';
        
        // Show success notification
        showNotification('Research generated successfully!', 'success');
    }, 3000);
}

// Format date helper function
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `toast align-items-center text-white bg-${type} border-0`;
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'assertive');
    notification.setAttribute('aria-atomic', 'true');
    
    notification.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add to DOM
    const toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
    toastContainer.appendChild(notification);
    document.body.appendChild(toastContainer);
    
    // Show notification
    if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
        const toast = new bootstrap.Toast(notification);
        toast.show();
    } else {
        // Fallback if Bootstrap JS is not loaded
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.display = 'none';
            document.body.removeChild(toastContainer);
        }, 5000);
    }
    
    // Remove from DOM after hiding
    notification.addEventListener('hidden.bs.toast', function () {
        if (document.body.contains(toastContainer)) {
            document.body.removeChild(toastContainer);
        }
    });
}

// Load NVIDIA account details (for demo)
function loadNvidiaDetails() {
    const logoEl = document.getElementById('accountDetailLogo');
    const nameEl = document.getElementById('accountDetailName');
    const industryEl = document.getElementById('accountDetailIndustry');
    const infoEl = document.getElementById('accountDetailInfo');
    const contactEl = document.getElementById('accountDetailContact');
    
    if (logoEl) logoEl.innerHTML = '<img src="https://logo.clearbit.com/nvidia.com" alt="NVIDIA" width="60" height="60">';
    if (nameEl) nameEl.textContent = 'NVIDIA';
    if (industryEl) industryEl.textContent = 'Technology - Semiconductors';
    
    if (infoEl) {
        infoEl.innerHTML = `
            <p><strong>Founded:</strong> 1993</p>
            <p><strong>CEO:</strong> Jensen Huang</p>
            <p><strong>Employees:</strong> 22,000+</p>
            <p><strong>Revenue:</strong> $26.9 billion (2023)</p>
            <p><strong>Products:</strong> GPUs, AI/ML platforms, Gaming hardware, Data center solutions</p>
        `;
    }
    
    if (contactEl) {
        contactEl.innerHTML = `
            <p><strong>Headquarters:</strong> Santa Clara, California, United States</p>
            <p><strong>Website:</strong> <a href="https://www.nvidia.com" target="_blank">www.nvidia.com</a></p>
            <p><strong>Phone:</strong> +1 (408) 486-2000</p>
        `;
    }
    
    // Load research tabs content
    loadNvidiaResearchTabs();
}

// Load NVIDIA research tabs content
function loadNvidiaResearchTabs() {
    const companyInsightsEl = document.getElementById('companyInsightsGrid');
    const industryInsightsEl = document.getElementById('industryInsightsGrid');
    const talkTrackEl = document.getElementById('talkTrackContent');
    const historyEl = document.getElementById('researchHistoryTableBody');
    
    if (companyInsightsEl) {
        companyInsightsEl.innerHTML = `
            <div class="col">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between mb-3">
                            <h5 class="card-title">AI Leadership</h5>
                            <span class="badge bg-success">Strength</span>
                        </div>
                        <p class="card-text">NVIDIA has established itself as the dominant player in AI computing, with its GPUs being the preferred choice for training and running large AI models.</p>
                    </div>
                </div>
            </div>
            <div class="col">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between mb-3">
                            <h5 class="card-title">Data Center Growth</h5>
                            <span class="badge bg-success">Strength</span>
                        </div>
                        <p class="card-text">Data center revenue has grown to become NVIDIA's largest segment, with 141% year-over-year growth, reflecting increased demand for AI infrastructure.</p>
                    </div>
                </div>
            </div>
            <div class="col">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between mb-3">
                            <h5 class="card-title">Supply Chain Risks</h5>
                            <span class="badge bg-warning">Challenge</span>
                        </div>
                        <p class="card-text">Heavy reliance on TSMC for manufacturing creates potential supply chain vulnerabilities, especially amid ongoing chip shortages and geopolitical tensions.</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    if (industryInsightsEl) {
        industryInsightsEl.innerHTML = `
            <div class="col">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between mb-3">
                            <h5 class="card-title">AI Acceleration</h5>
                            <span class="badge bg-primary">Trend</span>
                        </div>
                        <p class="card-text">The global AI hardware market is projected to grow at a CAGR of 37% through 2028, driven by generative AI applications and enterprise adoption.</p>
                    </div>
                </div>
            </div>
            <div class="col">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between mb-3">
                            <h5 class="card-title">Competitor Landscape</h5>
                            <span class="badge bg-info">Analysis</span>
                        </div>
                        <p class="card-text">While AMD and Intel are making strides in AI chips, NVIDIA maintains a significant lead in software ecosystem (CUDA) and performance for AI workloads.</p>
                    </div>
                </div>
            </div>
            <div class="col">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between mb-3">
                            <h5 class="card-title">Regulatory Scrutiny</h5>
                            <span class="badge bg-warning">Challenge</span>
                        </div>
                        <p class="card-text">Increasing government regulations around AI chip exports, particularly to China, could impact global sales strategies for semiconductor companies.</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    if (talkTrackEl) {
        talkTrackEl.innerHTML = `
            <div class="mb-4">
                <h5>Introduction</h5>
                <p>Hi [Contact Name], I've been researching NVIDIA and noticed how your data center business has seen extraordinary growth with the surge in AI adoption. I'm particularly impressed by the 141% year-over-year growth in this segment.</p>
            </div>
            
            <div class="mb-4">
                <h5>Value Proposition</h5>
                <p>Given your focus on AI infrastructure and the challenges in scaling to meet demand, our solution could help optimize your supply chain resilience while maintaining your competitive edge in AI chip production. We've helped similar technology manufacturers reduce supply chain vulnerabilities by 32% while improving time-to-market.</p>
            </div>
            
            <div class="mb-4">
                <h5>Question</h5>
                <p>I'm curious - with the continued expansion of your data center business, what are your biggest challenges in scaling infrastructure to meet the growing demand for AI computing resources?</p>
            </div>
            
            <div>
                <h5>Call to Action</h5>
                <p>Would it make sense to schedule a brief call next week to discuss how our platform could support NVIDIA's growth strategy in the AI infrastructure space? I'd be happy to share some specific case studies from our work with other semiconductor companies.</p>
            </div>
        `;
    }
    
    if (historyEl) {
        historyEl.innerHTML = `
            <tr>
                <td>March 10, 2025</td>
                <td>Full Company Research</td>
                <td>Albert Perez</td>
                <td>
                    <button class="btn btn-sm btn-outline-secondary me-1">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary me-1">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
            <tr>
                <td>February 20, 2025</td>
                <td>Quarterly Update</td>
                <td>Albert Perez</td>
                <td>
                    <button class="btn btn-sm btn-outline-secondary me-1">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary me-1">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
            <tr>
                <td>December 15, 2024</td>
                <td>Initial Research</td>
                <td>Albert Perez</td>
                <td>
                    <button class="btn btn-sm btn-outline-secondary me-1">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary me-1">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    }
}

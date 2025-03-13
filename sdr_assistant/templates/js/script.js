/**
 * SDR World - Frontend JavaScript
 * 
 * This file contains the client-side logic for the SDR World application.
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
const saveBtn = document.querySelector('.save-btn');
const companyName = document.querySelector('.company-name');
const companyDescription = document.querySelector('.company-description');
const companyMetaItems = document.querySelectorAll('.meta-value');
const companyInsightsGrid = document.querySelector('.company-insights .insights-grid');
const industryInsightsGrid = document.querySelector('.industry-insights .insights-grid');
const futureInsightsGrid = document.querySelector('.future-insights .insights-grid');
const talkTrackContent = document.querySelector('.talk-track-content');
const userName = document.getElementById('userName');
const heroImage = document.querySelector('.hero-image img');

// DEMO MODE - For static HTML preview
const DEMO_MODE = true;

// Check if user is logged in
function checkUserLogin() {
    if (DEMO_MODE) {
        userName.textContent = 'Albert Perez'; // Default for demo
        return;
    }
    
    const token = localStorage.getItem('auth_token');
    if (token) {
        // User is logged in
        fetch('/api/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.name) {
                userName.textContent = data.name;
            }
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
        });
    } else {
        // No token found, user needs to log in
        userName.textContent = 'Albert Perez'; // Default for demo
    }
}

/**
 * Loads account data from the backend API or uses static data in demo mode
 */
function loadAccounts() {
    console.log("Loading accounts...");
    
    if (DEMO_MODE) {
        // Use static fallback data in demo mode
        // Clear existing options and add the placeholder
        accountSelect.innerHTML = '<option value="">Select an account...</option>';
        
        // Add static company options
        const staticCompanies = [
            { id: 'cisco', name: 'Cisco Systems' },
            { id: 'microsoft', name: 'Microsoft Corporation' },
            { id: 'google', name: 'Google (Alphabet Inc.)' },
            { id: 'amazon', name: 'Amazon.com, Inc.' }
        ];
        
        staticCompanies.forEach(company => {
            const option = document.createElement('option');
            option.value = company.id;
            option.textContent = company.name;
            option.dataset.id = company.id;
            accountSelect.appendChild(option);
        });
        
        console.log('Populated dropdown with static company data');
        return;
    }
    
    // Not in demo mode, fetch from API
    fetch('/api/accounts')
        .then(response => response.json())
        .then(accounts => {
            // Clear existing options except the placeholder
            accountSelect.innerHTML = '<option value="">Select an account...</option>';
            
            // Keep track of added account names to prevent duplicates
            const addedAccounts = new Set();
            
            // Sort accounts alphabetically
            accounts.sort((a, b) => a.name.localeCompare(b.name));
            
            // Add new options while filtering out duplicates
            accounts.forEach(account => {
                // Skip if this account name has already been added
                if (addedAccounts.has(account.name)) {
                    console.log(`Skipping duplicate account: ${account.name}`);
                    return;
                }
                
                // Add the account name to the set and create the option
                addedAccounts.add(account.name);
                const option = document.createElement('option');
                option.value = account.name;
                option.textContent = account.name;
                option.dataset.id = account.id; // Store ID for reference
                accountSelect.appendChild(option);
            });
            
            console.log(`Loaded ${addedAccounts.size} unique accounts from API`);
        })
        .catch(error => {
            console.error('Error loading accounts from API:', error);
        });
}

/**
 * Updates the company details based on selected company
 */
function updateCompanyDetails() {
    const selectedCompany = accountSelect.value;
    console.log("Selected company:", selectedCompany);
    
    // This is just a placeholder function with static data
    // In a real implementation, this would fetch data from an API
    const companyData = {
        'cisco': {
            name: 'Cisco Systems',
            headquarters: 'San Jose, California, United States',
            employees: '83,300+',
            marketCap: '$198.5 Billion',
            founded: '1984',
            description: 'Cisco Systems, Inc. designs, manufactures, and sells Internet Protocol based networking and other products related to the communications and information technology industry worldwide.',
            logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Cisco_logo_blue_2016.svg/1200px-Cisco_logo_blue_2016.svg.png',
            insights: {
                financial: {
                    title: 'Strong recurring revenue growth',
                    content: 'Cisco has been successfully transitioning to a subscription-based model, with software and services now representing over 50% of their revenue, providing more stable and predictable income streams.',
                    trend: 'positive'
                },
                product: {
                    title: 'Focus on cloud security and networking',
                    content: 'Cisco has been expanding its portfolio beyond hardware to include cloud security, SD-WAN, and network management software, aligning with enterprise digital transformation initiatives.',
                    trend: 'positive'
                },
                leadership: {
                    title: 'Strong leadership in network transformation',
                    content: 'Under CEO Chuck Robbins, Cisco has accelerated its shift to software and services while maintaining leadership in core networking hardware markets.',
                    trend: 'positive'
                }
            },
            industryInsights: [
                {
                    title: 'Network Security Consolidation',
                    content: 'The industry is moving toward unified security platforms that integrate networking and security functions, reducing complexity and improving threat response times.',
                    type: 'Market Shift'
                },
                {
                    title: 'Software-Defined Networking Growth',
                    content: 'SDN and intent-based networking are replacing traditional hardware-centric approaches, with IDC predicting that 60% of enterprises will implement fully software-defined networks by 2025.',
                    type: 'Trend'
                }
            ],
            futureInsights: [
                {
                    title: 'AI Network Management',
                    content: 'AI-driven network management and automation will reduce manual configuration by 70%, decreasing deployment time and human error while improving security response.',
                    type: 'Innovation'
                },
                {
                    title: 'Edge Computing Integration',
                    content: 'By 2026, over 75% of enterprise data will be processed at the edge, creating demand for secure, high-performance networking solutions that extend beyond traditional data centers.',
                    type: 'Trend'
                }
            ],
            talkTrack: "I noticed Cisco is making significant investments in transitioning from hardware to subscription-based services. Many of our customers in similar positions have found that this transition creates unique challenges around maintaining network performance while implementing new security architectures, especially in hybrid environments.\n\nWe've developed specialized solutions that help companies like Cisco manage this transition smoothly, ensuring that your network performance and security posture remain strong while you focus on growing your subscription business. Our platform integrates directly with Cisco's security and networking tools, creating a seamless experience for your team.\n\nWould it make sense to schedule a brief call with your network operations team to explore how we might help you accelerate this transition while maintaining enterprise-grade performance?"
        },
        'microsoft': {
            name: 'Microsoft Corporation',
            headquarters: 'Redmond, Washington, United States',
            employees: '221,000+',
            marketCap: '$2.8 Trillion',
            founded: '1975',
            description: 'Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide. The company operates through three segments: Productivity and Business Processes, Intelligent Cloud, and More Personal Computing.',
            logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/1200px-Microsoft_logo.svg.png',
            insights: {
                financial: {
                    title: 'Cloud revenue dominance',
                    content: 'Microsoft Azure continues to show exceptional growth, with cloud services now representing over 40% of total revenue and growing at 25% annually, solidifying Microsoft's position as a leader in enterprise cloud services.',
                    trend: 'positive'
                },
                product: {
                    title: 'AI integration across product lines',
                    content: 'Microsoft is heavily investing in AI capabilities across its entire product portfolio, from GitHub Copilot and Microsoft 365 Copilot to Azure OpenAI Service, creating a comprehensive AI ecosystem.',
                    trend: 'positive'
                },
                leadership: {
                    title: 'Strategic acquisitions strengthening position',
                    content: 'Under Satya Nadella's leadership, Microsoft has made strategic acquisitions like GitHub, Nuance, and Activision Blizzard to expand its reach into developer tools, healthcare AI, and gaming markets.',
                    trend: 'positive'
                }
            },
            industryInsights: [
                {
                    title: 'AI Development Democratization',
                    content: 'Enterprise AI adoption is accelerating with easier-to-use development tools, with Gartner predicting that 75% of enterprises will shift from piloting to operationalizing AI by 2026.',
                    type: 'Market Shift'
                },
                {
                    title: 'Low-Code/No-Code Growth',
                    content: 'The low-code development platform market is growing at over 25% annually, enabling business users to create applications with minimal traditional coding knowledge.',
                    type: 'Trend'
                }
            ],
            futureInsights: [
                {
                    title: 'Quantum Computing Commercialization',
                    content: 'Microsoft's Azure Quantum is positioning the company to be a leader as quantum computing becomes commercially viable for specific use cases over the next decade.',
                    type: 'Innovation'
                },
                {
                    title: 'Metaverse Enterprise Applications',
                    content: 'Microsoft Mesh and mixed reality tools are creating new enterprise collaboration models that will redefine remote work and training capabilities by 2027.',
                    type: 'Opportunity'
                }
            ],
            talkTrack: "I've been following Microsoft's impressive cloud growth and AI integration strategy, and I noticed your organization is heavily invested in the Microsoft ecosystem. Many of our clients are looking to maximize their Microsoft investments while ensuring they have the right governance and security controls in place.\n\nWe've developed a platform that enhances Microsoft's native tools by providing additional visibility and control across hybrid environments, which is especially valuable as you adopt more AI and cloud services. Our solution seamlessly integrates with Azure, Microsoft 365, and your existing security stack.\n\nWould it be valuable to schedule a brief discussion with your cloud strategy team to explore how we might help you accelerate your Microsoft-focused initiatives while ensuring proper governance?"
        },
        'google': {
            name: 'Google (Alphabet Inc.)',
            headquarters: 'Mountain View, California, United States',
            employees: '156,500+',
            marketCap: '$1.7 Trillion',
            founded: '1998',
            description: 'Google LLC is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, a search engine, cloud computing, software, and hardware.',
            logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/1200px-Google_2015_logo.svg.png',
            insights: {
                financial: {
                    title: 'Advertising dominance with cloud growth',
                    content: 'While advertising still accounts for over 75% of Google's revenue, Google Cloud is becoming a significant contributor with 45% year-over-year growth and approaching profitability.',
                    trend: 'positive'
                },
                product: {
                    title: 'AI leadership and product integration',
                    content: 'Google's AI capabilities, especially through DeepMind and Gemini models, are being systematically deployed across all major products, from Search to Workspace, enhancing user capabilities.',
                    trend: 'positive'
                },
                leadership: {
                    title: 'Focused restructuring under pressure',
                    content: 'CEO Sundar Pichai has implemented significant restructuring and workforce reduction to improve operational efficiency while facing increased competition in AI and cloud markets.',
                    trend: 'neutral'
                }
            },
            industryInsights: [
                {
                    title: 'Privacy-Centered Advertising Evolution',
                    content: 'The digital advertising industry is fundamentally changing with the deprecation of third-party cookies and increased privacy regulations, forcing new approaches to audience targeting.',
                    type: 'Market Shift'
                },
                {
                    title: 'Multi-cloud Strategy Adoption',
                    content: 'Over 85% of enterprises are now adopting multi-cloud strategies to avoid vendor lock-in and leverage best-of-breed services across providers.',
                    type: 'Trend'
                }
            ],
            futureInsights: [
                {
                    title: 'Generative AI Search Revolution',
                    content: 'Google's search business is transforming with AI-generated responses, potentially disrupting the traditional search and advertising model that has driven Google's growth for decades.',
                    type: 'Disruption'
                },
                {
                    title: 'Quantum Computing Applications',
                    content: 'Google's quantum computing research may deliver commercial applications in optimization and materials science by 2027, creating new revenue streams beyond advertising.',
                    type: 'Innovation'
                }
            ],
            talkTrack: "I've been following Google's strategic shift toward cloud and AI services while managing the transformation of its core advertising business. Many of our clients use Google Cloud alongside other providers and face challenges with consistent security controls and cost management across these environments.\n\nWe've built a solution that provides unified visibility and governance across Google Cloud, other cloud platforms, and on-premises infrastructure, which has helped similar organizations reduce cloud spend by 24% while strengthening their security posture.\n\nGiven Google's recent focus on operational efficiency, would it be valuable to connect with your cloud architecture team to discuss how our platform could help optimize your multi-cloud environment while supporting your AI and data initiatives?"
        },
        'amazon': {
            name: 'Amazon.com, Inc.',
            headquarters: 'Seattle, Washington, United States',
            employees: '1.5 Million+',
            marketCap: '$1.6 Trillion',
            founded: '1994',
            description: 'Amazon.com, Inc. engages in the retail sale of consumer products and subscriptions through online and physical stores in North America and internationally. It operates through e-commerce, AWS, and physical stores segments.',
            logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1200px-Amazon_logo.svg.png',
            insights: {
                financial: {
                    title: 'AWS profit engine with retail margin improvement',
                    content: 'While AWS contributes approximately 16% of Amazon's revenue, it generates over 70% of operating income, while the retail business is showing improved margins through logistics optimization.',
                    trend: 'positive'
                },
                product: {
                    title: 'Expanding beyond AWS to comprehensive enterprise services',
                    content: 'Amazon is broadening its B2B presence beyond AWS to include Amazon Business, supply chain services, and healthcare solutions, creating an integrated enterprise offering.',
                    trend: 'positive'
                },
                leadership: {
                    title: 'Post-Bezos transformation under Andy Jassy',
                    content: 'CEO Andy Jassy has focused on operational efficiency with significant cost-cutting measures while maintaining investment in strategic growth areas like healthcare and AI.',
                    trend: 'positive'
                }
            },
            industryInsights: [
                {
                    title: 'Supply Chain Technology Integration',
                    content: 'Advanced logistics technologies including AI-driven inventory management and autonomous fulfillment are transforming retail supply chains, with 65% of retailers planning major technology investments by 2026.',
                    type: 'Market Shift'
                },
                {
                    title: 'Hybrid Cloud Architectures',
                    content: 'Enterprise adoption of hybrid cloud architectures is accelerating, with 80% of organizations implementing workload-specific deployment strategies across public cloud, private cloud, and on-premises.',
                    type: 'Trend'
                }
            ],
            futureInsights: [
                {
                    title: 'Healthcare Ecosystem Development',
                    content: 'Amazon's strategic acquisitions in healthcare, including One Medical and PillPack, position the company to create an integrated healthcare service model that could disrupt traditional providers.',
                    type: 'Disruption'
                },
                {
                    title: 'Ambient Computing Experience',
                    content: 'Amazon's vast device ecosystem and AI capabilities are converging toward an ambient computing experience that will redefine how consumers interact with technology in their daily lives.',
                    type: 'Innovation'
                }
            ],
            talkTrack: "I've been following Amazon's evolution, particularly how AWS continues to drive profitability while you're expanding into new enterprise services. Many of our clients are heavy AWS users who are looking to optimize their cloud architecture and costs while maintaining the agility that attracted them to AWS initially.\n\nWe've developed a platform that enhances AWS's native capabilities by providing additional cost optimization, security controls, and operational insights. Our customers typically see a 22% reduction in cloud spend within the first six months while improving their security posture and governance.\n\nWould it make sense to connect with your cloud architecture team to explore how we might help you maximize your AWS investment while supporting your broader digital transformation initiatives?"
        }
    };
    
    if (selectedCompany && companyData[selectedCompany]) {
        const company = companyData[selectedCompany];
        updateCompanyInfo(company);
        updateCompanyInsights(company);
        
        // Update the hero image with the company logo
        if (heroImage && company.logoUrl) {
            // Store the original image URL if we haven't already
            if (!heroImage.dataset.originalSrc) {
                heroImage.dataset.originalSrc = heroImage.src;
            }
            
            // Change the image to the company logo
            heroImage.src = company.logoUrl;
            heroImage.alt = company.name + ' Logo';
            console.log("Updated hero image to:", company.logoUrl);
        }
    } else if (heroImage && heroImage.dataset.originalSrc) {
        // If no company is selected, restore the original image
        heroImage.src = heroImage.dataset.originalSrc;
        heroImage.alt = 'Research Team Collaborating';
    }
}

/**
 * Updates the company info section with data from the API
 */
function updateCompanyInfo(companyInfo) {
    if (companyName) {
        companyName.textContent = companyInfo.name;
    }
    
    if (companyDescription) {
        companyDescription.textContent = companyInfo.description;
    }
    
    // Update metadata items if they exist
    if (companyMetaItems && companyMetaItems.length >= 4) {
        companyMetaItems[0].textContent = companyInfo.headquarters;
        companyMetaItems[1].textContent = companyInfo.employees;
        companyMetaItems[2].textContent = companyInfo.marketCap;
        companyMetaItems[3].textContent = companyInfo.founded;
    }
}

/**
 * Updates the company insights sections with the selected company's data
 */
function updateCompanyInsights(company) {
    // Update company insights
    if (companyInsightsGrid && company.insights) {
        const insights = company.insights;
        const insightBoxes = companyInsightsGrid.querySelectorAll('.insight-box');
        
        if (insightBoxes.length >= 3) {
            // Financial Performance
            updateInsightBox(insightBoxes[0], insights.financial);
            
            // Product Portfolio
            updateInsightBox(insightBoxes[1], insights.product);
            
            // Key Leadership
            updateInsightBox(insightBoxes[2], insights.leadership);
        }
    }
    
    // Update industry insights
    if (industryInsightsGrid && company.industryInsights) {
        const insightBoxes = industryInsightsGrid.querySelectorAll('.insight-box');
        company.industryInsights.forEach((insight, index) => {
            if (index < insightBoxes.length) {
                const box = insightBoxes[index];
                const titleEl = box.querySelector('.insight-header-text');
                const contentEl = box.querySelector('.insight-body-text');
                const badgeEl = box.querySelector('.badge');
                
                if (titleEl) titleEl.textContent = insight.title;
                if (contentEl) contentEl.textContent = insight.content;
                if (badgeEl) badgeEl.innerHTML = `<i class="fas fa-chart-line me-1"></i> ${insight.type}`;
            }
        });
    }
    
    // Update future insights
    if (futureInsightsGrid && company.futureInsights) {
        const insightBoxes = futureInsightsGrid.querySelectorAll('.insight-box');
        company.futureInsights.forEach((insight, index) => {
            if (index < insightBoxes.length) {
                const box = insightBoxes[index];
                const titleEl = box.querySelector('.insight-header-text');
                const contentEl = box.querySelector('.insight-body-text');
                const badgeEl = box.querySelector('.badge');
                
                if (titleEl) titleEl.textContent = insight.title;
                if (contentEl) contentEl.textContent = insight.content;
                if (badgeEl) badgeEl.innerHTML = `<i class="fas fa-lightbulb me-1"></i> ${insight.type}`;
            }
        });
    }
    
    // Update talk track
    if (talkTrackContent && company.talkTrack) {
        talkTrackContent.innerHTML = company.talkTrack.split('\n\n').map(p => `<p class="mb-3">${p}</p>`).join('');
    }
}

/**
 * Updates a single insight box with the provided insight data
 */
function updateInsightBox(box, insight) {
    if (!box || !insight) return;
    
    const titleEl = box.querySelector('.insight-header-text');
    const contentEl = box.querySelector('.insight-body-text');
    const badgeEl = box.querySelector('.badge');
    
    if (titleEl) titleEl.textContent = insight.title;
    if (contentEl) contentEl.textContent = insight.content;
    
    if (badgeEl && insight.trend) {
        let iconClass = 'fa-arrow-right';
        let badgeClass = 'bg-secondary';
        let trendText = 'Neutral';
        
        switch (insight.trend.toLowerCase()) {
            case 'positive':
                iconClass = 'fa-arrow-up';
                badgeClass = 'bg-success';
                trendText = 'Positive Trend';
                break;
            case 'negative':
                iconClass = 'fa-arrow-down';
                badgeClass = 'bg-danger';
                trendText = 'Negative Trend';
                break;
            case 'neutral':
                iconClass = 'fa-arrow-right';
                badgeClass = 'bg-secondary';
                trendText = 'Neutral';
                break;
        }
        
        badgeEl.className = `badge rounded-pill ${badgeClass}`;
        badgeEl.innerHTML = `<i class="fas ${iconClass} me-1"></i> ${trendText}`;
    }
}

// Event listeners
if (generateBtn) {
    generateBtn.addEventListener('click', function() {
        alert('Research generation would be triggered here in the full application.');
    });
}

if (saveBtn) {
    saveBtn.addEventListener('click', function() {
        alert('Research would be saved to library here in the full application.');
    });
}

if (accountSelect) {
    accountSelect.addEventListener('change', updateCompanyDetails);
}

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    checkUserLogin();
    loadAccounts();
});

// Manually initialize for browsers that might have already fired DOMContentLoaded
if (document.readyState === 'loading') {
    console.log("Document still loading, waiting for DOMContentLoaded");
} else {
    console.log("Document already loaded, initializing immediately");
    checkUserLogin();
    loadAccounts();
}

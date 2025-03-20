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

// DOM Elements - will be initialized when document is fully loaded
let accountSelect;
let generateBtn;
let saveBtn;
let companyName;
let companyDescription;
let companyMetaItems;
let companyInsightsGrid;
let industryInsightsGrid;
let futureInsightsGrid;
let talkTrackContent;
let userName;
let heroImage;

// Default hero image URL to restore when no company is selected
const DEFAULT_HERO_IMAGE = 'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80';

// Initialize DOM elements when document is fully loaded
function initDOMElements() {
    accountSelect = document.getElementById('accountSelect');
    generateBtn = document.getElementById('generateBtn');
    saveBtn = document.querySelector('.save-btn');
    companyName = document.querySelector('.company-name');
    companyDescription = document.querySelector('.company-description');
    companyMetaItems = document.querySelectorAll('.meta-value');
    companyInsightsGrid = document.querySelector('.company-insights .insights-grid');
    industryInsightsGrid = document.querySelector('.industry-insights .insights-grid');
    futureInsightsGrid = document.querySelector('.future-insights .insights-grid');
    talkTrackContent = document.querySelector('.talk-track-content');
    userName = document.getElementById('userName');
    heroImage = document.querySelector('.hero-image img');
    console.log("Hero image element initialized:", heroImage);
}

// Use our data service instead of direct API calls
const dataService = window.dataService || new DataService();

/**
 * Initialize DOM elements when document is fully loaded
 */
function initDOMElements() {
    accountSelect = document.getElementById('accountSelect');
    generateBtn = document.getElementById('generateBtn');
    saveBtn = document.querySelector('.save-btn');
    companyName = document.querySelector('.company-name');
    companyDescription = document.querySelector('.company-description');
    companyMetaItems = document.querySelectorAll('.meta-value');
    companyInsightsGrid = document.querySelector('.company-insights .insights-grid');
    industryInsightsGrid = document.querySelector('.industry-insights .insights-grid');
    futureInsightsGrid = document.querySelector('.future-insights .insights-grid');
    talkTrackContent = document.querySelector('.talk-track-content');
    userName = document.getElementById('userName');
    heroImage = document.querySelector('.hero-image img');
    console.log("DOM elements initialized, hero image:", heroImage);
}

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
 * Loads account data using our data service
 */
function loadAccounts() {
    console.log("Loading accounts from data service...");
    
    // Clear existing options and add the placeholder
    if (accountSelect) {
        accountSelect.innerHTML = '<option value="">Select an account...</option>';
        
        // Use our data service to fetch accounts
        dataService.getAccounts()
            .then(accounts => {
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
                
                // Check if we should pre-select a company from previous research
                const currentCompany = dataService.getCurrentResearchCompany();
                if (currentCompany) {
                    const options = Array.from(accountSelect.options);
                    const matchingOption = options.find(option => option.textContent === currentCompany);
                    if (matchingOption) {
                        matchingOption.selected = true;
                        // Trigger the change event to update UI
                        const event = new Event('change');
                        accountSelect.dispatchEvent(event);
                    }
                }
                
                console.log(`Loaded ${addedAccounts.size} unique accounts from data service`);
            })
            .catch(error => {
                console.error('Error loading accounts from data service:', error);
            });
    } else {
        console.warn('Account select element not found');
    }
}

/**
 * Updates the company details based on selected company
 */
function updateCompanyDetails() {
    const selectedCompany = accountSelect.value;
    console.log("Selected company:", selectedCompany);
    console.log("DOM fully loaded when updating company details");
    
    // This is just a placeholder function with static data
    // In a real implementation, this would fetch data from an API
    const companyData = {
        'nvidia': {
            name: 'NVIDIA Corporation',
            headquarters: 'Santa Clara, California, United States',
            employees: '26,000+',
            marketCap: '$2.2 Trillion',
            founded: '1993',
            description: 'NVIDIA Corporation is an American multinational technology company that designs graphics processing units (GPUs), application programming interface (APIs) for data science and high-performance computing, and system on a chip units (SoCs) for the mobile computing and automotive market.',
            logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nvidia_logo.svg/1200px-Nvidia_logo.svg.png',
            insights: {
                financial: {
                    title: 'Explosive growth in AI compute demand',
                    content: 'NVIDIA has seen unprecedented revenue growth driven by demand for AI accelerators, with data center revenue quadrupling year-over-year as enterprises and cloud providers race to build AI infrastructure.',
                    trend: 'positive'
                },
                product: {
                    title: 'Expanding beyond GPUs to full-stack AI solutions',
                    content: 'NVIDIA has successfully transformed from a GPU manufacturer to a comprehensive AI platform company with hardware, software frameworks like CUDA and TensorRT, and enterprise solutions through NVIDIA AI Enterprise.',
                    trend: 'positive'
                },
                leadership: {
                    title: 'Visionary leadership in AI acceleration',
                    content: 'Under CEO Jensen Huang's direction, NVIDIA anticipated the AI revolution and positioned its technology at the center of the AI ecosystem years before competitors, creating substantial competitive advantages.',
                    trend: 'positive'
                }
            },
            industryInsights: [
                {
                    title: 'Generative AI Infrastructure Boom',
                    content: 'The market for specialized AI infrastructure is experiencing exponential growth, with enterprises expected to increase AI infrastructure spending by over 35% annually through 2027.',
                    type: 'Market Shift'
                },
                {
                    title: 'AI Sovereignty Investments',
                    content: 'Countries and large enterprises are investing in sovereign AI capabilities, driving demand for on-premises AI infrastructure that can deliver cloud-like capabilities with greater control and security.',
                    type: 'Trend'
                }
            ],
            futureInsights: [
                {
                    title: 'AI PC Revolution',
                    content: 'The emergence of AI PCs with dedicated neural processing units will create a new computing paradigm, with NVIDIA positioned to provide both consumer and workstation solutions for this transition.',
                    type: 'Innovation'
                },
                {
                    title: 'Autonomous Systems Integration',
                    content: 'NVIDIA's end-to-end autonomous vehicle and robotics platforms are positioned to accelerate the adoption of autonomous systems across multiple industries beyond automotive, including logistics, manufacturing, and healthcare.',
                    type: 'Opportunity'
                }
            ],
            talkTrack: "I've been following NVIDIA's remarkable growth as the AI revolution accelerates, and I'm impressed by how you've positioned yourselves at the center of the AI ecosystem. Many of our clients are implementing NVIDIA-powered AI infrastructure but facing challenges in optimizing these investments while ensuring proper governance and security controls.\n\nWe've developed solutions that complement NVIDIA's technology stack by providing enhanced visibility, cost optimization, and security for AI workloads. Our platform helps enterprises maximize their GPU utilization while ensuring that sensitive data used in AI model training remains protected.\n\nWould it make sense to connect with your enterprise AI team to explore how we might help you accelerate AI adoption among your customers while addressing their governance and operational challenges?"
        },
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
        updateTalkTrackById(company); // Use the new function with ID-based selection
        
        // Update the hero image with the company logo
        // Get reference to the hero image element - directly in the DOM
        // This approach bypasses potential stale references
        const heroImageElement = document.querySelector('.hero-image img');
        console.log("Found hero image element:", heroImageElement);
        
        if (heroImageElement && company.logoUrl) {
            // Store the original image source for later if needed
            if (!heroImageElement.dataset.originalSrc) {
                heroImageElement.dataset.originalSrc = heroImageElement.src;
                console.log("Stored original hero image in dataset:", heroImageElement.dataset.originalSrc);
            }
            
            // Apply styling to make logo look better
            heroImageElement.style.objectFit = 'contain';
            heroImageElement.style.backgroundColor = '#ffffff';
            heroImageElement.style.padding = '20px';
            
            // Directly change the img src to the company logo
            heroImageElement.src = company.logoUrl;
            heroImageElement.alt = company.name + ' Logo';
            console.log("Updated hero image to:", company.logoUrl);
        } else {
            console.error("Could not update hero image - Element:", !!heroImageElement, "Logo URL:", !!company.logoUrl);
        }
    } else if (document.querySelector('.hero-image img')) {
        // If no company is selected, restore the original image
        const heroImg = document.querySelector('.hero-image img');
        if (heroImg.dataset.originalSrc) {
            heroImg.src = heroImg.dataset.originalSrc;
        } else {
            heroImg.src = DEFAULT_HERO_IMAGE;
        }
        heroImg.alt = 'Research Team Collaborating';
        
        // Reset styling
        heroImg.style.objectFit = '';
        heroImg.style.backgroundColor = '';
        heroImg.style.padding = '';
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
 * Updates the talk track content based on the selected company
 */
function updateTalkTrack(company) {
    console.log('Updating talk track for:', company.name);
    
    // Update company name in the talk track header badge
    const companyBadge = document.querySelector('.talk-track-section .card-header .badge');
    if (companyBadge) {
        console.log('Updating company badge to:', company.name);
        companyBadge.textContent = company.name;
    } else {
        console.error('Company badge element not found');
    }
    
    // Find all the paragraph elements within the talk track content
    const paragraphs = document.querySelectorAll('.talk-track-content div p');
    console.log('Found talk track paragraphs:', paragraphs.length);
    
    if (paragraphs.length >= 3 && company.talkTrack) {
        // Split the talk track into sections
        const talkTrackParts = company.talkTrack.split('\n\n');
        console.log('Talk track parts:', talkTrackParts.length);
        
        // Update the paragraphs with the new content
        if (talkTrackParts.length >= 1) {
            paragraphs[0].textContent = talkTrackParts[0];
        }
        
        if (talkTrackParts.length >= 2) {
            paragraphs[1].textContent = talkTrackParts[1];
        }
        
        if (talkTrackParts.length >= 3) {
            paragraphs[2].textContent = talkTrackParts[2];
        }
        
        // Update generation date
        const dateElement = document.querySelector('.talk-track-box .text-muted.small');
        if (dateElement) {
            const today = new Date();
            const formattedDate = today.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            dateElement.textContent = `Generated on ${formattedDate} • Based on latest company research`;
        }
        
        console.log('Talk track updated successfully for:', company.name);
    } else {
        console.error('Talk track paragraphs not found or talk track is missing');
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
    
    // Talk track is now updated in the separate updateTalkTrack function
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
        // Get the selected account from the dropdown
        const accountSelect = document.getElementById('accountSelect');
        if (!accountSelect || !accountSelect.value || accountSelect.value === '') {
            showNotification('Please select a company first', 'warning');
            return;
        }
        
        const accountName = accountSelect.options[accountSelect.selectedIndex].text;
        const companyValue = accountSelect.value;
        
        // Show loading state
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
        
        // Clear existing content and show loading indicators
        showLoadingIndicators();
        
        // Store the selected company in our data service
        dataService.setCurrentResearchCompany(accountName);
        
        // Get the account from our data service
        dataService.getAccountByName(accountName)
            .then(account => {
                if (!account) {
                    throw new Error(`Account not found: ${accountName}`);
                }
                
                // Check if research already exists
                return dataService.getResearch(account.id)
                    .then(research => {
                        if (research) {
                            // Research exists, use it
                            console.log('Using existing research for', accountName);
                            return research;
                        } else {
                            // Research doesn't exist, generate it
                            console.log('Generating new research for', accountName);
                            return generateResearchFromAPI(accountName, companyValue);
                        }
                    });
            })
            .then(researchData => {
                updateUIWithResearchData(researchData, accountName);
                generateBtn.disabled = false;
                generateBtn.innerHTML = '<i class="fas fa-search me-2"></i>GENERATE RESEARCH';
                showNotification('Research loaded successfully!', 'success');
            })
            .catch(error => {
                console.error('Error processing research:', error);
                generateBtn.disabled = false;
                generateBtn.innerHTML = '<i class="fas fa-search me-2"></i>GENERATE RESEARCH';
                showNotification('Error generating research. Please try again.', 'error');
            });
    });
}

if (saveBtn) {
    saveBtn.addEventListener('click', function() {
        // Get the selected account name
        const accountSelect = document.getElementById('accountSelect');
        if (!accountSelect || !accountSelect.value || accountSelect.value === '') {
            showNotification('No research data to save', 'warning');
            return;
        }
        
        const accountName = accountSelect.options[accountSelect.selectedIndex].text;
        
        // Get account by name
        dataService.getAccountByName(accountName)
            .then(account => {
                if (!account) {
                    throw new Error(`Account not found: ${accountName}`);
                }
                
                // Update account status
                return dataService.updateAccount(account.id, {
                    status: 'Researched',
                    researchStatus: 'Active Research',
                    updatedAt: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
                });
            })
            .then(() => {
                showNotification('Research saved successfully!', 'success');
            })
            .catch(error => {
                console.error('Error saving research:', error);
                showNotification('Error saving research. Please try again.', 'error');
            });
    });
}

// Add direct event listener to the select element in the DOM
document.addEventListener('DOMContentLoaded', function() {
    // Add direct event listener to account select
    const accountSelectElement = document.getElementById('accountSelect');
    if (accountSelectElement) {
        accountSelectElement.addEventListener('change', function() {
            console.log('Account selection changed - direct event handler');
            const selectedCompany = this.value;
            console.log('Selected company:', selectedCompany);
            
            // Get company data and update the UI
            updateCompanyDetails();
            
            // Force an explicit talk track update with the selected company
            if (selectedCompany && companyData && companyData[selectedCompany]) {
                console.log('Forcing talk track update for company:', selectedCompany);
                updateTalkTrackById(companyData[selectedCompany]);
            }
            
            // Update the hero image with the company logo
            const companyLogos = {
                'nvidia': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nvidia_logo.svg/1200px-Nvidia_logo.svg.png',
                'cisco': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Cisco_logo_blue_2016.svg/1200px-Cisco_logo_blue_2016.svg.png',
                'microsoft': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/1200px-Microsoft_logo.svg.png',
                'google': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/1200px-Google_2015_logo.svg.png',
                'amazon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1200px-Amazon_logo.svg.png'
            };
            
            const heroImg = document.querySelector('.hero-image img');
            if (heroImg) {
                // Store the original image URL if we haven't already
                if (!heroImg.dataset.originalSrc) {
                    heroImg.dataset.originalSrc = DEFAULT_HERO_IMAGE;
                    console.log('Stored original hero image URL:', heroImg.dataset.originalSrc);
                }
                
                if (selectedCompany && companyLogos[selectedCompany]) {
                    console.log('Updating hero image to company logo:', companyLogos[selectedCompany]);
                    heroImg.src = companyLogos[selectedCompany];
                    heroImg.alt = selectedCompany + ' Logo';
                    
                    // Add styling to make the logo look better
                    heroImg.style.objectFit = 'contain';
                    heroImg.style.backgroundColor = '#ffffff';
                    heroImg.style.padding = '20px';
                } else {
                    // Reset to default image if no company is selected
                    console.log('Resetting hero image to default');
                    heroImg.src = heroImg.dataset.originalSrc || DEFAULT_HERO_IMAGE;
                    heroImg.alt = 'Research Team Collaborating';
                    
                    // Reset styling
                    heroImg.style.objectFit = '';
                    heroImg.style.backgroundColor = '';
                    heroImg.style.padding = '';
                }
            }
        });
    }
});

// Keep the original handler for backwards compatibility
if (accountSelect) {
    accountSelect.addEventListener('change', function() {
        console.log('Account selection changed - original handler');
        updateCompanyDetails();
    });
}

// Initialize smooth scrolling for sidebar navigation
function initSmoothScrolling() {
    const insightsNavLinks = document.querySelectorAll('.insights-nav a');
    
    insightsNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            insightsNavLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to the clicked link
            this.classList.add('active');
            
            // Get the target section id from the href attribute
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                // Scroll to the target section with smooth behavior
                window.scrollTo({
                    top: targetSection.offsetTop - 80, // Reduced offset for better visibility
                    behavior: 'smooth'
                });
                
                console.log(`Scrolling to section: ${targetId}`);
                
                // Force the update of active section
                setTimeout(() => {
                    highlightCurrentSection();
                }, 100);
            }
        });
    });
    
    // Also initialize scroll behavior for section detection
    window.addEventListener('scroll', highlightCurrentSection);
    
    // Run once on page load to set the initial active section
    setTimeout(highlightCurrentSection, 200);
    
    console.log("Smooth scrolling initialized");
}

// Highlight the correct navigation link based on scroll position
function highlightCurrentSection() {
    const sections = [
        document.querySelector('#company-insights'),
        document.querySelector('#industry-insights'),
        document.querySelector('#future-insights')
    ];
    
    const navLinks = document.querySelectorAll('.insights-nav a');
    
    if (!sections[0] || !navLinks.length) {
        return; // Exit if sections or navLinks aren't found
    }
    
    // Get current scroll position
    const scrollPosition = window.scrollY + 150; // Add offset to improve detection
    
    // Find the current section based on scroll position
    let currentSectionIndex = 0;
    
    for (let i = sections.length - 1; i >= 0; i--) {
        const section = sections[i];
        if (section && scrollPosition >= section.offsetTop - 100) {
            currentSectionIndex = i;
            break;
        }
    }
    
    // Remove active class from all links
    navLinks.forEach(link => link.classList.remove('active'));
    
    // Add active class to the current section's link
    if (navLinks[currentSectionIndex]) {
        navLinks[currentSectionIndex].classList.add('active');
        console.log('Set active section to:', currentSectionIndex);
    }
}

/**
 * Get the appropriate badge HTML based on the trend type.
 * Dynamically assigns color and icon based on trend type.
 */
function getTrendBadgeHTML(trend) {
    let icon, text, bgClass;
    
    switch(trend) {
        case 'positive':
            icon = 'fa-arrow-up';
            text = 'Positive Trend';
            bgClass = 'bg-success';
            break;
        case 'neutral':
            icon = 'fa-arrow-right';
            text = 'Neutral';
            bgClass = 'bg-secondary';
            break;
        case 'negative':
            icon = 'fa-arrow-down';
            text = 'Negative Trend';
            bgClass = 'bg-danger';
            break;
        case 'key':
            icon = 'fa-check';
            text = 'Key Insight';
            bgClass = 'bg-info';
            break;
        case 'market':
            icon = 'fa-chart-line';
            text = 'Market Shift';
            bgClass = 'bg-primary';
            break;
        case 'growing':
            icon = 'fa-arrow-up';
            text = 'Growing Trend';
            bgClass = 'bg-success';
            break;
        default:
            icon = 'fa-info-circle';
            text = 'Insight';
            bgClass = 'bg-secondary';
    }
    
    return `<span class="badge rounded-pill ${bgClass}"><i class="fas ${icon} me-1"></i> ${text}</span>`;
}

/**
 * Generate research using backend API services (Perplexity and OpenAI).
 * Makes a call to the /api/generate-research endpoint.
 */
function generateResearchFromAPI(accountName, companyValue) {
    // Show loading indicators
    showLoadingIndicators();
    
    console.log(`Generating research for ${accountName} using API...`);
    
    // Make API call to generate research
    fetch('/api/generate-research', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add authentication headers if needed
            // 'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
            accountName: accountName
        })
    })
    .then(response => {
        if (!response.ok) {
            // If response is not ok, attempt to get the error message from the JSON response
            return response.json().then(data => {
                throw new Error(data.message || 'Error generating research');
            });
        }
        return response.json();
    })
    .then(data => {
        if (!data.success) {
            throw new Error(data.message || 'Failed to generate research');
        }
        
        // Update the UI with the research data
        updateUIWithResearchData(data, companyValue);
        
        // Enable the generate button again
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-search me-2"></i>GENERATE RESEARCH';
        }
        
        // Show success notification
        showNotification('Research generated successfully!', 'success');
    })
    .catch(error => {
        console.error('Error generating research:', error);
        
        // Handle error - revert to demo data if needed
        if (DEMO_MODE) {
            console.log('Falling back to demo data');
            updateCompanyDetails();
        }
        
        // Enable the generate button again
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-search me-2"></i>GENERATE RESEARCH';
        }
        
        // Show error notification
        showNotification(`Error: ${error.message}`, 'error');
    });
}

/**
 * Show loading indicators in the insights and talk track sections
 */
function showLoadingIndicators() {
    // Show loading indicators for industry insights
    const industryInsightsSection = document.getElementById('industry-insights-content');
    if (industryInsightsSection) {
        industryInsightsSection.innerHTML = getLoadingHTML('Loading industry insights...');
    }
    
    // Show loading indicators for company insights
    const companyInsightsSection = document.getElementById('company-insights-content');
    if (companyInsightsSection) {
        companyInsightsSection.innerHTML = getLoadingHTML('Loading company insights...');
    }
    
    // Show loading indicators for vision insights
    const visionInsightsSection = document.getElementById('vision-insights-content');
    if (visionInsightsSection) {
        visionInsightsSection.innerHTML = getLoadingHTML('Loading vision insights...');
    }
    
    // Show loading indicators for talk track
    const talkTrackSection = document.getElementById('recommended-talk-track');
    if (talkTrackSection) {
        talkTrackSection.innerHTML = getLoadingHTML('Generating talk track...');
    }
}

/**
 * Get HTML for loading indicator with custom message
 */
function getLoadingHTML(message) {
    return `<div class="text-center py-4">
        <div class="spinner-border" style="color: #40dfaf;" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">${message}</p>
    </div>`;
}

/**
 * Update the UI with the research data from the API
 */
function updateUIWithResearchData(data, companyValue) {
    // Update industry insights
    const industryInsightsSection = document.getElementById('industry-insights-content');
    if (industryInsightsSection) {
        industryInsightsSection.innerHTML = `<div class="markdown-content">${marked.parse(data.industryInsights)}</div>`;
    }
    
    // Update company insights
    const companyInsightsSection = document.getElementById('company-insights-content');
    if (companyInsightsSection) {
        companyInsightsSection.innerHTML = `<div class="markdown-content">${marked.parse(data.companyInsights)}</div>`;
    }
    
    // Update vision insights
    const visionInsightsSection = document.getElementById('vision-insights-content');
    if (visionInsightsSection) {
        visionInsightsSection.innerHTML = `<div class="markdown-content">${marked.parse(data.visionInsights)}</div>`;
    }
    
    // Update talk track
    const talkTrackSection = document.getElementById('recommended-talk-track');
    if (talkTrackSection) {
        talkTrackSection.innerHTML = `<div class="markdown-content">${marked.parse(data.recommendedTalkTrack)}</div>`;
    }
    
    // Update company details and UI from static data (logo, etc)
    if (companyValue && companyData && companyData[companyValue]) {
        updateCompanyDetails();
    }
    
    // Enable the save button
    const saveBtn = document.getElementById('saveBtn');
    if (saveBtn) {
        saveBtn.disabled = false;
    }
}

/**
 * Save the generated research to Airtable
 */
function saveResearchToAirtable(accountName) {
    // Get the current research data from the UI
    const industryInsights = document.getElementById('industry-insights-content').innerHTML;
    const companyInsights = document.getElementById('company-insights-content').innerHTML;
    const visionInsights = document.getElementById('vision-insights-content').innerHTML;
    const recommendedTalkTrack = document.getElementById('recommended-talk-track').innerHTML;
    
    // Get account ID (in a real implementation, we would get this from the account data)
    // For now, we'll use a placeholder
    const accountId = accountName.toLowerCase().replace(/\s+/g, '-');
    
    // Show loading state on save button
    const saveBtn = document.getElementById('saveBtn');
    if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...';
    }
    
    // Make API call to save research
    fetch('/api/save-to-airtable', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add authentication headers if needed
            // 'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
            accountId: accountId,
            accountName: accountName,
            industryInsights: industryInsights,
            companyInsights: companyInsights,
            visionInsights: visionInsights,
            recommendedTalkTrack: recommendedTalkTrack
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Error saving research');
            });
        }
        return response.json();
    })
    .then(data => {
        if (!data.success) {
            throw new Error(data.message || 'Failed to save research');
        }
        
        // Restore save button
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>SAVE TO LIBRARY';
        }
        
        // Show success notification
        showNotification('Research saved to library!', 'success');
    })
    .catch(error => {
        console.error('Error saving research:', error);
        
        // Restore save button
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>SAVE TO LIBRARY';
        }
        
        // Show error notification
        showNotification(`Error: ${error.message}`, 'error');
    });
}

/**
 * Show a notification message to the user
 */
function showNotification(message, type = 'info') {
    // Remove any existing notifications
    const existingNotifications = document.querySelectorAll('.custom-notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `custom-notification alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.maxWidth = '300px';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto dismiss after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add button for generating insights with OpenAI
// Removed the OpenAI button function to maintain original UI

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    
    // Initialize DOM elements first
    initDOMElements();
    
    // Store the original hero image URL for later use
    if (heroImage && !heroImage.dataset.originalSrc) {
        heroImage.dataset.originalSrc = heroImage.src || DEFAULT_HERO_IMAGE;
        console.log('Stored original hero image URL:', heroImage.dataset.originalSrc);
    }
    
    checkUserLogin();
    loadAccounts();
    initSmoothScrolling();
    
    // Handle hash in URL if present
    if (window.location.hash) {
        const hash = window.location.hash;
        const targetSection = document.querySelector(hash);
        const targetLink = document.querySelector(`.insights-nav a[href="${hash}"]`);
        
        if (targetSection && targetLink) {
            // Remove active class from all links
            document.querySelectorAll('.insights-nav a').forEach(l => l.classList.remove('active'));
            
            // Add active class to the target link
            targetLink.classList.add('active');
            
            // Scroll to section after a slight delay to ensure page is loaded
            setTimeout(() => {
                window.scrollTo({
                    top: targetSection.offsetTop - 80,
                    behavior: 'smooth'
                });
            }, 300);
        }
    }
    
    // Set a slight delay to ensure accounts are loaded before selecting NVIDIA
    setTimeout(() => {
        // Set NVIDIA as the default selected company
        if (accountSelect) {
            accountSelect.value = 'nvidia';
            // Trigger the change event to update UI
            updateCompanyDetails();
            // Dispatch a change event to ensure event listeners are triggered
            accountSelect.dispatchEvent(new Event('change'));
        }
    }, 500);
});

// Manually initialize for browsers that might have already fired DOMContentLoaded
if (document.readyState === 'loading') {
    console.log("Document still loading, waiting for DOMContentLoaded");
} else {
    console.log("Document already loaded, initializing immediately");
    checkUserLogin();
    loadAccounts();
    initSmoothScrolling();
    
    // Set a slight delay to ensure accounts are loaded before selecting NVIDIA
    setTimeout(() => {
        // Set NVIDIA as the default selected company
        if (accountSelect) {
            accountSelect.value = 'nvidia';
            // Trigger the change event to update UI
            updateCompanyDetails();
        }
    }, 500);
}

/**
 * Updates talk track content by directly targeting elements by their IDs
 * This is an alternative approach that should be more reliable
 */
function updateTalkTrackById(company) {
    console.log('Updating talk track by ID for company:', company.name);
    
    // Update company name in the talk track header badge
    const companyBadge = document.querySelector('.talk-track-section .card-header .badge');
    if (companyBadge) {
        console.log('Updating company badge to:', company.name);
        companyBadge.textContent = company.name;
    } else {
        console.error('Company badge element not found');
    }
    
    // Get direct references to the talk track paragraphs by their IDs
    const openingParagraph = document.getElementById('talk-track-opening');
    const valueParagraph = document.getElementById('talk-track-value');
    const engagementParagraph = document.getElementById('talk-track-engagement');
    
    console.log('Opening paragraph found:', !!openingParagraph);
    console.log('Value paragraph found:', !!valueParagraph);
    console.log('Engagement paragraph found:', !!engagementParagraph);
    
    if (company.talkTrack) {
        // Split the talk track into sections
        const talkTrackParts = company.talkTrack.split('\n\n');
        console.log('Talk track parts count:', talkTrackParts.length);
        
        // Update each paragraph with the corresponding talk track section
        if (openingParagraph && talkTrackParts.length >= 1) {
            openingParagraph.textContent = talkTrackParts[0];
            console.log('Updated opening paragraph');
        }
        
        if (valueParagraph && talkTrackParts.length >= 2) {
            valueParagraph.textContent = talkTrackParts[1];
            console.log('Updated value proposition paragraph');
        }
        
        if (engagementParagraph && talkTrackParts.length >= 3) {
            engagementParagraph.textContent = talkTrackParts[2];
            console.log('Updated engagement paragraph');
        }
        
        // Update generation date
        const dateElement = document.querySelector('.talk-track-box .text-muted.small');
        if (dateElement) {
            const today = new Date();
            const formattedDate = today.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            dateElement.textContent = `Generated on ${formattedDate} \u2022 Based on latest company research`;
        }
        
        console.log('Talk track updated successfully for:', company.name);
    } else {
        console.error('Talk track data is missing for company:', company.name);
    }
}

/**
 * Data Service for SDR World
 * 
 * This service handles all data operations for the frontend,
 * providing a consistent interface to access account and research data
 * whether we're using a real Supabase backend or mock data.
 */

class DataService {
    constructor() {
        // Singleton pattern
        if (DataService.instance) {
            return DataService.instance;
        }
        DataService.instance = this;
        
        // Initialize with mock data for demo purposes
        this.initializeMockData();
        
        // Cache frequently accessed data
        this.accountsCache = null;
        this.currentResearchCache = null;
    }
    
    /**
     * Initialize mock data for demo purposes
     * In a production environment, this would be replaced with Supabase API calls
     */
    initializeMockData() {
        this.mockAccounts = [
            {
                id: "1",
                name: "NVIDIA",
                logoUrl: "https://logo.clearbit.com/nvidia.com",
                industry: "Technology",
                description: "NVIDIA is a technology company known for designing graphics processing units (GPUs) for gaming and professional markets, as well as system on a chip units for mobile computing and automotive markets.",
                headquarters: "Santa Clara, CA",
                status: "Researched",
                updatedAt: "Mar 9, 2025",
                researchStatus: "Active Research",
                employees: "26,000+",
                marketCap: "$2.3 Trillion",
                founded: "1993"
            },
            {
                id: "2",
                name: "Google",
                logoUrl: "https://logo.clearbit.com/google.com",
                industry: "Technology",
                description: "Google LLC is an American multinational technology company that specializes in Internet-related services and products.",
                headquarters: "Mountain View, CA",
                status: "Researched",
                updatedAt: "Mar 4, 2025"
            },
            {
                id: "3",
                name: "Microsoft",
                logoUrl: "https://logo.clearbit.com/microsoft.com",
                industry: "Technology",
                description: "Microsoft Corporation is an American multinational technology company that develops, licenses, and supports software, services, devices, and solutions.",
                headquarters: "Redmond, WA",
                status: "Researched",
                updatedAt: "Feb 28, 2025"
            },
            {
                id: "4",
                name: "Amazon",
                logoUrl: "https://logo.clearbit.com/amazon.com",
                industry: "Retail",
                description: "Amazon.com, Inc. is an American multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence.",
                headquarters: "Seattle, WA",
                status: "Pending",
                updatedAt: "Mar 1, 2025"
            },
            {
                id: "5",
                name: "JP Morgan Chase",
                logoUrl: "https://logo.clearbit.com/jpmorganchase.com",
                industry: "Finance",
                description: "JPMorgan Chase & Co. is an American multinational investment bank and financial services holding company.",
                headquarters: "New York, NY",
                status: "Pending",
                updatedAt: "Mar 2, 2025"
            },
            {
                id: "6",
                name: "Cisco Systems",
                logoUrl: "https://logo.clearbit.com/cisco.com",
                industry: "Technology",
                description: "Cisco Systems, Inc. is an American multinational technology conglomerate that develops, manufactures, and sells networking hardware, software, telecommunications equipment and other technology services and products.",
                headquarters: "San Jose, CA",
                status: "Researched",
                updatedAt: "Mar 10, 2025"
            }
        ];
        
        this.mockResearch = [
            {
                id: "1",
                accountId: "1",
                companyName: "NVIDIA Corporation",
                overview: "NVIDIA is a global technology company and inventor of the GPU...",
                insights: [
                    "Recently acquired ARM Holdings for $40 billion to strengthen its AI capabilities",
                    "Growing demand in data center and AI sectors",
                    "Facing increased competition from AMD and Intel in the GPU market"
                ],
                talkTracks: [
                    "Your AI compute needs are growing rapidly - NVIDIA's latest data center GPUs could accelerate your ML initiatives by 40%",
                    "Your competitors are implementing AI-powered analytics - NVIDIA's enterprise solutions can help you maintain competitive edge"
                ],
                createdAt: "Mar 9, 2025"
            }
        ];
    }
    
    /**
     * Get all accounts
     * @returns {Promise<Array>} List of accounts
     */
    async getAccounts() {
        // If we have cached accounts, return them
        if (this.accountsCache) {
            return this.accountsCache;
        }
        
        try {
            // In production, this would be a Supabase API call
            // For demo, we'll use mock data with a simulated delay
            await this._simulateNetworkDelay(300);
            this.accountsCache = this.mockAccounts;
            return this.accountsCache;
        } catch (error) {
            console.error('Error fetching accounts:', error);
            return [];
        }
    }
    
    /**
     * Get a specific account by ID
     * @param {string} accountId - The account ID
     * @returns {Promise<Object>} Account object
     */
    async getAccount(accountId) {
        try {
            await this._simulateNetworkDelay(200);
            const account = this.mockAccounts.find(a => a.id === accountId);
            return account || null;
        } catch (error) {
            console.error(`Error fetching account ${accountId}:`, error);
            return null;
        }
    }
    
    /**
     * Get a specific account by name
     * @param {string} name - The account name
     * @returns {Promise<Object>} Account object
     */
    async getAccountByName(name) {
        try {
            await this._simulateNetworkDelay(200);
            const account = this.mockAccounts.find(a => a.name === name);
            return account || null;
        } catch (error) {
            console.error(`Error fetching account by name ${name}:`, error);
            return null;
        }
    }
    
    /**
     * Create a new account
     * @param {Object} accountData - The account data
     * @returns {Promise<Object>} Created account
     */
    async createAccount(accountData) {
        try {
            await this._simulateNetworkDelay(500);
            const newId = (Math.max(...this.mockAccounts.map(a => parseInt(a.id))) + 1).toString();
            const newAccount = {
                id: newId,
                ...accountData,
                updatedAt: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
            };
            
            this.mockAccounts.push(newAccount);
            this.accountsCache = null; // Invalidate cache
            return newAccount;
        } catch (error) {
            console.error('Error creating account:', error);
            return null;
        }
    }
    
    /**
     * Update an existing account
     * @param {string} accountId - The account ID
     * @param {Object} accountData - The updated account data
     * @returns {Promise<Object>} Updated account
     */
    async updateAccount(accountId, accountData) {
        try {
            await this._simulateNetworkDelay(500);
            const index = this.mockAccounts.findIndex(a => a.id === accountId);
            
            if (index !== -1) {
                const updatedAccount = {
                    ...this.mockAccounts[index],
                    ...accountData,
                    updatedAt: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
                };
                
                this.mockAccounts[index] = updatedAccount;
                this.accountsCache = null; // Invalidate cache
                return updatedAccount;
            }
            
            return null;
        } catch (error) {
            console.error(`Error updating account ${accountId}:`, error);
            return null;
        }
    }
    
    /**
     * Get research for a specific account
     * @param {string} accountId - The account ID
     * @returns {Promise<Object>} Research object
     */
    async getResearch(accountId) {
        try {
            await this._simulateNetworkDelay(300);
            const research = this.mockResearch.find(r => r.accountId === accountId);
            return research || null;
        } catch (error) {
            console.error(`Error fetching research for account ${accountId}:`, error);
            return null;
        }
    }
    
    /**
     * Create new research
     * @param {Object} researchData - The research data
     * @returns {Promise<Object>} Created research
     */
    async createResearch(researchData) {
        try {
            await this._simulateNetworkDelay(700);
            const newId = (this.mockResearch.length + 1).toString();
            const newResearch = {
                id: newId,
                ...researchData,
                createdAt: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
            };
            
            this.mockResearch.push(newResearch);
            
            // Update the account status to reflect that research was conducted
            const accountId = researchData.accountId;
            const accountIndex = this.mockAccounts.findIndex(a => a.id === accountId);
            
            if (accountIndex !== -1) {
                this.mockAccounts[accountIndex].status = "Researched";
                this.mockAccounts[accountIndex].researchStatus = "Active Research";
                this.mockAccounts[accountIndex].updatedAt = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                this.accountsCache = null; // Invalidate cache
            }
            
            return newResearch;
        } catch (error) {
            console.error('Error creating research:', error);
            return null;
        }
    }
    
    /**
     * Update existing research
     * @param {string} researchId - The research ID
     * @param {Object} researchData - The updated research data
     * @returns {Promise<Object>} Updated research
     */
    async updateResearch(researchId, researchData) {
        try {
            await this._simulateNetworkDelay(500);
            const index = this.mockResearch.findIndex(r => r.id === researchId);
            
            if (index !== -1) {
                const updatedResearch = {
                    ...this.mockResearch[index],
                    ...researchData,
                    updatedAt: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
                };
                
                this.mockResearch[index] = updatedResearch;
                return updatedResearch;
            }
            
            return null;
        } catch (error) {
            console.error(`Error updating research ${researchId}:`, error);
            return null;
        }
    }
    
    /**
     * Set current research company (used for research form)
     * @param {string} companyName - Name of the company
     */
    setCurrentResearchCompany(companyName) {
        localStorage.setItem('currentResearchCompany', companyName);
    }
    
    /**
     * Get current research company name
     * @returns {string} Current company name
     */
    getCurrentResearchCompany() {
        return localStorage.getItem('currentResearchCompany') || null;
    }
    
    /**
     * Simulate network delay for a more realistic experience
     * @param {number} ms - Milliseconds to delay
     * @returns {Promise} Promise that resolves after the delay
     * @private
     */
    _simulateNetworkDelay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    /**
     * Reset all data to initial state (for testing)
     */
    resetAllData() {
        this.initializeMockData();
        this.accountsCache = null;
        this.currentResearchCache = null;
        localStorage.removeItem('currentResearchCompany');
    }
}

// Create a singleton instance
const dataService = new DataService();

// Make it available globally
window.dataService = dataService;

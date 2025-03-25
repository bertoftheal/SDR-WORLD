-- Supabase Schema for SDR World Application
-- This script creates the necessary tables for the SDR World application

-- Accounts table - Stores company information
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    industry TEXT,
    location TEXT,
    headquarters TEXT,
    employees TEXT,
    employee_count INTEGER,
    revenue TEXT,
    market_cap TEXT,
    website TEXT,
    logo_url TEXT,
    description TEXT,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Research table - Stores generated research for accounts
CREATE TABLE research (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    account_name TEXT NOT NULL,
    industry_insights TEXT,
    company_insights TEXT,
    vision_insights TEXT,
    talk_track TEXT,
    created_by UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users table - Stores user information
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX idx_accounts_name ON accounts(name);
CREATE INDEX idx_research_account_id ON research(account_id);
CREATE INDEX idx_research_account_name ON research(account_name);

-- Sample data for testing
INSERT INTO accounts (name, industry, headquarters, employees, logo_url, description, market_cap)
VALUES 
('NVIDIA', 'Technology', 'Santa Clara, CA', '26,000+', 'https://logo.clearbit.com/nvidia.com', 
 'NVIDIA is a technology company known for designing graphics processing units (GPUs) for gaming and professional markets, as well as system on a chip units for mobile computing and automotive markets.',
 '$2.3 Trillion'),
 
('Microsoft', 'Technology', 'Redmond, WA', '181,000+', 'https://logo.clearbit.com/microsoft.com',
 'Microsoft Corporation is an American multinational technology company that develops, manufactures, licenses, supports, and sells computer software, consumer electronics, personal computers, and related services.',
 '$2.8 Trillion'),
 
('Cisco', 'Technology', 'San Jose, CA', '83,300+', 'https://logo.clearbit.com/cisco.com',
 'Cisco Systems, Inc. is an American multinational technology conglomerate that develops, manufactures, and sells networking hardware, software, telecommunications equipment and other high-technology services and products.',
 '$212 Billion');

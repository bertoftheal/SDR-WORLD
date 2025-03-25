-- Add airtable_id column to accounts table
ALTER TABLE accounts 
ADD COLUMN IF NOT EXISTS airtable_id TEXT;

-- Add airtable_id column to research table (if needed)
ALTER TABLE research
ADD COLUMN IF NOT EXISTS airtable_record_id TEXT;

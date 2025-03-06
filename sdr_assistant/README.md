# SDR Account Research Assistant

A web application for Sales Development Representatives (SDRs) to generate AI-powered research insights for their accounts. The app integrates with Airtable for account data and uses Perplexity API for generating insights.

## Features

- Select accounts from Airtable
- Generate AI research insights using Perplexity API
- Display structured insights on industry trends, company background, and forward-thinking vision
- Save insights back to Airtable

## Setup Instructions

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following variables:
   ```
   AIRTABLE_API_KEY=your_airtable_api_key_here
   AIRTABLE_BASE_ID=your_airtable_base_id_here
   AIRTABLE_TABLE_NAME=your_airtable_table_name_here
   PERPLEXITY_API_KEY=your_perplexity_api_key_here
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`

## Airtable Configuration

Your Airtable table should have the following fields:
- `Name`: The name of the account
- `AI_Insights`: A text field where the generated insights will be saved

## API Information

- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)
- [Perplexity API Documentation](https://docs.perplexity.ai/)

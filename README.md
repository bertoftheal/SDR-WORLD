# SDR Assistant

A modular web application designed to help Sales Development Representatives (SDRs) generate research and talk tracks for potential client accounts.

## Project Structure

The SDR Assistant application follows a modular architecture based on SOLID principles:

```
sdr_assistant/
│
├── api/                  # API routes and endpoints
│   ├── account_routes.py # Account-related endpoints
│   ├── auth_routes.py    # Authentication endpoints
│   ├── research_routes.py# Research generation endpoints
│   └── routes.py         # Core routing setup
│
├── config/               # Configuration management
│   └── settings.py       # Application settings with environment variables
│
├── core/                 # Business logic
│   ├── accounts.py       # Account management operations
│   ├── auth.py           # Authentication logic and JWT handling
│   └── research.py       # Research generation logic
│
├── interfaces/           # Service interfaces defining contracts
│   └── service_interface.py # Interface definitions for services
│
├── models/               # Data models
│   ├── account.py        # Account data model
│   └── research.py       # Research data model
│
├── services/             # External service integrations
│   ├── airtable_service.py  # Airtable API integration
│   ├── openai_service.py    # OpenAI API integration for talk tracks
│   └── perplexity_service.py# Perplexity API integration for research
│
├── static/               # Frontend static assets
│   ├── css/              # CSS styling
│   ├── js/               # JavaScript files
│   └── index.html        # Main HTML page
│
├── tests/                # Test suite
│   ├── core/             # Tests for core functionality
│   └── services/         # Tests for service integrations
│
├── utils/                # Utility functions and helpers
│   ├── exceptions.py     # Custom exception classes
│   ├── helpers.py        # General utility functions
│   └── logger.py         # Logging configuration
│
├── app.py                # Application entry point
└── requirements.txt      # Python dependencies
```

## Features

- **Account Management**: View and manage client accounts
- **Research Generation**: Generate AI-powered research on companies
- **Talk Track Creation**: Create personalized sales talk tracks
- **Authentication**: Secure API endpoints with JWT authentication

## API Integrations

- **Airtable**: For storing account and research data
- **Perplexity AI**: For generating research insights
- **OpenAI**: For generating personalized talk tracks

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\\Scripts\\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with the following variables:
   ```
   AIRTABLE_API_KEY=your_airtable_key
   AIRTABLE_BASE_ID=your_base_id
   OPENAI_API_KEY=your_openai_key
   PERPLEXITY_API_KEY=your_perplexity_key
   JWT_SECRET_KEY=your_jwt_secret
   ```
6. Run the application: `python -m sdr_assistant.app`

## Testing

Run tests with pytest:

```
python -m pytest sdr_assistant/tests
```

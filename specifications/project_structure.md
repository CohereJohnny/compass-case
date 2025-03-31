# Project Structure

This document outlines the project structure for the Cohere Compass SDK Web Interface. The structure is designed to be modular, maintainable, and follow Flask best practices.

## Directory Structure

```
compass-case/                      # Root directory
├── .env                           # Environment variables
├── .gitignore                     # Git ignore file
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup script
├── README.md                      # Project documentation
├── docs/                          # Documentation
│   ├── build/                     # Built documentation
│   └── source/                    # Documentation source files
├── specifications/                # Project specifications
│   ├── prd.md                     # Product Requirements Document
│   ├── api_specification.md       # API Specification
│   ├── data_model.md              # Data Model
│   ├── project_structure.md       # Project Structure (this file)
│   ├── architecture.md            # Architecture
│   └── ux_flow.md                 # UX Flow
├── migration/                     # Migration scripts
└── web_interface/                 # Web interface application
    ├── __init__.py                # Package initialization
    ├── app.py                     # Main Flask application
    ├── settings.pkl               # Stored settings
    ├── static/                    # Static assets
    │   ├── css/                   # CSS stylesheets
    │   │   └── style.css          # Main stylesheet
    │   └── js/                    # JavaScript files
    │       └── main.js            # Main JavaScript file
    └── templates/                 # HTML templates
        ├── index.html             # Home page
        ├── indexes.html           # Indexes list
        ├── create_index.html      # Create index form
        ├── view_index.html        # View index details
        ├── upload.html            # Upload document form
        ├── search.html            # Search interface
        ├── chat.html              # Chat with specific index
        ├── chat_index.html        # Chat with any index selection
        ├── api_explorer.html      # API explorer
        ├── documentation.html     # Documentation
        └── settings.html          # Settings page
```

## Key Files and Their Purposes

### Configuration Files

- **`.env`**: Contains environment variables including API keys and service URLs.
- **`requirements.txt`**: Lists all Python dependencies for the project.
- **`setup.py`**: Defines package metadata and dependencies for installation.

### Application Files

- **`web_interface/app.py`**: The main Flask application containing routes, views, and business logic.
- **`web_interface/__init__.py`**: Package initialization.
- **`web_interface/settings.pkl`**: Persists user settings like API keys and model preferences.

### Static Assets

- **`web_interface/static/css/style.css`**: Main CSS stylesheet for the application.
- **`web_interface/static/js/main.js`**: Contains client-side JavaScript for dynamic behavior.

### Templates

- **`web_interface/templates/index.html`**: Home page template.
- **`web_interface/templates/indexes.html`**: Lists all available indexes.
- **`web_interface/templates/create_index.html`**: Form for creating a new index.
- **`web_interface/templates/view_index.html`**: Shows details for a specific index.
- **`web_interface/templates/upload.html`**: Form for uploading documents to an index.
- **`web_interface/templates/search.html`**: Interface for searching an index.
- **`web_interface/templates/chat.html`**: Chat interface for a specific index.
- **`web_interface/templates/chat_index.html`**: Interface for selecting an index to chat with.
- **`web_interface/templates/api_explorer.html`**: Interface for testing SDK API methods.
- **`web_interface/templates/documentation.html`**: Shows documentation for the application.
- **`web_interface/templates/settings.html`**: Interface for configuring application settings.

## Module Organization

### Flask Application (`app.py`)

The Flask application is organized into the following sections:

1. **Imports and Setup**: Importing required modules and setting up the Flask app.
2. **Helper Functions**: Functions for common tasks like client initialization and settings management.
3. **Route Handlers**: Functions decorated with `@app.route` that respond to HTTP requests.
4. **API Endpoint Handlers**: Functions that provide JSON responses for AJAX requests.
5. **Utility Functions**: Helper functions for processing data, handling errors, etc.

### Template Structure

Each template follows a common structure:

1. **Header**: Navigation and page title
2. **Main Content**: Page-specific content
3. **Footer**: Copyright information
4. **Scripts**: JavaScript for page-specific functionality

## Naming Conventions

- **Routes**: Lowercase with hyphens (kebab-case), e.g., `/api-explorer`
- **Python Functions**: Snake case, e.g., `create_index()`
- **JavaScript Functions**: Camel case, e.g., `updateSearchResults()`
- **CSS Classes**: Kebab case, e.g., `.search-results`
- **Template Files**: Snake case, e.g., `create_index.html`

## Dependencies

### Python Dependencies

- **Flask**: Web framework
- **Cohere**: Cohere API client
- **Cohere Compass**: Compass SDK
- **python-dotenv**: For loading environment variables
- **Requests**: For HTTP requests
- **Werkzeug**: For utilities (file uploads, etc.)

### Frontend Dependencies

- **Bootstrap**: CSS framework for responsive design
- **Bootstrap Icons**: Icon set
- **JavaScript (vanilla)**: For client-side interactivity

## Environment Configuration

The application relies on the following environment variables:

- `COMPASS_API_URL`: URL for the Compass API
- `COMPASS_API_BEARER_TOKEN`: Bearer token for Compass API authentication
- `COMPASS_PARSER_URL`: URL for the Compass Parser API
- `COMPASS_PARSER_BEARER_TOKEN`: Bearer token for Compass Parser API authentication
- `COHERE_API_KEY`: API key for Cohere services
- `FLASK_SECRET_KEY`: Secret key for Flask session encryption

These can also be configured through the settings interface in the application, which stores them in `settings.pkl`. 
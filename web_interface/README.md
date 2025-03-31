# Cohere Compass SDK Web Interface

A web-based interface for interacting with the Cohere Compass SDK. This application provides a user-friendly way to explore and test the SDK's functionality.

## Features

- **Index Management**: 
  - Create new indexes with customizable settings
  - View all existing indexes and their details
  - Monitor document counts and index status

- **Document Management**: 
  - Upload documents to indexes with support for various file formats
  - Configure advanced parsing options for PDF documents
  - Track uploaded documents and their metadata

- **Search Interface**: 
  - Search indexes with customizable parameters
  - View search results with relevance scores
  - Inspect document content directly from search results

- **Chat Interface**:
  - Chat with your documents using Cohere's powerful LLMs
  - Single-index chat for focused conversations with specific indexes
  - Multi-index chat with index selection for broader queries
  - View relevant search results used as context for responses
  - Interactive document preview for full context inspection

- **API Explorer**: 
  - Interactive testing of SDK methods with dynamic form generation
  - Live documentation for available methods and parameters
  - Example code generation for use in your own applications
  - JSON response formatting and visualization

- **Settings Management**:
  - Configure API tokens for Compass and Cohere
  - Select from available chat models with details on capabilities
  - Secure storage of sensitive configuration information
  - Password visibility toggles for easier input

- **Documentation**: 
  - Access to comprehensive SDK documentation
  - Code samples for common tasks
  - Interactive guides for using the SDK

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cohere-ai/compass-case.git
   cd compass-case
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root with the following variables:
   ```
   COMPASS_API_URL=your-compass-api-url
   COMPASS_API_BEARER_TOKEN=your-api-token
   COMPASS_PARSER_URL=your-compass-parser-url
   COMPASS_PARSER_BEARER_TOKEN=your-parser-token
   COHERE_API_KEY=your-cohere-api-key
   FLASK_SECRET_KEY=your-flask-secret-key
   ```

## Usage

1. Start the web interface:
   ```bash
   python -m web_interface.app
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

3. The interface provides several key sections:
   - **Home**: Overview of the application features
   - **Indexes**: List of all your Compass indexes
   - **Chat**: Interactive chat interface for your documents
   - **API Explorer**: Interactive SDK method testing
   - **Documentation**: Comprehensive SDK documentation
   - **Settings**: Application configuration

## Chat Functionality

The chat interface allows you to interact with your documents using natural language:

1. **Single-Index Chat**:
   - Access by clicking the "Chat" button next to any index
   - Ask questions about documents in that specific index
   - View relevant document chunks used as context

2. **Multi-Index Chat**:
   - Access through the main "Chat" navigation link
   - Select any index from a dropdown menu
   - Chat with documents across different indexes

3. **Under the Hood**:
   - Uses Compass search to find relevant document chunks
   - Sends these chunks as context to Cohere's Chat API
   - Displays both the AI response and the source documents
   - Uses the model selected in Settings (defaults to command-a-03-2025)

4. **Document Inspection**:
   - Click on any search result to view the full document content
   - See document IDs and relevance scores
   - Preview document content in a modal dialog

## API Explorer

The API Explorer allows you to:

1. Select a client type (CompassClient or CompassParserClient)
2. Select a method to call
3. Fill in the required parameters
4. Execute the method and view the response
5. See example code for using the method in your own applications

## Development

### Project Structure

```
web_interface/
├── static/             # Static files
│   ├── css/            # Stylesheet files
│   │   └── style.css   # Main stylesheet
│   └── js/             # JavaScript files
│       └── main.js     # Main JavaScript file
├── templates/          # HTML templates
│   ├── index.html      # Home page
│   ├── indexes.html    # Indexes list
│   ├── view_index.html # Index details
│   ├── create_index.html # Create index form
│   ├── upload.html     # Document upload form
│   ├── search.html     # Search interface
│   ├── chat.html       # Single-index chat interface
│   ├── chat_index.html # Multi-index chat interface
│   ├── api_explorer.html # API testing interface
│   ├── documentation.html # SDK documentation
│   └── settings.html   # Application settings
├── app.py              # Flask application
└── settings.pkl        # Stored settings file
```

### Adding New API Methods

To add new methods to the API Explorer:

1. Open `templates/api_explorer.html`
2. Find the `apiMethods` object
3. Add a new method definition with its parameters and documentation

Example:
```javascript
apiMethods: {
    compass: {
        // Add your new method here
        your_new_method: {
            description: "Description of what the method does.",
            parameters: {
                param1: { type: "string", required: true, description: "Description of param1." },
                param2: { type: "integer", required: false, default: 10, description: "Description of param2." }
            }
        }
    }
}
```

### Adding New Features

The application is built with Flask and uses a combination of server-side rendering and client-side JavaScript:

1. **Server-side (Flask)**:
   - Routes are defined in `app.py`
   - Data processing logic using the Cohere Compass SDK
   - Template rendering using Jinja2

2. **Client-side**:
   - Bootstrap 5 for UI components and responsive design
   - JavaScript for interactive elements
   - Prism.js for code highlighting in API Explorer

## Dependencies

- **Flask**: Web framework for Python
- **Cohere Python SDK**: For chat API integration
- **dotenv**: For loading environment variables
- **Bootstrap 5**: Front-end framework
- **Cohere Compass SDK**: Core SDK for interacting with Compass API

## License

[MIT License](../LICENSE) 
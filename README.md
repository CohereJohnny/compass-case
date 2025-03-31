# Cohere Compass SDK Documentation and Web Interface

This project provides comprehensive documentation and a web interface for the Cohere Compass SDK, making it easier to understand and work with the SDK.

## Project Components

The project consists of two main components:

1. **SDK Documentation**: Comprehensive documentation for the Cohere Compass SDK, including API reference, guides, and examples.
2. **Web Interface**: A Flask-based web application that provides an interactive interface for working with the SDK.

## SDK Documentation

The documentation is built using Sphinx and includes:

- **API Reference**: Complete reference for all classes, methods, and properties
- **Guides**: Step-by-step guides for common tasks
- **Examples**: Practical code examples demonstrating SDK usage

### Building the Documentation

To build the documentation:

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the HTML documentation:
   ```bash
   cd docs
   make html
   ```

3. Open the documentation in your browser:
   ```bash
   open docs/build/html/index.html
   ```

## Web Interface

The web interface provides a user-friendly way to interact with the Cohere Compass SDK, including:

- **Index Management**: View, create, and manage indexes
- **Document Management**: Upload and search documents through a user-friendly interface
- **Search Interface**: Search indexes with customizable parameters and view results
- **API Explorer**: Interactive testing of SDK methods with automatic form generation
- **Chat Integration**: Chat with your documents using Cohere's powerful LLMs
- **Settings Management**: Configure API keys and select chat models

### Running the Web Interface

To run the web interface:

1. Make sure you have the required environment variables set in a `.env` file in the project root:
   ```
   COMPASS_API_URL=your-compass-api-url
   COMPASS_API_BEARER_TOKEN=your-api-token
   COMPASS_PARSER_URL=your-compass-parser-url
   COMPASS_PARSER_BEARER_TOKEN=your-parser-token
   COHERE_API_KEY=your-cohere-api-key
   FLASK_SECRET_KEY=your-flask-secret-key
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the web interface:
   ```bash
   python -m web_interface.app
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Project Structure

```
compass-case/
├── cohere_compass/     # The SDK package
├── docs/               # Documentation
│   ├── build/          # Generated documentation
│   ├── source/         # Source files for documentation
│   └── Makefile        # For building documentation
├── web_interface/      # Web interface application
│   ├── static/         # Static files (CSS, JS)
│   │   ├── css/        # Stylesheet files
│   │   └── js/         # JavaScript files
│   ├── templates/      # HTML templates
│   │   ├── index.html  # Home page
│   │   ├── indexes.html # Indexes list
│   │   ├── chat.html   # Chat interface
│   │   ├── settings.html # Settings page
│   │   └── ...         # Other templates
│   ├── app.py          # Flask application
│   └── settings.pkl    # Stored settings
├── .env                # Environment variables
└── requirements.txt    # Project dependencies
```

## Integration with Cursor IDE

The documentation is designed to work well with Cursor's "vibe coding" features:

1. **Well-formatted Docstrings**: All classes and methods have comprehensive docstrings
2. **Type Annotations**: Complete type hints for better autocompletion
3. **Module Structure**: Clear organization of modules for easy navigation

## Key Features

### Chat Interface
The web interface includes a powerful chat capability that allows users to:
- Chat with specific indexes using Cohere's LLM models
- See search results used as context for generating responses
- Configure different chat models through the settings page
- Use both single-index and multi-index chat interfaces

### Document Context Display
When chatting with documents, the interface shows:
- Relevant document chunks used as context
- Document metadata including IDs and relevance scores
- Full text viewing in a modal dialog

### Settings Management
The application includes a settings page that allows users to:
- Store Compass API Bearer Token
- Configure Cohere API Key
- Select from available chat models
- View model capabilities and context lengths

## Contributing

Contributions to improve the documentation or web interface are welcome. Please follow these steps:

1. Fork the repository
2. Create a branch for your changes
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
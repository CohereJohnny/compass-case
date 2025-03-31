"""
Cohere Compass SDK Web Interface

This module provides a web interface for interacting with the Cohere Compass SDK.
"""

import os
import sys
import json
import uuid
import base64
import pickle

# Add the parent directory to Python path so we can find the cohere_compass package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import dotenv
import cohere

from cohere_compass.clients import CompassClient, CompassParserClient
from cohere_compass.models import ParserConfig, MetadataConfig, CompassDocument, PDFParsingStrategy
from cohere_compass.models.config import IndexConfig

# Load environment variables
dotenv.load_dotenv()

app = Flask(__name__)
app.config['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'compass-secret-key')

# Settings file path
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.pkl')

# Configure clients
def get_compass_client():
    """Create and return a CompassClient instance."""
    api_url = os.getenv("COMPASS_API_URL")
    if not api_url:
        raise ValueError("COMPASS_API_URL environment variable is not set")
    
    # Get bearer token from settings if available
    settings = load_settings()
    bearer_token = settings.get('compass_api_bearer_token') or os.getenv("COMPASS_API_BEARER_TOKEN")
    
    return CompassClient(index_url=api_url, bearer_token=bearer_token)

def get_parser_client():
    """Create and return a CompassParserClient instance."""
    parser_url = os.getenv("COMPASS_PARSER_URL")
    if not parser_url:
        raise ValueError("COMPASS_PARSER_URL environment variable is not set")
    
    bearer_token = os.getenv("COMPASS_PARSER_BEARER_TOKEN")
    return CompassParserClient(
        parser_url=parser_url, 
        bearer_token=bearer_token,
        parser_config=ParserConfig()
    )

def get_cohere_client():
    """Create and return a Cohere client instance."""
    settings = load_settings()
    api_key = settings.get('cohere_api_key') or os.getenv("COHERE_API_KEY")
    
    if not api_key:
        raise ValueError("Cohere API key not found in settings or environment variables")
    
    return cohere.Client(api_key=api_key)

# Settings functions
def load_settings():
    """Load settings from file."""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'rb') as f:
                return pickle.load(f)
    except Exception as e:
        print(f"Error loading settings: {e}")
    
    return {}

def save_settings(settings):
    """Save settings to file."""
    try:
        with open(SETTINGS_FILE, 'wb') as f:
            pickle.dump(settings, f)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False

# Routes
@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/indexes')
def list_indexes():
    """List all indexes."""
    try:
        client = get_compass_client()
        response = client.list_indexes()
        
        if response.error:
            return render_template('indexes.html', error=response.error)
        
        indexes = response.result.get("indexes", [])
        return render_template('indexes.html', indexes=indexes)
    except Exception as e:
        return render_template('indexes.html', error=str(e))

@app.route('/indexes/create', methods=['GET', 'POST'])
def create_index():
    """Create a new index."""
    if request.method == 'POST':
        try:
            index_name = request.form.get('index_name')
            max_chunks_per_doc = int(request.form.get('max_chunks_per_doc', 100))
            
            config = IndexConfig(
                max_chunks_per_doc=max_chunks_per_doc
            )
            
            client = get_compass_client()
            response = client.create_index(
                index_name=index_name,
                index_config=config
            )
            
            if response.error:
                return render_template('create_index.html', error=response.error)
            
            return redirect(url_for('list_indexes'))
        except Exception as e:
            return render_template('create_index.html', error=str(e))
    
    return render_template('create_index.html')

@app.route('/indexes/<index_name>')
def view_index(index_name):
    """View details of a specific index."""
    try:
        client = get_compass_client()
        
        # Get index details (not directly supported by the API, so we list all and filter)
        list_response = client.list_indexes()
        if list_response.error:
            return render_template('view_index.html', error=list_response.error)
        
        indexes = list_response.result.get("indexes", [])
        index = next((idx for idx in indexes if idx['name'] == index_name), None)
        
        if not index:
            return render_template('view_index.html', error=f"Index '{index_name}' not found")
        
        # Initialize documents list
        documents = []
        
        # Get documents if the index has any (only if count > 0)
        if index.get('count', 0) > 0:
            try:
                # Method 1: Try common words first - this might work for most text documents
                common_queries = ["the", "a", "in", "to", "and", "of", "is", "for", "on", "with"]
                
                for query in common_queries:
                    search_response = client.search_documents(
                        index_name=index_name, 
                        query=query, 
                        top_k=100
                    )
                    
                    # Extract documents from hits array
                    if hasattr(search_response, 'hits') and search_response.hits:
                        documents = search_response.hits
                        print(f"Found {len(documents)} documents from hits attribute")
                        break
                    elif not search_response.error and search_response.result:
                        if hasattr(search_response.result, 'hits'):
                            documents = search_response.result.hits
                            print(f"Found {len(documents)} documents from result.hits")
                            break
                        else:
                            documents = search_response.result.get("documents", [])
                            if documents:
                                print(f"Found {len(documents)} documents from result.documents")
                                break
                
                # Method 2: If no documents found, try a broader approach
                if not documents:
                    # Try a query using a space character - some APIs treat this as a wildcard
                    search_response = client.search_documents(
                        index_name=index_name, 
                        query=" ", 
                        top_k=100
                    )
                    
                    if hasattr(search_response, 'hits') and search_response.hits:
                        documents = search_response.hits
                    elif not search_response.error and search_response.result:
                        if hasattr(search_response.result, 'hits'):
                            documents = search_response.result.hits
                        else:
                            documents = search_response.result.get("documents", [])
                
                # Method 3: If still no documents, try with model_dump
                if not documents and hasattr(search_response, 'model_dump'):
                    try:
                        dump = search_response.model_dump()
                        if 'hits' in dump:
                            documents = dump.get('hits', [])
                        elif 'result' in dump and isinstance(dump['result'], dict):
                            if 'hits' in dump['result']:
                                documents = dump['result']['hits']
                            elif 'documents' in dump['result']:
                                documents = dump['result']['documents']
                    except Exception as dump_error:
                        print(f"Error dumping model: {dump_error}")
                
                # Log status for debugging
                print(f"Documents found for index {index_name}: {len(documents)}")
                
            except Exception as search_error:
                # Just log the error but don't fail the entire page
                print(f"Error listing documents: {search_error}")
                # We'll continue with an empty documents list
        
        return render_template(
            'view_index.html', 
            index=index, 
            index_name=index_name, 
            documents=documents
        )
    except Exception as e:
        return render_template('view_index.html', error=str(e))

@app.route('/indexes/<index_name>/search', methods=['GET', 'POST'])
def search_index(index_name):
    """Search in a specific index."""
    if request.method == 'POST':
        try:
            query = request.form.get('query', '')
            top_k = int(request.form.get('top_k', 10))
            
            # Debug information
            print(f"Searching index '{index_name}' for query: '{query}' with top_k: {top_k}")
            
            client = get_compass_client()
            response = client.search_documents(
                index_name=index_name,
                query=query,
                top_k=top_k
            )
            
            # Print response information for debugging
            print(f"Response type: {type(response)}")
            if hasattr(response, '__dict__'):
                print(f"Response attributes: {vars(response)}")
            elif isinstance(response, dict):
                print(f"Response keys: {response.keys()}")
            
            # Handle different response formats
            if isinstance(response, dict) and response.get('error'):
                return render_template(
                    'search.html', 
                    index_name=index_name, 
                    error=response.get('error')
                )
            elif hasattr(response, 'error') and response.error:
                return render_template(
                    'search.html', 
                    index_name=index_name, 
                    error=response.error
                )
            
            # Extract documents from the response using all possible patterns
            documents = []
            
            # Primary extraction: from hits array
            if hasattr(response, 'hits') and response.hits:
                documents = response.hits
                print(f"Extracted {len(documents)} documents from response.hits")
            # Try all possible ways to extract documents
            elif isinstance(response, dict):
                if 'hits' in response:
                    documents = response.get('hits', [])
                elif 'documents' in response:
                    documents = response.get('documents', [])
                elif 'result' in response and isinstance(response['result'], dict):
                    result = response['result']
                    if 'documents' in result:
                        documents = result.get('documents', [])
                    elif 'hits' in result:
                        documents = result.get('hits', [])
            elif hasattr(response, 'result'):
                if response.result:
                    if isinstance(response.result, dict) and 'documents' in response.result:
                        documents = response.result.get('documents', [])
                    elif isinstance(response.result, dict) and 'hits' in response.result:
                        documents = response.result.get('hits', [])
                    elif hasattr(response.result, 'documents'):
                        documents = response.result.documents
                    elif hasattr(response.result, 'hits'):
                        documents = response.result.hits
            elif hasattr(response, 'documents'):
                documents = response.documents
            
            # Additional attempt for nested structures
            elif hasattr(response, 'results') and hasattr(response.results, 'documents'):
                documents = response.results.documents
            
            # Debug document extraction
            print(f"Found {len(documents)} documents in search results")
            if not documents and hasattr(response, 'model_dump'):
                # For Pydantic models, try using model_dump to see the structure
                try:
                    dump = response.model_dump()
                    print(f"Response model dump: {dump}")
                    # Try extraction from dumped model
                    if 'hits' in dump:
                        documents = dump.get('hits', [])
                    elif 'documents' in dump:
                        documents = dump.get('documents', [])
                    elif 'result' in dump and isinstance(dump['result'], dict):
                        if 'documents' in dump['result']:
                            documents = dump['result'].get('documents', [])
                        elif 'hits' in dump['result']:
                            documents = dump['result'].get('hits', [])
                except Exception as dump_error:
                    print(f"Error dumping model: {dump_error}")
            
            return render_template(
                'search.html', 
                index_name=index_name, 
                query=query, 
                documents=documents
            )
        except Exception as e:
            print(f"Search error: {str(e)}")
            return render_template('search.html', index_name=index_name, error=str(e))
    
    return render_template('search.html', index_name=index_name)

@app.route('/indexes/<index_name>/upload', methods=['GET', 'POST'])
def upload_document(index_name):
    """Upload a document to an index."""
    if request.method == 'POST':
        try:
            # Check if file was uploaded
            if 'document' not in request.files:
                return render_template(
                    'upload.html', 
                    index_name=index_name, 
                    error="No file selected"
                )
            
            file = request.files['document']
            if file.filename == '':
                return render_template(
                    'upload.html', 
                    index_name=index_name, 
                    error="No file selected"
                )
            
            # Read the file
            file_bytes = file.read()
            filename = file.filename
            content_type = file.content_type or 'application/octet-stream'
            document_id = str(uuid.uuid4())
            
            # Check if advanced settings are enabled
            use_advanced_settings = 'advanced_settings' in request.form
            
            if use_advanced_settings:
                # Get parsing settings
                pdf_parsing_strategy = request.form.get('pdf_parsing_strategy', 'default')
                chunk_size = int(request.form.get('chunk_size', 1000))
                chunk_overlap = int(request.form.get('chunk_overlap', 200))
                
                # Create temporary folder for the file
                temp_dir = "/tmp/compass_uploads"
                os.makedirs(temp_dir, exist_ok=True)
                temp_file_path = os.path.join(temp_dir, filename)
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(file_bytes)
                
                # Setup parser config based on parsing strategy
                if pdf_parsing_strategy == 'image_to_markdown':
                    parser_config = ParserConfig(
                        pdf_parsing_strategy=PDFParsingStrategy.ImageToMarkdown,
                        num_tokens_per_chunk=chunk_size,
                        num_tokens_overlap=chunk_overlap
                    )
                elif pdf_parsing_strategy == 'text_extraction':
                    parser_config = ParserConfig(
                        pdf_parsing_strategy=PDFParsingStrategy.QuickText,  # QuickText is the text extraction option
                        num_tokens_per_chunk=chunk_size,
                        num_tokens_overlap=chunk_overlap
                    )
                else:
                    # Default option
                    parser_config = ParserConfig(
                        num_tokens_per_chunk=chunk_size,
                        num_tokens_overlap=chunk_overlap
                    )
                
                try:
                    # Create a new parser client with our custom config
                    parser_client = CompassParserClient(
                        parser_url=os.getenv("COMPASS_PARSER_URL"),
                        bearer_token=os.getenv("COMPASS_PARSER_BEARER_TOKEN"),
                        parser_config=parser_config
                    )
                    
                    # Process files in the directory (since the SDK doesn't seem to have a direct process_file method)
                    # Create a temporary folder and place our file there
                    parsed_docs = []
                    
                    # Use process_folder since that's what's used in the create_index.py example
                    response = parser_client.process_folder(folder_path=temp_dir)
                    
                    for doc in response:
                        if isinstance(doc, tuple):
                            # This is an error tuple (filename, exception)
                            filename, ex = doc
                            print(f"Failed to parse {filename}: {ex}")
                        else:
                            # This is a valid CompassDocument
                            parsed_docs.append(doc)
                    
                    # Clean up temp directory
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    
                    if not parsed_docs:
                        return render_template(
                            'upload.html',
                            index_name=index_name,
                            error="No documents were successfully parsed"
                        )
                    
                    # Upload using insert_docs
                    client = get_compass_client()
                    response = client.insert_docs(
                        index_name=index_name,
                        docs=iter(parsed_docs)
                    )
                    
                    print(f"Document uploaded with advanced parsing. Response: {response}")
                    
                except Exception as parser_error:
                    # Log the full error for debugging
                    import traceback
                    print(f"Parser error: {str(parser_error)}")
                    print(traceback.format_exc())
                    
                    # Try to clean up temp file if it exists
                    try:
                        if os.path.exists(temp_file_path):
                            os.remove(temp_file_path)
                    except:
                        pass
                    
                    return render_template(
                        'upload.html',
                        index_name=index_name,
                        error=f"Parser error: {str(parser_error)}"
                    )
            else:
                # Use standard upload_document
                client = get_compass_client()
                response = client.upload_document(
                    index_name=index_name,
                    filename=filename,
                    filebytes=file_bytes,
                    content_type=content_type,
                    document_id=document_id
                )
            
            # Check for error in response - handling both object and dictionary formats
            if isinstance(response, dict) and response.get('error'):
                return render_template(
                    'upload.html', 
                    index_name=index_name, 
                    error=response.get('error')
                )
            elif hasattr(response, 'error') and response.error:
                return render_template(
                    'upload.html', 
                    index_name=index_name, 
                    error=response.error
                )
            
            return redirect(url_for('view_index', index_name=index_name))
        except Exception as e:
            return render_template('upload.html', index_name=index_name, error=str(e))
    
    return render_template('upload.html', index_name=index_name)

@app.route('/api-explorer')
def api_explorer():
    """Render the API explorer page."""
    # Define available API methods for both client types
    api_methods = [
        {
            "id": "list_indexes",
            "name": "List Indexes",
            "description": "Retrieve a list of all indexes.",
            "params": []
        },
        {
            "id": "create_index",
            "name": "Create Index",
            "description": "Create a new index with the specified configuration.",
            "params": [
                {
                    "name": "index_name",
                    "type": "string",
                    "required": True,
                    "description": "Name of the index to create."
                },
                {
                    "name": "index_config",
                    "type": "object",
                    "required": False,
                    "description": "Configuration for the index (JSON object). Example: {\"max_chunks_per_doc\": 100}"
                }
            ]
        },
        {
            "id": "search_documents",
            "name": "Search Documents",
            "description": "Search for documents in an index using a query.",
            "params": [
                {
                    "name": "index_name",
                    "type": "string",
                    "required": True,
                    "description": "Name of the index to search."
                },
                {
                    "name": "query",
                    "type": "string",
                    "required": True,
                    "description": "The search query."
                },
                {
                    "name": "top_k",
                    "type": "integer",
                    "required": False,
                    "default": 10,
                    "description": "Number of results to return."
                }
            ]
        },
        {
            "id": "upload_document",
            "name": "Upload Document",
            "description": "Upload a document to an index.",
            "params": [
                {
                    "name": "index_name",
                    "type": "string",
                    "required": True,
                    "description": "Name of the index to upload to."
                },
                {
                    "name": "filename",
                    "type": "string",
                    "required": True,
                    "description": "Name of the file."
                },
                {
                    "name": "filebytes",
                    "type": "string",
                    "required": True,
                    "description": "Base64 encoded file content."
                },
                {
                    "name": "content_type",
                    "type": "string",
                    "required": False,
                    "default": "application/octet-stream",
                    "description": "Content type of the file."
                },
                {
                    "name": "document_id",
                    "type": "string",
                    "required": False,
                    "description": "Custom ID for the document."
                }
            ]
        },
        {
            "id": "process_folder",
            "name": "Process Folder (Parser)",
            "description": "Process all documents in a folder (Parser client only).",
            "params": [
                {
                    "name": "folder_path",
                    "type": "string",
                    "required": True,
                    "description": "Path to the folder containing documents."
                }
            ]
        }
    ]
    
    return render_template('api_explorer.html', api_methods=api_methods)

@app.route('/api/call', methods=['POST'])
def api_call():
    """Make a dynamic API call based on user input."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400
        
        client_type = data.get('client_type')
        method_name = data.get('method')
        params = data.get('params', {})
        max_retries = data.get('max_retries', 3)
        sleep_retry_seconds = data.get('sleep_retry_seconds', 1)
        
        if not client_type or not method_name:
            return jsonify({"error": "Missing client_type or method"}), 400
        
        # Get the appropriate client
        if client_type == 'compass':
            client = get_compass_client()
        elif client_type == 'parser':
            client = get_parser_client()
        else:
            return jsonify({"error": f"Unknown client type: {client_type}"}), 400
        
        # Get the method from the client
        if not hasattr(client, method_name):
            return jsonify({"error": f"Method '{method_name}' not found on {client_type} client"}), 400
        
        method = getattr(client, method_name)
        
        # Function to call the method with retries
        def call_with_retries(method, params, max_retries, sleep_seconds):
            import time
            retry_count = 0
            last_error = None
            
            while retry_count <= max_retries:
                try:
                    return method(**params), None
                except Exception as e:
                    last_error = e
                    retry_count += 1
                    if retry_count <= max_retries:
                        time.sleep(sleep_seconds)
            
            return None, str(last_error)
        
        # Call the method with retries
        result, error = call_with_retries(method, params, max_retries, sleep_retry_seconds)
        
        if error:
            return jsonify({"error": error}), 500
        
        # Convert the result to a JSON-serializable format
        if hasattr(result, 'model_dump'):
            # For Pydantic models
            result_dict = result.model_dump()
        elif hasattr(result, '__dict__'):
            # For other objects
            result_dict = result.__dict__
        else:
            # For primitive types
            result_dict = result
        
        return jsonify({"result": result_dict})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/docs')
def documentation():
    """Render the documentation page."""
    return render_template('documentation.html')

@app.route('/chat')
def chat_home():
    """Render the chat interface with index selection."""
    try:
        client = get_compass_client()
        response = client.list_indexes()
        
        if response.error:
            return render_template('chat.html', error=response.error, indexes=[])
        
        indexes = response.result.get("indexes", [])
        settings = load_settings()
        return render_template('chat.html', indexes=indexes, settings=settings)
    except Exception as e:
        return render_template('chat.html', error=str(e), indexes=[])

@app.route('/indexes/<index_name>/chat')
def chat_with_index(index_name):
    """Render the chat interface for a specific index."""
    try:
        # Check if the index exists
        client = get_compass_client()
        list_response = client.list_indexes()
        
        if list_response.error:
            return render_template('chat.html', index_name=index_name, error=list_response.error, indexes=[])
        
        indexes = list_response.result.get("indexes", [])
        index = next((idx for idx in indexes if idx['name'] == index_name), None)
        
        if not index:
            return render_template('chat.html', error=f"Index '{index_name}' not found", indexes=indexes)
        
        settings = load_settings()
        return render_template('chat.html', index_name=index_name, indexes=indexes, settings=settings)
    except Exception as e:
        return render_template('chat.html', index_name=index_name, error=str(e), indexes=[])

@app.route('/indexes/<index_name>/chat-generate', methods=['POST'])
def generate_chat_response(index_name):
    """Generate a response using Cohere Chat API with Compass search context for a specific index."""
    try:
        # Get request data
        data = request.json
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({
                'success': False, 
                'error': 'Prompt is required'
            }), 400
        
        # Get settings
        settings = load_settings()
        
        # Initialize Cohere client
        cohere_api_key = settings.get('cohere_api_key') or app.config.get('COHERE_API_KEY')
        if not cohere_api_key:
            return jsonify({
                'success': False, 
                'error': 'Cohere API Key is not configured. Please configure it in Settings.'
            }), 500
        
        co = cohere.ClientV2(cohere_api_key)
        
        # Search the index with the prompt to get relevant context
        client = get_compass_client()
        search_response = client.search_documents(
            index_name=index_name,
            query=prompt,
            top_k=5
        )
        
        # Extract documents from the search results
        search_results = []
        if hasattr(search_response, 'hits') and search_response.hits:
            search_results = search_response.hits
        elif hasattr(search_response, 'result') and hasattr(search_response.result, 'hits'):
            search_results = search_response.result.hits
        
        # Create a list of documents to send to Cohere
        documents = []
        for result in search_results:
            if hasattr(result, 'text'):
                documents.append({"data": {"text": result.text}})
            elif hasattr(result, 'content'):
                documents.append({"data": {"text": result.content}})
        
        # Get the model from settings or use default
        chat_model = settings.get('chat_model') or "command-a-03-2025"
        
        # Generate response using Cohere chat API V2 with search results as context
        chat_response = co.chat(
            model=chat_model,
            messages=[{"role": "user", "content": prompt}],
            documents=documents if documents else None
        )
        
        # Format search results for the response
        formatted_search_results = []
        for result in search_results:
            formatted_result = {}
            
            if hasattr(result, 'text'):
                formatted_result['text'] = result.text
            elif hasattr(result, 'content'):
                formatted_result['text'] = result.content
            
            if hasattr(result, 'document_id'):
                formatted_result['document_id'] = result.document_id
            
            if hasattr(result, 'score'):
                formatted_result['score'] = result.score
            
            formatted_search_results.append(formatted_result)
        
        return jsonify({
            'success': True,
            'response': chat_response.message.content[0].text,
            'search_results': formatted_search_results,
            'model_used': chat_model
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/chat/generate', methods=['POST'])
def generate_chat_response_any_index():
    """Generate a response using Cohere Chat API with Compass search context for any index."""
    try:
        # Get request data
        data = request.json
        prompt = data.get('prompt')
        index_name = data.get('index_name')
        
        if not prompt or not index_name:
            return jsonify({
                'success': False, 
                'error': 'Prompt and index name are required'
            }), 400
        
        # Get settings
        settings = load_settings()
        
        # Initialize Cohere client
        cohere_api_key = settings.get('cohere_api_key') or app.config.get('COHERE_API_KEY')
        if not cohere_api_key:
            return jsonify({
                'success': False, 
                'error': 'Cohere API Key is not configured. Please configure it in Settings.'
            }), 500
        
        co = cohere.ClientV2(cohere_api_key)
        
        # Search the index with the prompt to get relevant context
        client = get_compass_client()
        search_response = client.search_documents(
            index_name=index_name,
            query=prompt,
            top_k=5
        )
        
        # Extract documents from the search results
        search_results = []
        if hasattr(search_response, 'hits') and search_response.hits:
            search_results = search_response.hits
        elif hasattr(search_response, 'result') and hasattr(search_response.result, 'hits'):
            search_results = search_response.result.hits
        
        # Create a list of documents to send to Cohere
        documents = []
        for result in search_results:
            if hasattr(result, 'text'):
                documents.append({"data": {"text": result.text}})
            elif hasattr(result, 'content'):
                documents.append({"data": {"text": result.content}})
        
        # Get the model from settings or use default
        chat_model = settings.get('chat_model') or "command-a-03-2025"
        
        # Generate response using Cohere chat API V2 with search results as context
        chat_response = co.chat(
            model=chat_model,
            messages=[{"role": "user", "content": prompt}],
            documents=documents if documents else None
        )
        
        # Format search results for the response
        formatted_search_results = []
        for result in search_results:
            formatted_result = {}
            
            if hasattr(result, 'text'):
                formatted_result['text'] = result.text
            elif hasattr(result, 'content'):
                formatted_result['text'] = result.content
            
            if hasattr(result, 'document_id'):
                formatted_result['document_id'] = result.document_id
            
            if hasattr(result, 'score'):
                formatted_result['score'] = result.score
            
            formatted_search_results.append(formatted_result)
        
        return jsonify({
            'success': True,
            'response': chat_response.message.content[0].text,
            'search_results': formatted_search_results,
            'model_used': chat_model
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Render and process the settings page."""
    settings = load_settings()
    error = None
    success_message = None
    
    if request.method == 'POST':
        # Update settings from form
        settings['compass_api_bearer_token'] = request.form.get('compass_api_bearer_token')
        settings['cohere_api_key'] = request.form.get('cohere_api_key')
        settings['chat_model'] = request.form.get('chat_model')
        
        # Save settings
        if save_settings(settings):
            success_message = "Settings saved successfully!"
        else:
            error = "Failed to save settings."
    
    return render_template('settings.html', settings=settings, error=error, success_message=success_message)

@app.route('/api/models')
def list_models():
    """API endpoint to list Cohere models."""
    api_key = request.args.get('api_key') or load_settings().get('cohere_api_key')
    
    if not api_key:
        return jsonify({"error": "API key is required"})
    
    try:
        # Create Cohere client with provided API key
        client = cohere.Client(api_key=api_key)
        
        # Get list of models
        response = client.models.list()
        
        # Filter chat models and convert to serializable dictionaries
        chat_models = []
        for model in response.models:
            if 'chat' in model.endpoints:
                # Create a serializable dictionary from the model object
                model_dict = {
                    'name': model.name,
                    'description': getattr(model, 'description', ''),
                    'endpoints': model.endpoints,
                    'context_length': getattr(model, 'context_length', 0)
                }
                chat_models.append(model_dict)
        
        return jsonify({"models": chat_models})
    except Exception as e:
        import traceback
        print(f"Error fetching models: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 8080))) 
# API Specification

This document specifies the API endpoints for the Cohere Compass SDK Web Interface. The application uses a combination of traditional web routes for page rendering and API endpoints for AJAX functionality.

## Authentication

All endpoints that interact with the Cohere or Compass APIs require proper authentication through environment variables or settings.

- `COMPASS_API_BEARER_TOKEN`: Token for authenticating with the Compass API
- `COMPASS_PARSER_BEARER_TOKEN`: Token for authenticating with the Compass Parser API
- `COHERE_API_KEY`: API key for Cohere services

## Base URLs

- Web Interface: `http://localhost:8000` (default)
- Compass API: Configured via `COMPASS_API_URL` environment variable
- Compass Parser API: Configured via `COMPASS_PARSER_URL` environment variable

## Web Routes

### Pages

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/indexes` | GET | List all indexes |
| `/indexes/create` | GET | Display index creation form |
| `/indexes/<index_name>` | GET | View details of a specific index |
| `/indexes/<index_name>/search` | GET | Display search interface for an index |
| `/indexes/<index_name>/upload` | GET | Display document upload form |
| `/chat` | GET | Display chat selection interface |
| `/indexes/<index_name>/chat` | GET | Chat interface for a specific index |
| `/api-explorer` | GET | API exploration interface |
| `/docs` | GET | Documentation page |
| `/settings` | GET | Settings page |

### Forms

| Route | Method | Description | Form Parameters |
|-------|--------|-------------|----------------|
| `/indexes/create` | POST | Create a new index | `index_name`, `max_chunks_per_doc` |
| `/indexes/<index_name>/search` | POST | Search index | `query`, `top_k`, `include_metadata` |
| `/indexes/<index_name>/upload` | POST | Upload document | `file` (multipart), `document_id`, `metadata` |
| `/settings` | POST | Update settings | `cohere_api_key`, `compass_api_bearer_token`, `chat_model` |

## API Endpoints

### Index Management

#### List Indexes

```
GET /indexes
```

**Response:**
```json
{
  "indexes": [
    {
      "name": "string",
      "count": 0,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

#### Create Index

```
POST /indexes/create
```

**Request Form Data:**
```
index_name: string
max_chunks_per_doc: integer (default: 100)
```

**Response:**
```json
{
  "success": true,
  "message": "Index created successfully",
  "index": {
    "name": "string",
    "count": 0,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

### Document Management

#### Upload Document

```
POST /indexes/<index_name>/upload
```

**Request Form Data:**
```
file: file (multipart/form-data)
document_id: string (optional)
metadata: JSON string (optional)
```

**Response:**
```json
{
  "success": true,
  "message": "Document uploaded successfully",
  "document_id": "string",
  "num_chunks": 0
}
```

### Search

#### Search Documents

```
POST /indexes/<index_name>/search
```

**Request Form Data:**
```
query: string
top_k: integer (default: 10)
include_metadata: boolean (default: true)
```

**Response:**
```json
{
  "success": true,
  "search_results": [
    {
      "document_id": "string",
      "text": "string",
      "score": 0.0,
      "metadata": {
        "key": "value"
      }
    }
  ],
  "query": "string",
  "top_k": 0
}
```

### Chat

#### Generate Chat Response for Index

```
POST /indexes/<index_name>/chat-generate
```

**Request:**
```json
{
  "prompt": "string"
}
```

**Response:**
```json
{
  "success": true,
  "response": "string",
  "search_results": [
    {
      "document_id": "string",
      "text": "string",
      "score": 0.0,
      "metadata": {
        "key": "value"
      }
    }
  ],
  "model_used": "string"
}
```

#### Generate Chat Response (Any Index)

```
POST /chat/generate
```

**Request:**
```json
{
  "prompt": "string",
  "index_name": "string"
}
```

**Response:**
```json
{
  "success": true,
  "response": "string",
  "search_results": [
    {
      "document_id": "string",
      "text": "string",
      "score": 0.0,
      "metadata": {
        "key": "value"
      }
    }
  ],
  "model_used": "string"
}
```

### API Explorer

#### Call API

```
POST /api/call
```

**Request:**
```json
{
  "method_name": "string",
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "key": "value"
  },
  "execution_time": 0.0
}
```

### Settings

#### List Models

```
GET /api/models
```

**Response:**
```json
{
  "models": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "max_context_length": 0
    }
  ]
}
```

## Error Handling

All API endpoints return errors in the following format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid parameters provided
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Pagination

For endpoints that return multiple items, pagination is supported with the following query parameters:

- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

## Rate Limiting

The application does not implement rate limiting directly, but is constrained by:

1. Cohere API rate limits
2. Compass API rate limits

Users should be aware of these external service constraints when making frequent API calls. 
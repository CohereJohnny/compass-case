# Cohere Compass SDK Web Interface - API Specification

This document outlines the API endpoints for the Cohere Compass SDK Web Interface, structured for migration from Flask to FastAPI.

## API Overview

The API is organized into the following categories:

1. Index Management
2. Document Management
3. Search
4. Chat
5. Settings
6. API Explorer

## Endpoint Specifications

### 1. Index Management

#### 1.1 List Indexes

**Endpoint:** `GET /api/indexes`

**Description:** Retrieves a list of all indexes.

**Response:**
```json
{
  "success": true,
  "indexes": [
    {
      "name": "string",
      "count": "integer",
      "created_at": "string (ISO datetime)"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

#### 1.2 Create Index

**Endpoint:** `POST /api/indexes`

**Description:** Creates a new index.

**Request Body:**
```json
{
  "index_name": "string",
  "max_chunks_per_doc": "integer (optional, default: 100)"
}
```

**Response:**
```json
{
  "success": true,
  "index": {
    "name": "string",
    "created_at": "string (ISO datetime)"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

#### 1.3 Get Index Details

**Endpoint:** `GET /api/indexes/{index_name}`

**Description:** Retrieves details for a specific index.

**Path Parameters:**
- `index_name`: Name of the index

**Response:**
```json
{
  "success": true,
  "index": {
    "name": "string",
    "count": "integer",
    "created_at": "string (ISO datetime)"
  },
  "documents": [
    {
      "document_id": "string",
      "file_name": "string",
      "content_type": "string",
      "uploaded_at": "string (ISO datetime)"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

### 2. Document Management

#### 2.1 Upload Document

**Endpoint:** `POST /api/indexes/{index_name}/documents`

**Description:** Uploads a document to a specific index.

**Path Parameters:**
- `index_name`: Name of the index

**Request Body:**
- `multipart/form-data` with the following fields:
  - `document`: File to upload
  - `document_id`: Optional document ID (string)
  - `advanced_settings`: Boolean indicating if advanced settings should be used
  - `pdf_parsing_strategy`: One of "default", "image_to_markdown", "text_extraction" (optional)
  - `chunk_size`: Integer chunk size (optional, default: 1000)
  - `chunk_overlap`: Integer chunk overlap (optional, default: 200)

**Response:**
```json
{
  "success": true,
  "document": {
    "document_id": "string",
    "file_name": "string",
    "content_type": "string",
    "uploaded_at": "string (ISO datetime)"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

### 3. Search

#### 3.1 Search Documents

**Endpoint:** `POST /api/indexes/{index_name}/search`

**Description:** Searches for documents in a specific index.

**Path Parameters:**
- `index_name`: Name of the index

**Request Body:**
```json
{
  "query": "string",
  "top_k": "integer (optional, default: 10)"
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "document_id": "string",
      "text": "string",
      "score": "float",
      "metadata": "object (optional)"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

### 4. Chat

#### 4.1 Generate Chat Response (Single Index)

**Endpoint:** `POST /api/indexes/{index_name}/chat`

**Description:** Generates a chat response using Cohere API based on documents in a specific index.

**Path Parameters:**
- `index_name`: Name of the index

**Request Body:**
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
      "score": "float"
    }
  ],
  "model_used": "string"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

#### 4.2 Generate Chat Response (Any Index)

**Endpoint:** `POST /api/chat`

**Description:** Generates a chat response using Cohere API based on documents in any index.

**Request Body:**
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
      "score": "float"
    }
  ],
  "model_used": "string"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

### 5. Settings

#### 5.1 Get Settings

**Endpoint:** `GET /api/settings`

**Description:** Retrieves the current application settings.

**Response:**
```json
{
  "success": true,
  "settings": {
    "compass_api_bearer_token": "string (masked)",
    "cohere_api_key": "string (masked)",
    "chat_model": "string"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

#### 5.2 Update Settings

**Endpoint:** `POST /api/settings`

**Description:** Updates application settings.

**Request Body:**
```json
{
  "compass_api_bearer_token": "string (optional)",
  "cohere_api_key": "string (optional)",
  "chat_model": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Settings updated successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

### 6. Models

#### 6.1 List Chat Models

**Endpoint:** `GET /api/models`

**Description:** Retrieves available Cohere chat models.

**Query Parameters:**
- `api_key`: Cohere API key (optional, if not provided in settings)

**Response:**
```json
{
  "success": true,
  "models": [
    {
      "name": "string",
      "description": "string",
      "endpoints": ["string"],
      "context_length": "integer"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

### 7. API Explorer

#### 7.1 Call API Method

**Endpoint:** `POST /api/call`

**Description:** Dynamically calls a Compass SDK method.

**Request Body:**
```json
{
  "client_type": "string (compass or parser)",
  "method": "string",
  "params": "object"
}
```

**Response:**
```json
{
  "success": true,
  "result": "object (depends on the method called)"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

## Authentication

Current implementation does not include authentication. For the VueJS + FastAPI migration, consider:

- API key-based authentication
- OAuth 2.0 integration
- JWT-based authentication
- Role-based access control

## Error Handling

The API should return appropriate HTTP status codes:

- 200: Successful operation
- 400: Bad request (invalid parameters)
- 401: Unauthorized (authentication failure)
- 403: Forbidden (authorization failure)
- 404: Resource not found
- 500: Internal server error

Each error response should include:
- An appropriate HTTP status code
- A JSON body with error details

## API Versioning

For the migration, consider implementing API versioning:

```
/api/v1/...
```

## FastAPI Implementation Notes

When implementing these endpoints in FastAPI:

1. Use Pydantic models for request/response validation
2. Implement dependency injection for common utilities (e.g., clients)
3. Use path operation decorators with appropriate HTTP methods
4. Utilize FastAPI's automatic OpenAPI documentation
5. Implement proper error handling with HTTPException
6. Consider using async/await for improved performance

### Example FastAPI Endpoint

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Index(BaseModel):
    name: str
    count: int
    created_at: str

class IndexList(BaseModel):
    success: bool
    indexes: List[Index]
    
@app.get("/api/indexes", response_model=IndexList)
async def list_indexes(compass_client = Depends(get_compass_client)):
    try:
        response = await compass_client.list_indexes()
        indexes = response.result.get("indexes", [])
        return {
            "success": True,
            "indexes": indexes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
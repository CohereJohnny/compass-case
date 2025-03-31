# Cohere Compass SDK Web Interface - Data Models

This document defines the data models that will be used in the FastAPI backend and VueJS frontend implementation.

## Backend Models (Pydantic)

### 1. Index Models

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class IndexConfig(BaseModel):
    max_chunks_per_doc: int = Field(100, description="Maximum number of chunks per document")

class IndexCreate(BaseModel):
    index_name: str = Field(..., description="Name of the index")
    max_chunks_per_doc: Optional[int] = Field(100, description="Maximum number of chunks per document")

class IndexResponse(BaseModel):
    name: str
    count: int
    created_at: datetime

class IndexList(BaseModel):
    success: bool = True
    indexes: List[IndexResponse]

class IndexDetail(BaseModel):
    success: bool = True
    index: IndexResponse
    documents: List["DocumentResponse"] = []
```

### 2. Document Models

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum

class PDFParsingStrategy(str, Enum):
    DEFAULT = "default"
    IMAGE_TO_MARKDOWN = "image_to_markdown"
    QUICK_TEXT = "text_extraction"

class DocumentUpload(BaseModel):
    document_id: Optional[str] = None
    advanced_settings: bool = False
    pdf_parsing_strategy: Optional[PDFParsingStrategy] = PDFParsingStrategy.DEFAULT
    chunk_size: Optional[int] = 1000
    chunk_overlap: Optional[int] = 200

class DocumentResponse(BaseModel):
    document_id: str
    file_name: str
    content_type: str
    uploaded_at: datetime
    
class SearchResult(BaseModel):
    document_id: str
    text: str
    score: float
    metadata: Optional[dict] = None
```

### 3. Search Models

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class SearchQuery(BaseModel):
    query: str = Field(..., description="Search query")
    top_k: Optional[int] = Field(10, description="Number of results to return")

class SearchResponse(BaseModel):
    success: bool = True
    results: List[SearchResult]
```

### 4. Chat Models

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="Chat prompt")

class ChatRequestAnyIndex(BaseModel):
    prompt: str = Field(..., description="Chat prompt")
    index_name: str = Field(..., description="Index name")

class ChatResponse(BaseModel):
    success: bool = True
    response: str
    search_results: List[SearchResult]
    model_used: str
```

### 5. Settings Models

```python
from pydantic import BaseModel, Field
from typing import Optional

class Settings(BaseModel):
    compass_api_bearer_token: Optional[str] = None
    cohere_api_key: Optional[str] = None
    chat_model: Optional[str] = None

class SettingsResponse(BaseModel):
    success: bool = True
    settings: Settings

class SettingsUpdate(BaseModel):
    compass_api_bearer_token: Optional[str] = None
    cohere_api_key: Optional[str] = None
    chat_model: Optional[str] = None
```

### 6. API Explorer Models

```python
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, Literal

class ApiCall(BaseModel):
    client_type: Literal["compass", "parser"]
    method: str
    params: Dict[str, Any] = {}

class ApiResponse(BaseModel):
    success: bool = True
    result: Any
```

### 7. Model List Models

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class ChatModel(BaseModel):
    name: str
    description: Optional[str] = None
    endpoints: List[str]
    context_length: Optional[int] = None

class ModelListResponse(BaseModel):
    success: bool = True
    models: List[ChatModel]
```

## Frontend Types (TypeScript)

### 1. Index Types

```typescript
interface IndexConfig {
  max_chunks_per_doc: number;
}

interface IndexCreateParams {
  index_name: string;
  max_chunks_per_doc?: number;
}

interface IndexResponse {
  name: string;
  count: number;
  created_at: string; // ISO date string
}

interface IndexListResponse {
  success: boolean;
  indexes: IndexResponse[];
}

interface DocumentResponse {
  document_id: string;
  file_name: string;
  content_type: string;
  uploaded_at: string; // ISO date string
}

interface IndexDetailResponse {
  success: boolean;
  index: IndexResponse;
  documents: DocumentResponse[];
}
```

### 2. Document Types

```typescript
enum PDFParsingStrategy {
  DEFAULT = "default",
  IMAGE_TO_MARKDOWN = "image_to_markdown",
  QUICK_TEXT = "text_extraction"
}

interface DocumentUploadParams {
  document_id?: string;
  document: File;
  advanced_settings: boolean;
  pdf_parsing_strategy?: PDFParsingStrategy;
  chunk_size?: number;
  chunk_overlap?: number;
}

interface SearchResult {
  document_id: string;
  text: string;
  score: number;
  metadata?: Record<string, any>;
}
```

### 3. Search Types

```typescript
interface SearchQueryParams {
  query: string;
  top_k?: number;
}

interface SearchResponse {
  success: boolean;
  results: SearchResult[];
}
```

### 4. Chat Types

```typescript
interface ChatRequestParams {
  prompt: string;
}

interface ChatRequestAnyIndexParams {
  prompt: string;
  index_name: string;
}

interface ChatResponse {
  success: boolean;
  response: string;
  search_results: SearchResult[];
  model_used: string;
}

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}
```

### 5. Settings Types

```typescript
interface Settings {
  compass_api_bearer_token?: string;
  cohere_api_key?: string;
  chat_model?: string;
}

interface SettingsResponse {
  success: boolean;
  settings: Settings;
}

interface SettingsUpdateParams {
  compass_api_bearer_token?: string;
  cohere_api_key?: string;
  chat_model?: string;
}
```

### 6. API Explorer Types

```typescript
type ClientType = 'compass' | 'parser';

interface ApiCallParams {
  client_type: ClientType;
  method: string;
  params: Record<string, any>;
}

interface ApiMethodParameter {
  type: string;
  required: boolean;
  default?: any;
  description: string;
}

interface ApiMethod {
  description: string;
  parameters: Record<string, ApiMethodParameter>;
}

interface ApiMethodsDefinition {
  compass: Record<string, ApiMethod>;
  parser: Record<string, ApiMethod>;
}

interface ApiResponse {
  success: boolean;
  result: any;
}
```

### 7. Model List Types

```typescript
interface ChatModel {
  name: string;
  description?: string;
  endpoints: string[];
  context_length?: number;
}

interface ModelListResponse {
  success: boolean;
  models: ChatModel[];
}
```

## Store Structure (Pinia)

Here's a suggested structure for your Pinia stores in the VueJS application:

```typescript
// Main application store structure
interface AppState {
  isLoading: boolean;
  error: string | null;
}

// Indexes store structure
interface IndexesState {
  indexes: IndexResponse[];
  currentIndex: IndexDetailResponse | null;
  isLoading: boolean;
  error: string | null;
}

// Chat store structure
interface ChatState {
  messages: Message[];
  currentIndexName: string | null;
  searchResults: SearchResult[];
  modelUsed: string;
  isLoading: boolean;
  error: string | null;
}

// Settings store structure
interface SettingsState {
  settings: Settings;
  availableModels: ChatModel[];
  isLoading: boolean;
  error: string | null;
}

// API Explorer store structure
interface ApiExplorerState {
  clientType: ClientType | null;
  selectedMethod: string | null;
  methodDefinitions: ApiMethodsDefinition;
  paramValues: Record<string, any>;
  response: any;
  isLoading: boolean;
  error: string | null;
}
```

## API Services (Axios)

Here's a suggested structure for your API services in the VueJS application:

```typescript
// api/index.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;

// api/indexes.ts
import apiClient from './index';
import type { 
  IndexListResponse, 
  IndexDetailResponse, 
  IndexCreateParams,
  DocumentUploadParams 
} from '@/types';

export const indexesApi = {
  getIndexes: () => apiClient.get<IndexListResponse>('/indexes'),
  
  getIndex: (indexName: string) => 
    apiClient.get<IndexDetailResponse>(`/indexes/${indexName}`),
    
  createIndex: (params: IndexCreateParams) => 
    apiClient.post('/indexes', params),
    
  uploadDocument: (indexName: string, params: FormData) => 
    apiClient.post(`/indexes/${indexName}/documents`, params, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  
  searchDocuments: (indexName: string, query: string, topK?: number) => 
    apiClient.post(`/indexes/${indexName}/search`, { query, top_k: topK }),
};

// Additional API service files for chat, settings, etc.
```

## Component Structure (VueJS)

Here's a suggested component structure for your VueJS application:

```
src/
└── components/
    ├── layout/
    │   ├── AppHeader.vue
    │   ├── AppFooter.vue
    │   ├── AppNavigation.vue
    │   └── AppLayout.vue
    ├── indexes/
    │   ├── IndexesList.vue
    │   ├── IndexDetail.vue
    │   ├── CreateIndexForm.vue
    │   └── UploadDocumentForm.vue
    ├── search/
    │   ├── SearchForm.vue
    │   └── SearchResults.vue
    ├── chat/
    │   ├── ChatInterface.vue
    │   ├── ChatMessage.vue
    │   ├── ChatInput.vue
    │   └── ContextDisplay.vue
    ├── settings/
    │   ├── SettingsForm.vue
    │   └── ModelSelection.vue
    ├── api-explorer/
    │   ├── ApiExplorer.vue
    │   ├── MethodSelection.vue
    │   ├── ParameterForm.vue
    │   └── ResponseDisplay.vue
    └── common/
        ├── Button.vue
        ├── Card.vue
        ├── Modal.vue
        ├── Spinner.vue
        └── Alert.vue
``` 
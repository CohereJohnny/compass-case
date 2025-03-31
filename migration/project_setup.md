# Cohere Compass SDK Web Interface - Project Setup Guide

This guide outlines the steps to set up the new VueJS frontend and FastAPI backend project structure for the Cohere Compass SDK Web Interface.

## Repository Structure

```
compass-vue-fastapi/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── indexes.py
│   │   │   │   ├── documents.py
│   │   │   │   ├── search.py
│   │   │   │   ├── chat.py
│   │   │   │   └── settings.py
│   │   │   └── dependencies.py
│   │   ├── core/          # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── config.py  # Application config
│   │   │   └── security.py
│   │   ├── models/        # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── index.py
│   │   │   ├── document.py
│   │   │   ├── search.py
│   │   │   ├── chat.py
│   │   │   └── settings.py
│   │   ├── services/      # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── compass.py # SDK wrapper
│   │   │   └── storage.py # Settings storage
│   │   └── main.py        # FastAPI app entry point
│   ├── tests/             # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── test_api/
│   │       ├── __init__.py
│   │       └── test_indexes.py
│   ├── .env.example       # Example environment variables
│   ├── pyproject.toml     # Python package config
│   ├── poetry.lock        # Dependencies lock file
│   └── README.md          # Backend documentation
├── frontend/              # VueJS frontend
│   ├── public/            # Static assets
│   │   ├── favicon.ico
│   │   └── index.html
│   ├── src/
│   │   ├── assets/        # Images, fonts, etc.
│   │   ├── components/    # Vue components
│   │   │   ├── common/
│   │   │   ├── layout/
│   │   │   ├── indexes/
│   │   │   ├── chat/
│   │   │   └── settings/
│   │   ├── composables/   # Reusable composition functions
│   │   ├── router/        # Vue Router configuration
│   │   │   └── index.ts
│   │   ├── stores/        # Pinia stores
│   │   │   ├── index.ts
│   │   │   ├── indexes.ts
│   │   │   ├── chat.ts
│   │   │   └── settings.ts
│   │   ├── types/         # TypeScript types
│   │   │   ├── index.ts
│   │   │   ├── api.ts
│   │   │   └── models.ts
│   │   ├── views/         # Page components
│   │   │   ├── HomeView.vue
│   │   │   ├── IndexesView.vue
│   │   │   ├── ChatView.vue
│   │   │   └── SettingsView.vue
│   │   ├── services/      # API services
│   │   │   ├── api.ts
│   │   │   ├── indexes.ts
│   │   │   ├── chat.ts
│   │   │   └── settings.ts
│   │   ├── App.vue        # Root Vue component
│   │   ├── main.ts        # Entry point
│   │   └── env.d.ts       # TypeScript env declaration
│   ├── .env.development   # Development environment variables
│   ├── .env.production    # Production environment variables
│   ├── index.html         # Entry HTML file
│   ├── tsconfig.json      # TypeScript configuration
│   ├── vite.config.ts     # Vite configuration
│   ├── package.json       # Node dependencies
│   └── README.md          # Frontend documentation
├── docker/                # Docker configuration
│   ├── backend/
│   │   └── Dockerfile
│   └── frontend/
│       └── Dockerfile
├── docker-compose.yml     # Docker Compose configuration
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 16+
- Docker and Docker Compose (optional, for containerized development)
- Git

### Step 1: Create the Project Structure

```bash
# Create project root directory
mkdir compass-vue-fastapi
cd compass-vue-fastapi

# Create basic directory structure
mkdir -p backend/app/{api/{routes},core,models,services} backend/tests frontend/src
```

### Step 2: Set Up the Backend (FastAPI)

#### Install Poetry (Dependency Management)

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Configure Poetry to create virtual environments in the project directory
poetry config virtualenvs.in-project true
```

#### Initialize Backend Project

```bash
cd backend

# Initialize Poetry project
poetry init \
  --name "compass-sdk-backend" \
  --description "FastAPI backend for Cohere Compass SDK Web Interface" \
  --author "Your Name <your.email@example.com>" \
  --python "^3.10"

# Add dependencies
poetry add fastapi uvicorn pydantic python-dotenv cohere-compass
poetry add pytest pytest-asyncio httpx --group dev
```

#### Create Main Application File

Create `backend/app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import indexes, documents, search, chat, settings

app = FastAPI(
    title="Cohere Compass SDK API",
    description="API for the Cohere Compass SDK Web Interface",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(indexes.router, prefix="/api", tags=["indexes"])
app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(settings.router, prefix="/api", tags=["settings"])

@app.get("/api/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
```

#### Create Configuration File

Create `backend/app/core/config.py`:

```python
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Cohere Compass SDK API"
    
    # CORS settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",  # Vue development server
        "http://localhost:8000",  # Production build served by FastAPI
    ]
    
    # Default settings for storage
    SETTINGS_PATH: str = "settings.json"
    
    # Environment variables
    COMPASS_API_URL: str = os.getenv("COMPASS_API_URL", "")
    COMPASS_API_BEARER_TOKEN: str = os.getenv("COMPASS_API_BEARER_TOKEN", "")
    COMPASS_PARSER_URL: str = os.getenv("COMPASS_PARSER_URL", "")
    COMPASS_PARSER_BEARER_TOKEN: str = os.getenv("COMPASS_PARSER_BEARER_TOKEN", "")
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    
    class Config:
        case_sensitive = True

settings = Settings()
```

#### Create an Index Router Example

Create `backend/app/api/routes/indexes.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.models.index import IndexCreate, IndexResponse, IndexList, IndexDetail
from app.api.dependencies import get_compass_client
from app.services.compass import CompassService

router = APIRouter()

@router.get("/indexes", response_model=IndexList)
async def list_indexes(compass_service: CompassService = Depends(get_compass_client)):
    """
    Retrieve a list of all indexes.
    """
    try:
        indexes = await compass_service.list_indexes()
        return {"success": True, "indexes": indexes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/indexes", response_model=IndexResponse)
async def create_index(
    index_data: IndexCreate,
    compass_service: CompassService = Depends(get_compass_client)
):
    """
    Create a new index.
    """
    try:
        index = await compass_service.create_index(
            index_name=index_data.index_name,
            max_chunks_per_doc=index_data.max_chunks_per_doc
        )
        return index
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/indexes/{index_name}", response_model=IndexDetail)
async def get_index(
    index_name: str,
    compass_service: CompassService = Depends(get_compass_client)
):
    """
    Get details for a specific index.
    """
    try:
        index_detail = await compass_service.get_index(index_name)
        return index_detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Create Dependencies

Create `backend/app/api/dependencies.py`:

```python
from fastapi import Depends
from app.core.config import settings
from app.services.compass import CompassService
from app.services.storage import SettingsStorage

def get_settings_storage():
    return SettingsStorage(settings.SETTINGS_PATH)

def get_compass_client(storage: SettingsStorage = Depends(get_settings_storage)):
    """
    Returns a CompassService instance with the appropriate configuration.
    """
    # Get API tokens from storage, falling back to environment variables
    stored_settings = storage.load_settings()
    
    compass_api_bearer_token = stored_settings.get("compass_api_bearer_token", "") or settings.COMPASS_API_BEARER_TOKEN
    compass_parser_bearer_token = stored_settings.get("compass_parser_bearer_token", "") or settings.COMPASS_PARSER_BEARER_TOKEN
    
    # Create and return the service
    return CompassService(
        index_url=settings.COMPASS_API_URL,
        bearer_token=compass_api_bearer_token,
        parser_url=settings.COMPASS_PARSER_URL,
        parser_bearer_token=compass_parser_bearer_token
    )

def get_cohere_api_key(storage: SettingsStorage = Depends(get_settings_storage)):
    """
    Returns the Cohere API key from storage or environment.
    """
    stored_settings = storage.load_settings()
    return stored_settings.get("cohere_api_key", "") or settings.COHERE_API_KEY
```

#### Create Environment Variables File

Create `backend/.env.example`:

```
# Compass API settings
COMPASS_API_URL=your-compass-api-url
COMPASS_API_BEARER_TOKEN=your-compass-api-bearer-token
COMPASS_PARSER_URL=your-compass-parser-url
COMPASS_PARSER_BEARER_TOKEN=your-compass-parser-bearer-token

# Cohere API settings
COHERE_API_KEY=your-cohere-api-key
```

### Step 3: Set Up the Frontend (VueJS)

#### Initialize VueJS Project

```bash
cd ../frontend

# Create a Vue project with Vite
npm create vite@latest . -- --template vue-ts

# Install dependencies
npm install

# Add additional dependencies
npm install vue-router@4 pinia axios bootstrap@5 bootstrap-icons @vueuse/core
npm install -D @types/node
```

#### Configure Vite

Update `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

#### Configure TypeScript

Update `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    
    /* Paths */
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

#### Set Up Vue Router

Create `frontend/src/router/index.ts`:

```typescript
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import HomeView from '@/views/HomeView.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/indexes',
    name: 'indexes',
    component: () => import('@/views/IndexesView.vue'),
  },
  {
    path: '/indexes/create',
    name: 'create-index',
    component: () => import('@/views/CreateIndexView.vue'),
  },
  {
    path: '/indexes/:indexName',
    name: 'index-detail',
    component: () => import('@/views/IndexDetailView.vue'),
    props: true,
  },
  {
    path: '/indexes/:indexName/search',
    name: 'search',
    component: () => import('@/views/SearchView.vue'),
    props: true,
  },
  {
    path: '/indexes/:indexName/upload',
    name: 'upload',
    component: () => import('@/views/UploadView.vue'),
    props: true,
  },
  {
    path: '/indexes/:indexName/chat',
    name: 'chat',
    component: () => import('@/views/ChatView.vue'),
    props: true,
  },
  {
    path: '/chat',
    name: 'chat-index',
    component: () => import('@/views/ChatIndexView.vue'),
  },
  {
    path: '/api-explorer',
    name: 'api-explorer',
    component: () => import('@/views/ApiExplorerView.vue'),
  },
  {
    path: '/docs',
    name: 'documentation',
    component: () => import('@/views/DocumentationView.vue'),
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/SettingsView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
```

#### Set Up Pinia Store

Create `frontend/src/stores/index.ts`:

```typescript
import { createPinia } from 'pinia';

const pinia = createPinia();

export default pinia;
```

Create `frontend/src/stores/indexes.ts`:

```typescript
import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { IndexResponse, IndexDetailResponse } from '@/types/models';
import { indexesApi } from '@/services/indexes';

export const useIndexesStore = defineStore('indexes', () => {
  const indexes = ref<IndexResponse[]>([]);
  const currentIndex = ref<IndexDetailResponse | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  async function fetchIndexes() {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await indexesApi.getIndexes();
      indexes.value = response.data.indexes;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch indexes';
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchIndex(indexName: string) {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await indexesApi.getIndex(indexName);
      currentIndex.value = response.data;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch index';
    } finally {
      isLoading.value = false;
    }
  }

  return {
    indexes,
    currentIndex,
    isLoading,
    error,
    fetchIndexes,
    fetchIndex,
  };
});
```

#### Set Up API Service

Create `frontend/src/services/api.ts`:

```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
```

Create `frontend/src/services/indexes.ts`:

```typescript
import apiClient from './api';
import type { 
  IndexListResponse, 
  IndexDetailResponse, 
  IndexCreateParams 
} from '@/types/models';

export const indexesApi = {
  getIndexes: () => 
    apiClient.get<IndexListResponse>('/indexes'),
  
  getIndex: (indexName: string) => 
    apiClient.get<IndexDetailResponse>(`/indexes/${indexName}`),
  
  createIndex: (params: IndexCreateParams) => 
    apiClient.post('/indexes', params),
};
```

#### Create Types

Create `frontend/src/types/models.ts`:

```typescript
// Index types
export interface IndexConfig {
  max_chunks_per_doc: number;
}

export interface IndexCreateParams {
  index_name: string;
  max_chunks_per_doc?: number;
}

export interface IndexResponse {
  name: string;
  count: number;
  created_at: string;
}

export interface IndexListResponse {
  success: boolean;
  indexes: IndexResponse[];
}

export interface DocumentResponse {
  document_id: string;
  file_name: string;
  content_type: string;
  uploaded_at: string;
}

export interface IndexDetailResponse {
  success: boolean;
  index: IndexResponse;
  documents: DocumentResponse[];
}

// More types will be added as needed...
```

#### Update Main App Entry Point

Update `frontend/src/main.ts`:

```typescript
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import pinia from './stores';

// Import Bootstrap CSS and icons
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

// Create and mount the app
const app = createApp(App);

app.use(router);
app.use(pinia);

app.mount('#app');

// Initialize Bootstrap JS
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
```

#### Create App Component

Update `frontend/src/App.vue`:

```vue
<template>
  <div class="app">
    <AppHeader />
    <main class="container py-4">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import AppHeader from '@/components/layout/AppHeader.vue';
import AppFooter from '@/components/layout/AppFooter.vue';

// Component setup
onMounted(() => {
  console.log('App mounted');
});
</script>

<style>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}
</style>
```

### Step 4: Environment Configuration

#### Create Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/frontend/Dockerfile
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://backend:8000/api
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: ../docker/backend/Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    env_file:
      - ./backend/.env
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Create Dockerfiles

Create `docker/frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

Create `docker/backend/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure poetry to not use virtual environments in Docker
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 5: Create README file

Create `README.md`:

```markdown
# Cohere Compass SDK Web Interface

A modern web interface for the Cohere Compass SDK, built with VueJS and FastAPI.

## Features

- Index Management
- Document Upload and Search
- Chat with Documents using Cohere's LLMs
- API Explorer
- Settings Management

## Project Structure

- `frontend/`: VueJS frontend application
- `backend/`: FastAPI backend API
- `docker/`: Docker configuration files

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+
- Docker and Docker Compose (optional)

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/compass-vue-fastapi.git
   cd compass-vue-fastapi
   ```

2. Set up the backend:
   ```bash
   cd backend
   cp .env.example .env  # Edit this file with your API keys
   poetry install
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

4. Run the backend:
   ```bash
   cd ../backend
   poetry run uvicorn app.main:app --reload
   ```

5. Run the frontend:
   ```bash
   cd ../frontend
   npm run dev
   ```

6. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Using Docker Compose

1. Clone the repository and set up environment variables:
   ```bash
   git clone https://github.com/yourusername/compass-vue-fastapi.git
   cd compass-vue-fastapi
   cp backend/.env.example backend/.env  # Edit this file with your API keys
   ```

2. Start the application:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

## Running the Project

### Starting the Backend

```bash
cd backend
poetry install
cp .env.example .env  # Edit with your API keys
poetry run uvicorn app.main:app --reload
```

### Starting the Frontend

```bash
cd frontend
npm install
npm run dev
```

The application should now be accessible at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Next Steps

1. Implement the remaining backend API endpoints
2. Create Vue components based on the UI component mapping
3. Configure API services and state management
4. Implement error handling and loading states
5. Set up testing for both frontend and backend 
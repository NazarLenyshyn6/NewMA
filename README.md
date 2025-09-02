# Multi-Agent System Architecture

A comprehensive microservices-based platform combining intelligent AI agents, user authentication, session management, and file processing capabilities. This system provides a sophisticated multi-agent orchestration environment with advanced machine learning, data analysis, and conversational AI capabilities through a distributed architecture with Redis caching and PostgreSQL persistence.

## System Overview

The Multi-Agent System is built on a microservices architecture that enables scalable, maintainable, and loosely coupled services. The platform integrates multiple specialized services to provide end-to-end AI-powered data analysis and conversational intelligence capabilities.

### Core Architecture Components

- **API Gateway**: Unified entry point and service orchestration layer
- **Authentication Service**: User management and JWT-based authentication
- **Session Service**: User session lifecycle and state management  
- **File Service**: Dataset upload, storage, and metadata management
- **Agent Service**: Multi-agent AI orchestration with advanced analytics capabilities
- **Frontend**: React-based user interface for system interaction

### Technology Stack

- **Backend Framework**: FastAPI 0.116.1+ across all services
- **Database**: PostgreSQL with SQLAlchemy 2.0+ ORM
- **Cache Layer**: Redis 6.0+ for session and memory management
- **AI/ML Stack**: LangChain, LangGraph, Anthropic Claude integration
- **Data Science**: NumPy, Pandas, Scikit-learn, PyTorch ecosystem
- **Authentication**: JWT tokens with python-jose cryptography
- **Server**: Uvicorn ASGI servers
- **Frontend**: React with TypeScript (Next.js framework)
- **Python**: 3.12+

## Service Architecture

### 1. API Gateway (`api_gateway/`) - Port 8003

**Purpose**: Centralized HTTP proxy and request routing layer providing unified access to all backend services.

**Key Features**:
- JWT token validation and user authentication
- Request routing to appropriate backend services
- Multipart file upload handling
- Server-sent events for streaming responses
- CORS configuration for cross-origin requests
- Standardized error handling and response formatting

**Technology Stack**:
- FastAPI with httpx for async streaming
- requests library for synchronous service communication
- python-jose for JWT token validation

### 2. Authentication Service (`auth_service/`) - Port 8000

**Purpose**: User authentication, registration, and JWT token management.

**Key Features**:
- User registration with email validation
- Secure password hashing using bcrypt
- JWT token generation and validation
- OAuth2 password flow implementation
- User profile management

**Database Schema**:
- **users**: User accounts with hashed passwords and timestamps

**Security Features**:
- bcrypt password hashing with configurable rounds
- JWT tokens with configurable expiration
- Email format validation
- SQL injection prevention through ORM

### 3. Session Service (`session_service/`) - Port 8001

**Purpose**: User session lifecycle management with Redis caching optimization.

**Key Features**:
- Named session creation and management
- Single active session per user enforcement
- Redis-based active session caching (TTL: 3600s)
- Session title uniqueness validation
- Active session deletion protection

**Database Schema**:
- **sessions**: UUID-based sessions with user association and activation status

**Caching Strategy**:
- Cache-first active session retrieval (~1ms response time)
- Database fallback on cache miss
- Automatic cache invalidation on state changes

### 4. File Service (`file_service/`) - Port 8002

**Purpose**: Dataset upload, storage, metadata management, and active file tracking per session.

**Key Features**:
- CSV file upload with automatic analysis and summarization
- Local filesystem storage with user namespacing
- Active file tracking per session with Redis caching
- Pandas-based dataset analysis (row/column count, data types)
- Extensible storage backend architecture
- File lifecycle management (upload, activation, deletion)

**Database Schema**:
- **files**: File metadata with storage URIs and auto-generated summaries

**Storage Architecture**:
- Local filesystem with `{user_id}_{filename}.extension` pattern
- URI-based addressing scheme (`local://` scheme)
- Pluggable storage backends for future cloud integration

### 5. Agent Service (`agent_service/`) - Port 8005

**Purpose**: Multi-agent AI orchestration providing advanced machine learning, data analysis, and conversational capabilities.

**Key Features**:

#### Multi-Agent Architecture
- **LangGraph-based Workflow Management**: State-driven execution graphs with conditional routing
- **Agent Mode Classification**: Technical Mode (comprehensive analysis) vs Quick Analysis Mode (rapid insights)
- **Modular Node System**: Specialized execution nodes for routing, classification, analysis, visualization, and memory management

#### AI/ML Capabilities
- **Anthropic Claude Integration**: Advanced language model capabilities
- **Code Generation & Execution**: Safe Python code execution environment with ML library support
- **Data Analysis**: Statistical analysis, hypothesis testing, ML modeling with scikit-learn, XGBoost, LightGBM
- **Visualization Generation**: Interactive plots using Plotly, Seaborn, Matplotlib
- **NLP Processing**: Text analysis with NLTK, spaCy, sentence transformers

#### Memory System
- **Conversation Memory**: Redis-cached conversation history with PostgreSQL persistence
- **Context Management**: User preferences, analysis summaries, code execution history
- **Session Variables**: Persistent variable storage across code executions
- **Memory Retrieval & Persistence**: Efficient memory operations with cache optimization

#### Execution Workflows

**Technical Mode Workflow**:
1. Task decomposition and subtask classification
2. Analysis action planning with comprehensive strategies
3. Code generation with production-ready error handling
4. Safe code execution with automatic debugging (max 5 attempts)
5. Detailed report generation with statistical validation
6. Memory persistence and context updates

**Quick Analysis Mode Workflow**:
1. Streamlined task breakdown for rapid execution
2. Efficient code generation focused on essential functionality
3. Simple visualizations for immediate insights
4. Concise reporting with key findings
5. Optimized for sub-30-second response times

#### Code Execution Environment
- **Safe Execution Framework**: Controlled execution context with variable persistence
- **Comprehensive ML Libraries**: NumPy, Pandas, PyTorch, scikit-learn, XGBoost, LightGBM, Optuna
- **Visualization Libraries**: Plotly, Seaborn, Matplotlib, NetworkX
- **NLP Libraries**: NLTK, spaCy, sentence-transformers, Gensim
- **Error Handling**: Automatic error capture with debugging workflows

**Database Schema**:
- **agent_memory**: Multi-composite key storage (user_id, session_id, file_name) with binary serialized summaries

**Performance Optimization**:
- Memory-efficient agent state management
- Selective memory loading and variable scoping
- Streaming response optimization via Server-Sent Events
- Cache-first memory retrieval strategy

### 6. Frontend (`frontend/`)

**Purpose**: React-based user interface providing intuitive interaction with the multi-agent system.

**Key Features**:
- User authentication and session management
- File upload interface with drag-and-drop support
- Real-time chat interface with streaming responses
- Session switching and management
- Responsive design for multiple device types

**Technology Stack**:
- Next.js framework with React and TypeScript
- Server-side rendering for optimal performance
- Real-time updates through Server-Sent Events

## Data Flow Architecture

### 1. User Authentication Flow
```
Frontend → API Gateway → Auth Service → PostgreSQL
                      ↓
            JWT Token Generation
                      ↓
      Token stored in Frontend → Used for all subsequent requests
```

### 2. Session Management Flow
```
Frontend → API Gateway → Session Service → PostgreSQL
                                        → Redis Cache (active session)
```

### 3. File Upload & Processing Flow
```
Frontend → API Gateway → File Service → Local Storage
                                     → PostgreSQL (metadata)
                                     → Redis Cache (active file)
                                     → Pandas Analysis → Summary Generation
```

### 4. AI Agent Interaction Flow
```
Frontend → API Gateway → Agent Service → Memory Retrieval (Redis/PostgreSQL)
                                      → LangGraph Orchestration
                                      → Anthropic Claude API
                                      → Code Execution Environment
                                      → Memory Persistence
                                      → Streaming Response → Frontend
```

## Database Architecture

### PostgreSQL Schema Design

**Authentication Database (`auth_db`)**:
```sql
users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,  -- bcrypt hashed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
```

**Session Database (`session_db`)**:
```sql
sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
```

**File Database (`file_db`)**:
```sql
files (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR NOT NULL,
    storage_uri VARCHAR NOT NULL,
    description TEXT NOT NULL,
    summary TEXT NOT NULL,       -- Auto-generated dataset analysis
    storage_type storage_type NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
```

**Agent Database (`agent_db`)**:
```sql
agent_memory (
    user_id INTEGER NOT NULL,
    session_id UUID NOT NULL,
    file_name VARCHAR NOT NULL,
    analysis_summary BYTEA NOT NULL,          -- Pickled analysis results
    visualization_summary BYTEA NOT NULL,     -- Pickled visualization metadata
    code_summary BYTEA NOT NULL,              -- Pickled code execution history
    user_preferences_summary BYTEA NOT NULL,  -- Pickled user patterns
    variables BYTEA NOT NULL,                 -- Pickled session variables
    conversation BYTEA NOT NULL,              -- Pickled conversation history
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, session_id, file_name)
)
```

### Redis Caching Architecture

**Active Session Cache**:
- **Key Pattern**: `session:active:user:{user_id}`
- **Value**: Active session UUID
- **TTL**: 3600 seconds

**Active File Cache**:
- **Key Pattern**: `active_file:user{user_id}:session:{session_id}`
- **Type**: Hash map with file metadata
- **TTL**: 3600 seconds

**Agent Memory Cache**:
- **Key Pattern**: `agent_memory:session:{session_id}:file:{file_name}`
- **Value**: Pickled Memory schema with binary summaries
- **TTL**: 3600 seconds

## API Architecture

### Unified API through Gateway

**Base URL**: `http://localhost:8003/api/v1/gateway`

#### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication with JWT token
- `GET /auth/me` - Current user profile

#### Session Management Endpoints
- `GET /sessions/` - List all user sessions
- `GET /sessions/active` - Get active session ID
- `POST /sessions/` - Create new session (auto-activated)
- `POST /sessions/active/{title}` - Set session as active
- `DELETE /sessions/{title}` - Delete session (if not active)

#### File Management Endpoints
- `GET /files/` - List all user files
- `GET /files/active` - Get active file for session
- `POST /files/active/` - Set file as active
- `POST /files/` - Upload file with automatic analysis
- `DELETE /files/{file_name}` - Delete file

#### Agent Interaction Endpoints
- `GET /chat/stream?question={query}` - Stream agent responses (SSE)
- `GET /chat/history` - Get conversation history
- `POST /chat/save` - Persist conversation memory

## Environment Configuration

### Global Configuration Variables

Create `.env` files in each service directory:

```bash
# Database Configuration (per service)
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_postgres_password_here
DB_NAME=service_specific_db_name

# Security Configuration (shared across all services)
SECRET_KEY=your_secret_key_here_generate_with_openssl_rand_hex_32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Redis Configuration (session_service, file_service, agent_service)
HOST=localhost
PORT=6379
DB=0

# File Storage Configuration (file_service)
LOCAL_STORAGE_PATH=/path/to/file/storage

# Anthropic API Configuration (agent_service)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Deployment Guide

### Development Setup

1. **Prerequisites**:
   ```bash
   # Install PostgreSQL and Redis
   brew install postgresql redis  # macOS
   sudo apt-get install postgresql redis-server  # Ubuntu
   
   # Start services
   brew services start postgresql redis  # macOS
   sudo systemctl start postgresql redis  # Ubuntu
   ```

2. **Database Initialization**:
   ```bash
   # Create databases
   createdb auth_db
   createdb session_db  
   createdb file_db
   createdb agent_db
   ```

3. **Service Startup** (in separate terminals):
   ```bash
   # Auth Service
   cd auth_service && python main.py

   # Session Service  
   cd session_service && python main.py

   # File Service
   cd file_service && python main.py

   # Agent Service
   cd agent_service && python main.py

   # API Gateway
   cd api_gateway && python main.py

   # Frontend
   cd frontend && npm run dev
   ```

### Production Deployment

```bash
# Use Uvicorn with production settings
uvicorn main:app --host 0.0.0.0 --port {service_port} --workers 4
```

### Service Ports

- **Auth Service**: 8000
- **Session Service**: 8001  
- **File Service**: 8002
- **API Gateway**: 8003
- **Agent Service**: 8005
- **Frontend**: 3000

## Performance Characteristics

### Response Time Benchmarks

- **Authentication**: ~50-100ms (database + bcrypt hashing)
- **Session Operations**: ~1-5ms (Redis cache hit), ~10-50ms (cache miss)
- **File Operations**: ~10-100ms (depending on file size and analysis complexity)
- **Agent Responses**: 
  - Quick Analysis Mode: ~10-30 seconds
  - Technical Mode: ~30-120 seconds (with debugging)
- **Memory Operations**: ~1-5ms (Redis), ~10-50ms (PostgreSQL fallback)

### Scalability Considerations

- **Database Connection Pooling**: SQLAlchemy manages connection pools per service
- **Redis Clustering**: Ready for Redis cluster deployment
- **Horizontal Scaling**: Each service can be scaled independently
- **Load Balancing**: API Gateway can be load balanced for high availability

### Memory Management

- **Agent Memory**: Efficient binary serialization with pickle
- **File Processing**: In-memory processing suitable for datasets up to ~1GB
- **Cache Management**: TTL-based expiration with automatic refresh
- **Variable Persistence**: Session-scoped variable storage for code execution

## Security Architecture

### Authentication & Authorization
- **JWT-based Authentication**: Cryptographically signed tokens with configurable expiration
- **Password Security**: bcrypt hashing with configurable rounds  
- **Token Validation**: Shared secret validation across all services
- **User Isolation**: All data scoped to authenticated users

### Data Security
- **Database Security**: Parameterized queries preventing SQL injection
- **File Security**: User-namespaced file storage with access controls
- **Memory Security**: Binary serialization with user/session/file composite keys
- **Network Security**: Internal service communication (production deployment should use private networks)

### API Security
- **Input Validation**: Pydantic schema validation for all endpoints
- **Rate Limiting**: Can be implemented at API Gateway level
- **CORS Configuration**: Configurable cross-origin request policies
- **Error Handling**: Secure error messages without sensitive information exposure

## Monitoring & Observability

### Logging
- **Access Logs**: HTTP request/response logging via Uvicorn
- **Error Tracking**: Comprehensive exception logging across all services
- **Agent Execution**: Detailed logging of workflow execution and decisions

### Health Monitoring
- **Service Health**: Database and Redis connectivity monitoring
- **Performance Metrics**: Response time and throughput tracking
- **Cache Hit Rates**: Redis cache performance monitoring
- **Agent Execution**: Workflow success/failure rates and execution times

### Metrics to Monitor
- **Authentication Success/Failure Rates**
- **Session Creation and Activation Patterns**
- **File Upload Success Rates and Processing Times**
- **Agent Query Response Times by Mode**
- **Cache Hit Rates (Redis)**
- **Database Connection Pool Usage**

## Development Guidelines

### Code Organization
- **Layered Architecture**: Clear separation of API, Service, Repository, and Model layers
- **Dependency Injection**: FastAPI dependency injection for database sessions and security
- **Error Handling**: Consistent exception handling with custom exception types
- **Documentation**: Comprehensive docstrings and API documentation via FastAPI

### Testing Strategy
- **Unit Tests**: Service and repository layer testing
- **Integration Tests**: API endpoint testing with test databases
- **End-to-End Tests**: Full workflow testing through API Gateway
- **Performance Tests**: Load testing for agent response times

### Extensibility Points
- **Storage Backends**: Pluggable storage architecture for cloud providers
- **Agent Modes**: New agent execution modes can be added through LangGraph
- **File Types**: Support for additional file formats (JSON, Excel, Parquet)
- **ML Libraries**: Easy integration of new machine learning frameworks
- **Authentication Providers**: OAuth2 integration with external providers

## Business Logic & Workflows

### User Workflow
1. **Registration/Login**: User creates account or authenticates
2. **Session Creation**: User creates named analysis session
3. **File Upload**: User uploads dataset with automatic analysis
4. **Agent Interaction**: User asks questions about their data
5. **Analysis & Visualization**: Agent provides insights with charts and reports
6. **Memory Persistence**: Conversation and analysis history saved
7. **Session Management**: User can switch between different analysis sessions

### Agent Decision Logic
- **Mode Classification**: Automatic selection between Technical and Quick Analysis modes
- **Task Decomposition**: Complex queries broken into manageable subtasks
- **Code Generation**: Dynamic Python code creation based on dataset characteristics
- **Error Recovery**: Automatic debugging with retry logic (up to 5 attempts)
- **Memory Integration**: Context-aware recommendations based on analysis history

### Data Processing Pipeline
1. **File Upload**: Binary data received via multipart form
2. **Storage**: File saved with user-specific naming convention
3. **Analysis**: Pandas-based dataset analysis and summarization
4. **Caching**: File metadata cached in Redis for fast access
5. **Agent Processing**: Dataset integrated into agent context for analysis

## Integration & Extensibility

### External API Integration
- **Anthropic Claude**: Advanced language model capabilities
- **Future ML APIs**: Architecture supports additional AI service integration
- **Cloud Storage**: Ready for S3, Google Cloud Storage, Azure Blob integration
- **Authentication Providers**: OAuth2 framework for Google, GitHub, etc.

### Microservice Communication
- **HTTP/REST**: Service-to-service communication via HTTP APIs
- **Event-Driven**: Ready for event-driven architecture with message queues
- **Service Discovery**: Hardcoded URLs (development), configurable for production
- **Circuit Breakers**: Can be implemented for fault tolerance

### Data Pipeline Extensions
- **Real-time Analytics**: Stream processing capabilities can be added
- **Batch Processing**: Background job processing for large datasets
- **ETL Pipelines**: Data transformation and loading workflows
- **Machine Learning Pipelines**: Model training and deployment automation

This Multi-Agent System provides a comprehensive platform for AI-powered data analysis with enterprise-grade architecture, security, and scalability. The modular design enables rapid development and deployment of new capabilities while maintaining system reliability and performance.
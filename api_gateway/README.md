# API Gateway Microservice

A FastAPI-based API gateway providing a unified entry point for multi-microservice architecture. This service orchestrates authentication, session management, file operations, and agent interactions through a centralized HTTP proxy layer with comprehensive request routing, token validation, and service coordination.

## Architecture Overview

The microservice implements a gateway pattern with client-server proxy architecture and centralized routing:

- **API Layer**: FastAPI endpoints providing unified interface to backend services
- **Client Layer**: HTTP client abstraction for backend service communication
- **Security Layer**: JWT token validation and OAuth2 integration
- **Schema Layer**: Pydantic models for request/response validation
- **Core Layer**: Configuration management and security utilities

## Technology Stack

- **Framework**: FastAPI 0.116.1+
- **HTTP Client**: Requests 2.32.4+ for synchronous calls, httpx 0.28.1+ for streaming
- **Authentication**: JWT token validation using python-jose 3.5.0+
- **Validation**: Pydantic 2.11.7+ with email validation support
- **Configuration**: Pydantic Settings 2.10.1+ for environment management
- **Server**: Uvicorn 0.35.0+ ASGI server
- **Python**: 3.12+

## Project Structure

```
api_gateway/
├── main.py                       # FastAPI application entry point
├── pyproject.toml               # Project dependencies and configuration
├── .env.example                 # Environment variables template
└── src/
    ├── api/                     # API layer
    │   └── v1/
    │       ├── router.py        # Main API router aggregation
    │       └── routes/
    │           ├── auth.py      # Authentication endpoints
    │           ├── session.py   # Session management endpoints
    │           ├── file.py      # File management endpoints
    │           └── agent.py     # Agent interaction endpoints
    ├── clients/                 # HTTP client layer
    │   ├── base.py              # Base client with response handling
    │   ├── auth.py              # Auth service client
    │   ├── session.py           # Session service client
    │   ├── file.py              # File service client
    │   └── agent.py             # Agent service client
    ├── core/                    # Core utilities and configuration
    │   ├── config.py            # Application configuration management
    │   └── security.py          # JWT token validation utilities
    └── schemas/                 # Pydantic request/response schemas
        ├── auth.py              # Authentication schemas
        ├── session.py           # Session management schemas
        └── file.py              # File operation schemas
```

## Core Components

### Configuration Management (`core/config.py`)

Centralized configuration using Pydantic Settings with environment variable support:

- **BaseConfig**: Foundation class for environment variable loading
- **SecurityConfig**: JWT authentication settings (secret key, algorithm, token expiration)
- **Settings**: Aggregated configuration class combining all settings

Environment variables are loaded from `.env` file in the root directory.

### Security (`core/security.py`)

- **JWTHandler**: JWT token validation and user ID extraction
- **get_current_user_id**: Dependency function for token validation
- **security**: HTTPBearer scheme for Authorization header extraction

### Client Layer Architecture

#### Base Client (`clients/base.py`)

- **BaseClient**: Foundation class providing standardized HTTP response handling
- **_handle_response**: Centralized error handling and JSON parsing
- **Error Propagation**: Consistent exception raising across all client implementations

#### Authentication Client (`clients/auth.py`)

- **register_user**: User registration with email/password validation
- **login**: OAuth2 authentication with form-encoded credentials
- **get_current_user**: User profile retrieval using Bearer token

#### Session Client (`clients/session.py`)

- **get_sessions**: Retrieve all user sessions
- **get_active_session_id**: Fetch currently active session identifier
- **create_session**: Create new session with automatic activation
- **set_active_session**: Switch active session by title
- **delete_session**: Remove session with business rule validation

#### File Client (`clients/file.py`)

- **get_files**: List all user-accessible files
- **get_active_file**: Retrieve active file for specific session
- **set_active_file**: Set file as active for session
- **upload_file**: Multipart file upload with metadata
- **delete_file**: File deletion with active file protection

#### Agent Client (`clients/agent.py`)

- **stream**: Asynchronous streaming of agent responses using httpx
- **get_conversation_memory**: Retrieve conversation history for session
- **save_memory**: Persist conversation memory to backend storage

### Schema Layer

#### Authentication Schemas (`schemas/auth.py`)

- **RegisterRequest**: User registration with email validation and password constraints (min 8 characters)

#### Session Schemas (`schemas/session.py`)

- **NewSessionRequest**: Session creation with title specification

#### File Schemas (`schemas/file.py`)

- **ActiveFileRequest**: Active file specification by name

## API Endpoints

Base URL: `/api/v1/gateway`

### Authentication Routes (`/auth`)

#### GET `/auth/me`
Retrieve the current authenticated user's information.

**Authentication:** Bearer token required

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### POST `/auth/register`
Register a new user with email and password.

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "detail": "User registered successfully",
  "user_id": 2
}
```

**Error Responses:**
- **422**: Validation errors (invalid email format, password too short)
- **409**: User already exists

#### POST `/auth/login`
Authenticate a user and obtain an access token.

**Request Body (form-encoded):**
```
username=user@example.com&password=userpassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Error Responses:**
- **401**: Invalid credentials

### Session Routes (`/sessions`)

#### GET `/sessions/`
Retrieve all sessions for the authenticated user.

**Authentication:** Bearer token required

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": 1,
    "title": "Data Analysis Project",
    "active": true,
    "created_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": 1,
    "title": "Machine Learning Model",
    "active": false,
    "created_at": "2024-01-14T15:20:00Z"
  }
]
```

#### GET `/sessions/active`
Retrieve the ID of the currently active session.

**Authentication:** Bearer token required

**Response:**
```json
"550e8400-e29b-41d4-a716-446655440000"
```

**Error Responses:**
- **404**: No active session found for user

#### POST `/sessions/`
Create a new session and automatically set it as active.

**Authentication:** Bearer token required

**Request Body:**
```json
{
  "title": "New Analysis Session"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "user_id": 1,
  "title": "New Analysis Session",
  "active": true,
  "created_at": "2024-01-15T11:00:00Z"
}
```

**Error Responses:**
- **409**: Session with same title already exists

#### POST `/sessions/active/{title}`
Set a specific session as active by title.

**Authentication:** Bearer token required

**Path Parameters:**
- `title`: Title of the session to activate

**Response:**
```json
{
  "detail": "'Data Analysis Project' set as active session for user_id=1"
}
```

**Error Responses:**
- **404**: Session with specified title not found

#### DELETE `/sessions/{title}`
Delete a session by title (only if not active).

**Authentication:** Bearer token required

**Path Parameters:**
- `title`: Title of the session to delete

**Response:**
```json
{
  "detail": "Session deleted successfully"
}
```

**Error Responses:**
- **404**: Session not found
- **400**: Cannot delete active session

### File Routes (`/files`)

#### GET `/files/`
List all files accessible to the authenticated user.

**Authentication:** Bearer token required

**Response:**
```json
[
  {
    "id": "file-uuid-1",
    "file_name": "sales_data.csv",
    "description": "Monthly sales analysis dataset",
    "storage_uri": "/storage/user1/sales_data.csv",
    "created_at": "2024-01-15T09:00:00Z"
  },
  {
    "id": "file-uuid-2",
    "file_name": "customer_segments.json",
    "description": "Customer segmentation results",
    "storage_uri": "/storage/user1/customer_segments.json",
    "created_at": "2024-01-14T16:30:00Z"
  }
]
```

#### GET `/files/active`
Retrieve the currently active file for the user's session.

**Authentication:** Bearer token required

**Response:**
```json
{
  "file_name": "sales_data.csv",
  "description": "Monthly sales analysis dataset",
  "storage_uri": "/storage/user1/sales_data.csv",
  "summary": "Dataset contains 10,000 sales records with columns: date, product, quantity, revenue"
}
```

**Error Responses:**
- **404**: No active file found for session

#### POST `/files/active/`
Set a specific file as active for the current session.

**Authentication:** Bearer token required

**Request Body:**
```json
{
  "file_name": "customer_segments.json"
}
```

**Response:**
```json
{
  "detail": "Active file updated successfully"
}
```

**Error Responses:**
- **404**: File not found

#### POST `/files/`
Upload a new file with associated metadata to the server.

**Authentication:** Bearer token required

**Request Body (multipart/form-data):**
- `file_name`: Logical name for the file
- `description`: Description of the file contents
- `file`: Binary file data

**Response:**
```json
{
  "detail": "File uploaded successfully",
  "file_id": "file-uuid-3",
  "storage_uri": "/storage/user1/new_dataset.csv"
}
```

**Error Responses:**
- **422**: Invalid file format or missing metadata
- **413**: File size exceeds limit

#### DELETE `/files/{file_name}`
Delete a specific file from the server.

**Authentication:** Bearer token required

**Path Parameters:**
- `file_name`: Name of the file to delete

**Response:**
```json
{
  "detail": "File deleted successfully"
}
```

**Error Responses:**
- **404**: File not found
- **400**: Cannot delete active file

### Agent Routes (`/chat`)

#### GET `/chat/stream`
Stream agent responses in real-time for a given question.

**Authentication:** Bearer token required

**Query Parameters:**
- `question`: User's question to the agent

**Response:**
Streaming text response (Server-Sent Events format)
```
data: The analysis shows that your sales data indicates...
data: Based on the patterns in the dataset...
data: I recommend focusing on the following insights...
```

**Content-Type:** `text/event-stream`

#### GET `/chat/history`
Retrieve conversation history for the current session and active file.

**Authentication:** Bearer token required

**Response:**
```json
{
  "conversation": [
    {
      "role": "user",
      "content": "What are the top selling products?",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "Based on your sales data, the top 3 products are...",
      "timestamp": "2024-01-15T10:30:15Z"
    }
  ],
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "file_name": "sales_data.csv"
}
```

#### POST `/chat/save`
Persist the current conversation memory to the database.

**Authentication:** Bearer token required

**Response:**
```json
{
  "detail": "Conversation memory saved successfully"
}
```

## Service Integration Architecture

### Backend Service Communication

The API Gateway communicates with the following backend services:

- **Auth Service** (Port 8000): User authentication and authorization
- **Session Service** (Port 8001): Session lifecycle management
- **File Service** (Port 8002): File storage and metadata management
- **Agent Service** (Port 8005): AI agent interactions and conversation memory

### Request Flow Pattern

1. **Client Request**: Frontend sends request to API Gateway
2. **Token Validation**: Gateway validates JWT token using security layer
3. **Service Resolution**: Gateway determines target backend service
4. **Request Proxying**: Client layer forwards request to appropriate service
5. **Response Handling**: Gateway processes response and returns to client
6. **Error Propagation**: Consistent error handling across all service boundaries

### Authentication Flow

- **Token Extraction**: OAuth2PasswordBearer extracts tokens from Authorization headers
- **Token Validation**: JWTHandler validates tokens and extracts user IDs
- **Service Authentication**: Tokens are forwarded to backend services for additional validation
- **Error Handling**: Authentication failures return standardized HTTP 401 responses

## Environment Configuration

Create a `.env` file with the following variables:

```bash
# Security Configuration (shared across all services)
SECRET_KEY=your_secret_key_here_generate_with_openssl_rand_hex_32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Security Note**: Generate a secure secret key using:
```bash
openssl rand -hex 32
```

## CORS Configuration

The gateway includes comprehensive CORS middleware configuration:

- **Origins**: Allows all origins (`["*"]`) for development
- **Credentials**: Supports credential-based requests
- **Methods**: Allows all HTTP methods (`["*"]`)
- **Headers**: Allows all headers (`["*"]`)

**Production Note**: Restrict `allow_origins` to specific domains in production environments.

## Error Handling

The service implements comprehensive error handling:

### HTTP Status Codes

- **HTTP 200**: Successful operation
- **HTTP 400**: Bad request (business rule violations)
- **HTTP 401**: Unauthorized (invalid or missing JWT token)
- **HTTP 404**: Resource not found (session, file, or user not found)
- **HTTP 409**: Conflict (duplicate resources)
- **HTTP 413**: Payload too large (file upload size exceeded)
- **HTTP 422**: Validation errors (invalid request data)
- **HTTP 500**: Internal server errors (backend service failures)

### Custom Exception Handling

- **HTTPError Handler**: Converts `requests.HTTPError` to JSON responses
- **Service Error Propagation**: Backend service errors forwarded to clients
- **Validation Errors**: Pydantic validation errors return detailed field-level feedback

## Client Layer Implementation

### Base Client Pattern

All service clients inherit from `BaseClient` providing:

- **_handle_response**: Standardized response processing and error handling
- **JSON Parsing**: Automatic JSON deserialization with error recovery
- **Status Code Validation**: HTTP status code checking with exception raising

### Request Patterns

#### Synchronous Requests (requests library)
Used for standard CRUD operations:
- Authentication operations
- Session management
- File metadata operations
- Memory persistence

#### Asynchronous Requests (httpx library)
Used for streaming operations:
- Agent response streaming
- Real-time data processing

### Service Discovery

Services are discovered through hardcoded base URLs (development configuration):

- **Auth Service**: `http://127.0.0.1:8000/api/v1`
- **Session Service**: `http://127.0.0.1:8001/api/v1`
- **File Service**: `http://127.0.0.1:8002/api/v1`
- **Agent Service**: `http://127.0.0.1:8005/api/v1`

**Production Note**: Implement service discovery mechanism (Consul, etcd) for production deployments.

## Performance Considerations

### Request Routing Efficiency

- **Direct Proxying**: Minimal request transformation overhead
- **Connection Reuse**: HTTP client connection pooling for backend services
- **Timeout Management**: Configurable timeouts for different operation types

### Streaming Optimization

- **Async Streaming**: Non-blocking agent response streaming using httpx
- **Memory Efficiency**: Chunk-based streaming without full response buffering
- **Connection Management**: Automatic connection lifecycle management

### Caching Strategy

The gateway relies on backend services for caching:
- **Session Cache**: Session service manages Redis-based session caching
- **File Metadata**: File service handles metadata caching
- **Authentication**: Auth service manages token validation caching

## Running the Service

### Development Mode
```bash
cd api_gateway
python main.py
```

The service starts on `http://localhost:8003` with auto-reload enabled.

### Production Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8003
```

## Dependencies

Core dependencies as defined in `pyproject.toml`:

- `fastapi>=0.116.1`: Modern web framework for APIs
- `httpx>=0.28.1`: Async HTTP client for streaming
- `pydantic-settings>=2.10.1`: Environment-based configuration
- `pydantic[email]>=2.11.7`: Data validation with email support
- `python-jose>=3.5.0`: JWT token validation
- `python-multipart>=0.0.20`: Multipart form handling for file uploads
- `requests>=2.32.4`: Synchronous HTTP client
- `uvicorn>=0.35.0`: ASGI server

## Business Rules

### Authentication Requirements
- All endpoints (except health checks) require valid JWT Bearer tokens
- Tokens must contain valid `sub` claim with user ID
- Expired or malformed tokens result in HTTP 401 responses

### Session Context Management
- File operations require an active session context
- Session switching affects file operation scope
- Active session deletion is prevented

### File Operation Constraints
- Active files cannot be deleted without deactivation
- File uploads are scoped to the current active session
- File access is restricted to authenticated user's resources

### Agent Interaction Rules
- Agent queries require both active session and active file context
- Conversation memory is session and file-specific
- Memory persistence is explicit through save operations

## Integration Points

### Frontend Integration
- **Authentication Flow**: Supports OAuth2 password flow for web clients
- **File Upload**: Multipart form-data support for file uploads
- **Streaming**: Server-Sent Events for real-time agent responses
- **CORS**: Cross-origin request support for web applications

### Backend Service Contracts
- **Consistent Authentication**: JWT tokens forwarded to all backend services
- **Error Format Standardization**: Uniform error response format across services
- **Request ID Tracking**: Request correlation for distributed tracing (future enhancement)

## Security Considerations

### Token Security
- **JWT Validation**: Cryptographic signature verification for all tokens
- **Secret Key Protection**: Environment variable-based secret management
- **Token Expiration**: Configurable token lifetime with automatic expiration

### Service Communication
- **Internal Network**: Backend services should run on isolated network segments
- **Request Validation**: Input validation at gateway level prevents malicious requests
- **Service Authentication**: Backend services should implement additional authentication layers

### File Security
- **Upload Validation**: File type and size validation at gateway level
- **Access Control**: User-scoped file access enforcement
- **Storage Security**: Files stored with user-specific access controls

## Monitoring and Observability

### Request Logging
- **Access Logs**: HTTP request/response logging via Uvicorn
- **Error Logs**: Exception tracking and error rate monitoring
- **Performance Metrics**: Response time and throughput monitoring

### Health Checks
- **Service Health**: Backend service availability monitoring
- **Gateway Health**: Internal component health verification
- **Dependency Health**: Database and cache connectivity monitoring

## Development Notes

- All endpoints follow RESTful conventions with consistent HTTP verb usage
- Request/response schemas are fully documented through Pydantic models
- Client implementations use static methods for stateless operation
- Service URLs are configurable through environment variables (future enhancement)
- Comprehensive docstrings document all components and business logic
- Error handling provides detailed context for debugging and client feedback
- The gateway serves as a single point of entry for distributed microservice architecture
# File Management Microservice

A FastAPI-based file management microservice providing dataset upload, storage, metadata management, and active file tracking for user sessions. This service supports local filesystem storage with Redis caching and automatic dataset analysis for CSV files.

## Architecture Overview

The microservice implements a layered architecture pattern with clear separation of concerns:

- **API Layer**: FastAPI endpoints handling HTTP requests/responses
- **Service Layer**: Business logic and file orchestration
- **Repository Layer**: Database access abstraction
- **Storage Layer**: Pluggable storage backends (local filesystem, future cloud storage)
- **Cache Layer**: Redis-based active file caching per session
- **Model Layer**: SQLAlchemy ORM models and Pydantic schemas
- **Core Layer**: Configuration, database management, security utilities, custom exceptions, and enums

## Technology Stack

- **Framework**: FastAPI 0.116.1+
- **Database**: PostgreSQL with SQLAlchemy 2.0.41+ ORM
- **Cache**: Redis 6.2.0+ for active file metadata caching
- **Data Processing**: Pandas 2.3.1+ for dataset analysis and summarization
- **Authentication**: JWT token validation using python-jose
- **Storage**: Local filesystem with extensible storage backend architecture
- **Validation**: Pydantic 2.11.7+ for data validation
- **Server**: Uvicorn ASGI server
- **Python**: 3.12+

## Project Structure

```
file_service/
├── main.py                      # FastAPI application entry point
├── pyproject.toml              # Project dependencies and configuration
└── src/
    ├── api/                    # API layer
    │   └── v1/
    │       ├── router.py       # Main API router (v1)
    │       └── routes/
    │           └── file.py     # File management endpoints
    ├── cache/                  # Redis caching layer
    │   └── file.py            # Redis file cache manager
    ├── core/                   # Core utilities and configuration
    │   ├── config.py          # Application configuration management
    │   ├── db.py              # Database connection management
    │   ├── enums.py           # Storage type enumeration
    │   ├── exceptions.py      # Custom file-related exceptions
    │   └── security.py        # JWT token validation utilities
    ├── models/                 # SQLAlchemy ORM models
    │   ├── base.py            # Base model with audit fields
    │   └── file.py            # File model definition
    ├── repositories/           # Data access layer
    │   └── file.py            # File repository operations
    ├── schemas/                # Pydantic schemas
    │   ├── base.py            # Base schema configuration
    │   └── file.py            # File-related schemas
    ├── services/               # Business logic layer
    │   └── file.py            # File management service
    └── storage/                # Storage backend abstraction
        ├── base.py            # Abstract storage interface
        └── local.py           # Local filesystem storage implementation
```

## Core Components

### Configuration Management (`core/config.py`)

Centralized configuration using Pydantic Settings with environment variable support:

- **PostgresConfig**: Database connection settings (host, port, user, password, database)
- **SecurityConfig**: JWT authentication settings (secret key, algorithm, token expiration)
- **LocalStorageConfig**: Local filesystem storage path configuration
- **RedisConfig**: Redis connection settings (host, port, database index)
- **Settings**: Aggregated configuration class combining all settings

Environment variables are loaded from `.env` file in the root directory.

### Database Management (`core/db.py`)

- **DBManager**: Handles SQLAlchemy engine and session lifecycle
- **Connection**: PostgreSQL with configurable connection pooling
- **Session Management**: Context-aware session handling for dependency injection

### Security (`core/security.py`)

- **JWTHandler**: JWT token validation and user ID extraction
- **HTTPBearer**: FastAPI security scheme for token extraction
- **get_current_user_id**: Dependency function for authenticated route protection

### Storage Backend (`storage/`)

#### Abstract Storage Interface (`storage/base.py`)

- **BaseStorage**: Abstract base class defining storage operations
- **File Validation**: Supported file extensions (currently CSV only)
- **Data Loading**: Pandas integration for dataset analysis
- **File Summarization**: Automatic dataset summary generation (rows, columns, data types)
- **Extension Validation**: Enforced file type restrictions

#### Local Storage Implementation (`storage/local.py`)

- **LocalStorage**: Concrete implementation for local filesystem storage
- **File Organization**: User-namespaced file storage with `user_id_filename.extension` pattern
- **URI Scheme**: `local://` scheme for storage URIs
- **Directory Management**: Automatic storage directory creation
- **File Operations**: Upload and deletion with proper error handling

### Cache Management (`cache/file.py`)

- **FileCacheManager**: Redis-based caching for active file metadata per session
- **Session-Specific Keys**: Cache keys formatted as `active_file:user{user_id}:session:{session_id}`
- **TTL Management**: Configurable time-to-live for cached entries (default: 3600 seconds)
- **Hash Storage**: Redis hash maps for structured file metadata storage
- **Connection Management**: Automatic Redis client lifecycle handling

### Custom Exceptions (`core/exceptions.py`)

Specialized exceptions for precise error handling:
- **DuplicateFileNameError**: File name already exists for user
- **UnsupportedFileExtensionError**: File extension not supported

### Enumerations (`core/enums.py`)

- **StorageType**: Enum defining supported storage types (LOCAL, with extensibility for cloud storage)

### Data Models

#### File Model (`models/file.py`)
```python
class File(Base):
    file_name: str (file identifier)
    storage_uri: str (storage location URI)
    description: str (user-provided description)
    summary: str (auto-generated dataset summary)
    storage_type: StorageType (storage backend type)
    user_id: int (owner reference)
    # Inherited from Base:
    id: int (primary key)
    created_at: datetime (auto-generated)
```

#### Pydantic Schemas (`schemas/file.py`)

- **FileCreate**: Internal file creation with all metadata fields
- **FileRead**: Public file data for API responses (excludes user_id and storage_type)
- **ActiveFile**: Minimal schema for setting active files (file_name only)

### Repository Layer (`repositories/file.py`)

Data access abstraction with file operations:
- `create_file(db, file_data)`: Create file record with duplicate name validation
- `get_files(db, user_id)`: Retrieve all user files
- `get_file(db, user_id, file_name)`: Find specific file by name
- `delete_file(db, user_id, file_name)`: Delete file record with validation

### Service Layer (`services/file.py`)

Business logic orchestration with storage and caching integration:
- `get_files(db, user_id)`: Retrieve all user files
- `get_active_file(db, user_id, session_id)`: Get active file from cache
- `upload_file(...)`: Complete file upload workflow with storage and caching
- `set_active_file(db, user_id, session_id, file_name)`: Set existing file as active
- `delete_file(db, user_id, file_name)`: Delete file from storage and database

## API Endpoints

Base URL: `/api/v1`

### File Routes (`/files`)

#### GET `/files/`
Retrieve all files for the authenticated user.

**Authentication:** Bearer token required

**Response:**
```json
[
  {
    "file_name": "sales_data",
    "storage_uri": "local:///path/to/storage/1_sales_data.csv",
    "description": "Monthly sales data for Q1 2024",
    "summary": "The dataset has **1500 rows** and **5 columns**.\n\nIt contains the following features:\n\n- **date**: `datetime64[ns]`\n- **product**: `object`\n- **sales**: `float64`\n- **region**: `object`\n- **quantity**: `int64`"
  }
]
```

#### GET `/files/active/{session}`
Retrieve the currently active file for a specific session.

**Authentication:** Bearer token required

**Path Parameters:**
- `session`: UUID of the session

**Response:**
```json
{
  "file_name": "sales_data",
  "storage_uri": "local:///path/to/storage/1_sales_data.csv", 
  "description": "Monthly sales data for Q1 2024",
  "summary": "The dataset has **1500 rows** and **5 columns**.\n\n..."
}
```

**Error Responses:**
- **404**: No active file found for session

#### POST `/files/active/{session}`
Set a specific file as the active file for a session.

**Authentication:** Bearer token required

**Path Parameters:**
- `session`: UUID of the session

**Request Body:**
```json
{
  "file_name": "sales_data"
}
```

**Response:** HTTP 200 (no content)

**Error Responses:**
- **404**: File not found for user

#### POST `/files/`
Upload a new file and automatically set it as active for the session.

**Authentication:** Bearer token required

**Request:** Multipart form data
- `file_name`: Name for the file (without extension)
- `session_id`: UUID of the session
- `description`: Description of the file content
- `file`: File data (CSV format)

**Response:**
```json
{
  "file_name": "new_dataset",
  "storage_uri": "local:///path/to/storage/1_new_dataset.csv",
  "description": "Customer analysis dataset",
  "summary": "The dataset has **2000 rows** and **8 columns**.\n\n..."
}
```

**Error Responses:**
- **409**: File name already exists
- **422**: Unsupported file extension

#### DELETE `/files/{file_name}`
Delete a file (both metadata and physical file).

**Authentication:** Bearer token required

**Path Parameters:**
- `file_name`: Name of the file to delete

**Response:** HTTP 200 (no content)

**Error Responses:**
- **404**: File not found

## File Management Features

### Supported File Types
- **CSV Files**: Full support with automatic analysis and summarization
- **Extensible Architecture**: Ready for additional file types (JSON, Excel, Parquet, etc.)

### Dataset Analysis
- **Automatic Summarization**: Row count, column count, and data type analysis
- **Pandas Integration**: Leverages pandas for robust data loading and analysis
- **Structured Summaries**: Markdown-formatted summaries for easy consumption

### Storage Management
- **Local Filesystem**: Default storage backend with configurable paths
- **User Namespacing**: Files organized by user ID to prevent conflicts
- **URI-Based Addressing**: Consistent addressing scheme for different storage backends
- **Extensible Design**: Abstract interface ready for cloud storage backends

### Active File Tracking
- **Session-Based**: Active files tracked per user session
- **Redis Caching**: Fast retrieval of active file metadata
- **Automatic Caching**: Newly uploaded files automatically become active
- **Cache Persistence**: TTL-based cache management with refresh on access

### File Lifecycle
- **Upload**: Store file, generate summary, persist metadata, cache as active
- **Activation**: Set existing file as active for session with cache update
- **Retrieval**: List all files or get active file metadata
- **Deletion**: Remove from both storage and database with validation

## Environment Configuration

Create a `.env` file with the following variables:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_postgres_password_here
DB_NAME=file_db

# Security Configuration (shared with other services)
SECRET_KEY=your_secret_key_here_generate_with_openssl_rand_hex_32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Local Storage Configuration
LOCAL_STORAGE_PATH=/path/to/file/storage

# Redis Configuration
HOST=localhost
PORT=6379
DB=0
```

**Security Note**: Generate a secure secret key using:
```bash
openssl rand -hex 32
```

## Database Setup

The application automatically creates database tables on startup using SQLAlchemy's `Base.metadata.create_all()`.

### Required Database Tables

- **files**: File metadata records
  - `id` (integer, primary key, auto-increment)
  - `file_name` (string, file identifier)
  - `storage_uri` (string, storage location URI)
  - `description` (text, user-provided description)
  - `summary` (text, auto-generated dataset summary)
  - `storage_type` (enum, storage backend type)
  - `user_id` (integer, owner reference)
  - `created_at` (timestamp with timezone, auto-generated)

### Database Schema

```sql
CREATE TYPE storage_type AS ENUM ('local');

CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR NOT NULL,
    storage_uri VARCHAR NOT NULL,
    description TEXT NOT NULL,
    summary TEXT NOT NULL,
    storage_type storage_type NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_files_user_id ON files(user_id);
CREATE INDEX idx_files_user_filename ON files(user_id, file_name);
```

## Redis Setup

The service requires Redis for caching active file metadata:

### Redis Key Structure
- **Pattern**: `active_file:user{user_id}:session:{session_id}`
- **Type**: Hash map containing file metadata
- **TTL**: 3600 seconds (1 hour)

### Redis Hash Fields
- `file_name`: Name of the file
- `storage_uri`: Storage location URI
- `description`: File description
- `summary`: Dataset summary
- `storage_type`: Storage backend type
- `user_id`: Owner ID

## Storage Setup

### Local Storage Configuration
- **Base Path**: Configured via `LOCAL_STORAGE_PATH` environment variable
- **Directory Structure**: Flat structure with user-namespaced filenames
- **File Naming**: `{user_id}_{file_name}.{extension}` pattern
- **Permissions**: Ensure write permissions for the application user

### Storage Directory Example
```
/path/to/file/storage/
├── 1_sales_data.csv
├── 1_customer_analysis.csv
├── 2_inventory_report.csv
└── 3_financial_data.csv
```

## Running the Service

### Development Mode
```bash
cd file_service
python main.py
```

The service starts on `http://localhost:8002` with auto-reload enabled.

### Production Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

### Application Lifespan
The service includes proper startup/shutdown handling:
- **Startup**: Redis client connection initialization and database table creation
- **Shutdown**: Graceful Redis client disconnection

## Dependencies

Core dependencies as defined in `pyproject.toml`:

- `fastapi>=0.116.1`: Modern web framework
- `sqlalchemy>=2.0.41`: ORM and database toolkit
- `psycopg2-binary>=2.9.10`: PostgreSQL adapter
- `pydantic>=2.11.7`: Data validation library
- `pydantic-settings>=2.10.1`: Environment-based configuration
- `python-jose>=3.5.0`: JWT implementation (validation only)
- `python-multipart>=0.0.20`: Form data parsing for file uploads
- `redis>=6.2.0`: Redis client library
- `pandas>=2.3.1`: Data analysis and manipulation library
- `uvicorn>=0.35.0`: ASGI server

## Error Handling

The service implements comprehensive error handling:

- **HTTP 400**: Bad request (validation errors)
- **HTTP 404**: Resource not found (file or active file not found)
- **HTTP 409**: Conflict (duplicate file name)
- **HTTP 401**: Unauthorized (invalid JWT token)
- **HTTP 422**: Validation errors (unsupported file extension, invalid request data)
- **HTTP 500**: Internal server errors (storage failures, database errors)

## Business Rules

### File Upload
- File names must be unique per user
- Only CSV files are currently supported
- Uploaded files automatically become active for the session
- Files are analyzed and summarized during upload

### File Naming
- User-provided file names are used as identifiers (without extensions)
- Physical files are stored with user ID prefixes
- Storage URIs use consistent schemes for different backends

### Active File Management
- One active file per user session
- Active file metadata cached in Redis for performance
- Cache TTL automatically refreshed on access
- Missing cache entries trigger database fallback

### File Deletion
- Files are deleted from both database and storage
- No cascade deletion of related entities
- File existence validated before deletion

### Data Analysis
- CSV files automatically analyzed using pandas
- Summaries include row count, column count, and data types
- Summaries formatted in Markdown for readability
- Analysis occurs during upload for immediate availability

## Integration Points

### Authentication Service Integration
- Validates JWT tokens from auth service
- Extracts user ID from token claims
- Shares security configuration (SECRET_KEY, ALGORITHM)

### Session Service Integration
- Session IDs used for active file tracking
- Cache keys include session identifiers
- No direct service communication required

### Token Requirements
- All endpoints require valid Bearer token
- Token must contain valid `sub` claim with user ID
- Token validation uses shared secret key

## Performance Considerations

### Caching Strategy
- **Cache Hit**: Active file lookup ~1ms (Redis hash get)
- **Cache Miss**: No fallback to database for active files
- **Cache Refresh**: Automatic TTL extension on access

### File Processing
- **Small Files**: In-memory processing using pandas
- **Large Files**: Memory usage scales with file size
- **Analysis Time**: Proportional to dataset complexity

### Storage Performance
- **Local Storage**: Limited by filesystem I/O performance
- **Concurrent Access**: File locks prevent corruption
- **Directory Scanning**: Minimal impact with flat structure

### Database Optimization
- Indexed queries on `user_id` and `(user_id, file_name)`
- Minimal database round trips per operation
- Proper connection pooling via SQLAlchemy

## Future Extensibility

### Additional Storage Backends
- S3-compatible storage implementation ready
- Google Cloud Storage support planned
- Azure Blob Storage integration possible

### File Type Support
- JSON file processing with schema analysis
- Excel file support with multi-sheet handling
- Parquet file support for big data workflows
- Image file metadata extraction

### Enhanced Analysis
- Statistical summaries for numerical columns
- Data quality assessment and profiling
- Column relationship analysis
- Missing value pattern detection

## Development Notes

- All file operations are atomic with proper error handling
- Storage backends are pluggable through abstract base class
- Redis cache failures don't affect core functionality (graceful degradation)
- The service follows RESTful API conventions
- Comprehensive docstrings document all components
- Environment variables provide secure configuration management
- Pandas integration enables rich dataset analysis capabilities
- Extensible storage architecture supports multiple backends
# AI Agent Service

A FastAPI-based intelligent agent microservice providing advanced machine learning and data analysis capabilities through LangGraph orchestration. This service delivers AI-powered insights, code generation, visualization, and conversational analysis through a sophisticated multi-agent system with Redis-based memory management and PostgreSQL persistence.

## Architecture Overview

The microservice implements a multi-agent orchestration pattern with state-driven execution graphs:

- **Orchestration Layer**: LangGraph-based workflow management with conditional routing
- **Agent Layer**: Specialized AI agents for different analysis modes (Technical, Quick Analysis)
- **Node Layer**: Modular execution units for specific tasks (routing, classification, analysis, visualization)
- **Service Layer**: Business logic orchestration and streaming response management
- **Memory Layer**: Conversation and context management with Redis caching
- **Repository Layer**: PostgreSQL data persistence abstraction
- **Cache Layer**: Redis-based memory caching for performance optimization
- **Core Layer**: Configuration, database management, and shared utilities

## Technology Stack

- **Framework**: FastAPI 0.116.1+
- **AI/ML Stack**: 
  - LangChain 0.3.27+ for agent orchestration
  - LangGraph 0.6.5+ for workflow management
  - Anthropic Claude for LLM capabilities
  - PyTorch 2.8.0+ for deep learning
- **Data Science Libraries**:
  - NumPy 2.3.2+, Pandas 2.3.1+, SciPy 1.16.1+
  - Scikit-learn 1.7.1+, XGBoost 3.0.4+, LightGBM 4.6.0+
  - Statsmodels 0.14.5+, Optuna 4.5.0+ for optimization
- **Visualization**: Plotly 6.3.0+, Seaborn 0.13.2+, Matplotlib
- **NLP**: NLTK 3.9.1+, spaCy 3.8.7+, Sentence Transformers 5.1.0+
- **Database**: PostgreSQL with SQLAlchemy 2.0.43+ ORM
- **Cache**: Redis 6.4.0+ for memory and state management
- **Server**: Uvicorn 0.35.0+ ASGI server
- **Python**: 3.12+

## Project Structure

```
agent_service/
├── main.py                       # FastAPI application entry point
├── pyproject.toml               # Project dependencies and configuration
├── graphs_visualization.ipynb   # Agent graph visualization notebook
└── src/
    ├── agents/                  # AI agent orchestration layer
    │   ├── graphs/
    │   │   ├── builder.py       # Agent execution graph construction
    │   │   └── orchestrator.py  # Multi-agent orchestration system
    │   ├── models/
    │   │   └── anthropic_.py    # Anthropic Claude model integration
    │   ├── nodes/               # Modular execution nodes
    │   │   ├── base.py          # Base node implementation
    │   │   ├── agent_model_classification.py  # Agent mode classification
    │   │   ├── conditional_routing.py         # Conditional routing logic
    │   │   ├── context_advising.py           # Context-aware advisory
    │   │   ├── direct_responding.py          # Direct response generation
    │   │   ├── subtask_classification.py     # Subtask categorization
    │   │   ├── summarization.py             # Content summarization
    │   │   ├── analysis/        # Analysis-specific nodes
    │   │   │   ├── action_planing.py        # Analysis action planning
    │   │   │   ├── code_generation.py       # Analysis code generation
    │   │   │   └── report_generation.py     # Analysis report generation
    │   │   ├── code/            # Code execution and debugging
    │   │   │   ├── debagging.py # Code debugging and error resolution
    │   │   │   └── execution.py # Safe code execution environment
    │   │   ├── memory/          # Memory management nodes
    │   │   │   ├── retrieval.py # Memory retrieval operations
    │   │   │   └── save.py      # Memory persistence operations
    │   │   ├── task/            # Task management nodes
    │   │   │   ├── decomposition.py           # Task decomposition
    │   │   │   ├── decomposition_summarization.py  # Task summary
    │   │   │   └── routing.py   # Task routing logic
    │   │   └── visualization/   # Visualization nodes
    │   │       ├── action_planing.py        # Visualization planning
    │   │       ├── code_generation.py       # Visualization code generation
    │   │       └── display.py   # Visualization display handling
    │   ├── prompts/             # AI prompt templates and management
    │   │   ├── agent_mode_classification.py # Mode classification prompts
    │   │   ├── code_debagging.py           # Code debugging prompts
    │   │   ├── context_advising.py         # Context advisory prompts
    │   │   ├── direct_responding.py        # Direct response prompts
    │   │   ├── fallback_handling.py        # Fallback handling prompts
    │   │   ├── subtask_classification.py   # Subtask classification prompts
    │   │   ├── summarization.py            # Summarization prompts
    │   │   ├── analysis/        # Analysis-specific prompts
    │   │   │   ├── action_planing.py
    │   │   │   ├── code_generation.py
    │   │   │   └── report_generation.py
    │   │   ├── task/            # Task management prompts
    │   │   │   ├── decomposition.py
    │   │   │   ├── decomposition_summarization.py
    │   │   │   └── routing.py
    │   │   └── visualization/   # Visualization prompts
    │   │       ├── action_planing.py
    │   │       └── code_generation.py
    │   ├── state.py             # Agent state management
    │   └── structured_outputs/  # Structured output schemas
    │       └── task/
    │           └── decomposition.py
    ├── api/                     # API layer
    │   └── v1/
    │       ├── router.py        # Main API router
    │       └── routes/
    │           ├── agent.py     # Agent interaction endpoints
    │           └── memory.py    # Memory management endpoints
    ├── cache/                   # Redis caching layer
    │   └── memory.py            # Agent memory cache manager
    ├── core/                    # Core utilities and configuration
    │   ├── config.py            # Application configuration management
    │   └── db.py                # Database connection management
    ├── loaders/                 # Data loading utilities
    │   ├── base.py              # Base loader interface
    │   └── local.py             # Local file system loader
    ├── models/                  # SQLAlchemy ORM models
    │   ├── base.py              # Base model with timestamp fields
    │   └── memory.py            # Agent memory model
    ├── repositories/            # Data access layer
    │   └── memory.py            # Memory repository operations
    ├── schemas/                 # Pydantic schemas
    │   ├── agent.py             # Agent request schemas
    │   ├── base.py              # Base schema configuration
    │   └── memory.py            # Memory-related schemas
    └── services/                # Business logic layer
        ├── agent.py             # Agent orchestration service
        └── memory.py            # Memory management service
```

## Core Components

### Configuration Management (`core/config.py`)

Centralized configuration using Pydantic Settings with environment variable support:

- **BaseConfig**: Foundation class for environment variable loading
- **PostgresConfig**: Database connection settings with URL construction
- **RedisConfig**: Redis connection settings (host, port, database index)
- **AnthropicModelConfig**: Anthropic API key configuration for Claude integration
- **Settings**: Aggregated configuration class combining all settings

Environment variables are loaded from `.env` file in the root directory.

### Database Management (`core/db.py`)

- **DBManager**: Handles SQLAlchemy engine and session lifecycle management
- **Connection**: PostgreSQL with configurable connection pooling
- **Session Management**: Context-aware session handling for dependency injection

### Agent State Management (`agents/state.py`)

The `AgentState` serves as the central state container for multi-agent workflows:

#### Core State Attributes
- **question**: Current user query or instruction
- **db**: SQLAlchemy database session for persistence operations
- **user_id**: Unique user identifier for session management
- **session_id**: UUID for session tracking and memory isolation
- **file_name**: Associated dataset or file being analyzed
- **storage_uri**: URI for persistent dataset/file storage
- **dataset_summary**: Pre-computed dataset context for agent reasoning
- **dependencies**: Available ML/data science libraries for code generation

#### Memory and Context Management
- **analysis_summary**: Cumulative summary of analysis operations
- **visualization_summary**: Summary of generated visualizations
- **code_summary**: Summary of executed code and results
- **user_preferences_summary**: Learned user preferences and patterns
- **variables**: Session-scoped variable storage for code execution
- **new_conversation**: Current conversation turn tracking

#### Workflow Control
- **agent_mode**: Execution mode (`TECHNICAL`, `QUICK`) for workflow selection
- **task_flow**: High-level flow type (`ADVISORY`, `EXPLORATORY`)
- **subtasks**: Queue of decomposed subtasks for sequential execution
- **subtask_flow**: Current subtask category (`ANALYSIS`, `VISUALIZATION`, `DIRECT_RESPONSE`)

#### Action Planning and Execution
- **analysis_action_plan**: Structured plan for data analysis execution
- **visualization_action_plan**: Structured plan for visualization generation
- **code**: Generated code snippets for execution
- **error_message**: Error context for debugging workflows

#### Quality Control
- **max_debugging_attempts**: Maximum retry limit for code debugging (default: 5)
- **current_debugging_attempt**: Current debugging iteration counter

#### Output Management
- **analysis_report**: Detailed analysis results and insights
- **visualization**: Generated visualization artifacts or representations

### Agent Graph Architecture

#### Agent Graph Builder (`agents/graphs/builder.py`)

The `AgentGraphBuilder` constructs sophisticated execution workflows using LangGraph:

**Core Nodes**:
- **Task Routing**: Determines workflow path based on user intent
- **Task Decomposition**: Breaks complex queries into manageable subtasks
- **Subtask Classification**: Categorizes subtasks for specialized handling
- **Context Advising**: Provides contextual guidance and recommendations
- **Direct Responding**: Handles simple queries requiring immediate responses

**Analysis Workflow**:
- **Analysis Action Planning**: Develops structured analysis strategies
- **Analysis Code Generation**: Generates executable analysis code
- **Analysis Report Generation**: Synthesizes results into comprehensive reports

**Visualization Workflow**:
- **Visualization Action Planning**: Plans effective data visualizations
- **Visualization Code Generation**: Creates visualization code
- **Visualization Display**: Handles visualization rendering and display

**Code Execution System**:
- **Code Execution**: Safe execution environment for generated code
- **Code Debugging**: Automatic error detection and resolution

**Memory Management**:
- **Memory Retrieval**: Accesses historical context and conversation
- **Memory Save**: Persists conversation and analysis state

**Conditional Routing**: Dynamic workflow branching based on execution context and results

#### Agent Orchestrator (`agents/graphs/orchestrator.py`)

The `AgentsOrchestratorGraphBuilder` manages multiple specialized agent modes:

- **Agent Mode Classification**: Determines optimal agent mode for user requests
- **Technical Agent**: Comprehensive analysis with detailed code generation and debugging
- **Quick Analysis Agent**: Streamlined workflow for rapid insights and simple visualizations

### Memory Management System

#### Memory Cache Manager (`cache/memory.py`)

Redis-based caching for performance optimization:

- **Connection Management**: Automatic Redis client lifecycle with keepalive
- **Key Formatting**: Structured cache keys for session and file isolation
- **Serialization**: Pickle-based object serialization for complex data structures
- **TTL Management**: Configurable time-to-live (default: 3600 seconds)
- **Error Resilience**: Graceful handling of Redis connection failures

#### Memory Service (`services/memory.py`)

High-level memory management with integrated caching:

- **get_memory**: Cache-first retrieval with database fallback
- **get_conversation_memory**: Unpickled conversation history access
- **create_memory**: Initialize memory with base data from loaders
- **update_memory_cache**: Selective field updates in cached memory
- **save_memory**: Persist cached changes to database
- **delete_memory**: Clean removal of memory records

#### Memory Model (`models/memory.py`)

PostgreSQL ORM model for persistent memory storage:

```python
class Memory(Base):
    user_id: int (composite primary key)
    session_id: UUID (composite primary key)
    file_name: str (composite primary key)
    analysis_summary: bytes (LargeBinary, pickled)
    visualization_summary: bytes (LargeBinary, pickled)
    code_summary: bytes (LargeBinary, pickled)
    user_preferences_summary: bytes (LargeBinary, pickled)
    variables: bytes (LargeBinary, pickled)
    conversation: bytes (LargeBinary, pickled)
```

### Data Loading System (`loaders/`)

- **BaseLoader**: Abstract interface for data loading operations
- **LocalLoader**: File system-based data loading with pandas integration

## API Endpoints

Base URL: `/api/v1`

### Agent Routes (`/agent`)

#### POST `/agent/stream`
Stream AI agent responses in real-time using Server-Sent Events.

**Request Body:**
```json
{
  "question": "Analyze the correlation between sales and marketing spend",
  "user_id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "file_name": "sales_data.csv",
  "storage_uri": "/storage/datasets/sales_data.csv",
  "dataset_summary": "Sales dataset with 12 columns and 10,000 records covering 2020-2023"
}
```

**Response (Server-Sent Events):**
```
data: {"type": "text", "data": "I'll analyze the correlation between sales and marketing spend. Let me start by examining the dataset structure..."}

data: {"type": "text", "data": "Based on the analysis, I found a strong positive correlation (r=0.82) between marketing spend and sales revenue..."}

data: {"type": "image", "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."}
```

**Content-Type:** `text/event-stream`

**Error Responses:**
- **422**: Invalid request data or missing required fields
- **500**: Agent execution failure or internal service error

### Memory Routes (`/memory`)

#### GET `/memory/`
Retrieve conversation memory for a user session.

**Query Parameters:**
- `user_id`: User identifier (required)
- `session_id`: Session UUID (required)
- `file_name`: Associated file name (required)
- `storage_uri`: Storage URI for data context (required)

**Response:**
```json
[
  {
    "role": "user",
    "content": "What are the key trends in this dataset?",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  {
    "role": "assistant",
    "content": "The dataset shows three key trends: 1) Seasonal sales peaks in Q4...",
    "timestamp": "2024-01-15T10:30:15Z"
  }
]
```

#### POST `/memory/`
Persist cached memory to database.

**Request Body:**
```json
{
  "user_id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "file_name": "sales_data.csv"
}
```

**Response:**
```json
{
  "detail": "Memory saved successfully"
}
```

#### DELETE `/memory/`
Remove memory record from cache and database.

**Request Body:**
```json
{
  "user_id": 1,
  "file_name": "sales_data.csv"
}
```

**Response:**
```json
{
  "detail": "Memory deleted successfully"
}
```

## Agent Execution Modes

### Technical Mode
Comprehensive analysis mode with full feature set:

- **Deep Task Decomposition**: Complex queries broken into detailed subtasks
- **Advanced Code Generation**: Production-ready code with comprehensive error handling
- **Thorough Debugging**: Multi-attempt error resolution with context preservation
- **Detailed Reporting**: In-depth analysis reports with statistical validation
- **Complex Visualizations**: Multi-panel dashboards and interactive plots
- **Context-Aware Advisory**: Sophisticated recommendations based on analysis history

### Quick Analysis Mode
Optimized mode for rapid insights:

- **Streamlined Decomposition**: Simplified task breakdown for faster execution
- **Efficient Code Generation**: Focused code generation with essential functionality
- **Basic Visualization**: Clear, simple visualizations for immediate insights
- **Concise Reporting**: Summary-focused reports with key findings
- **Rapid Response**: Optimized for sub-30-second response times

## Multi-Agent Workflow Patterns

### Task Routing and Classification

**Task Router**: Analyzes user intent and determines workflow path
- Advisory vs. Exploratory analysis classification
- Complexity assessment and mode recommendation
- Context evaluation for workflow optimization

**Subtask Classifier**: Categorizes decomposed tasks for specialized handling
- Analysis tasks: Statistical analysis, ML modeling, hypothesis testing
- Visualization tasks: Charts, dashboards, interactive plots
- Direct response tasks: Simple queries requiring immediate answers

### Conditional Routing Logic

The system employs sophisticated conditional routing based on execution context:

**From Task Router**:
- Complex queries → Task Decomposition
- Simple queries → Context Advisory

**From Subtask Classifier**:
- Analysis tasks → Analysis Action Planning
- Visualization tasks → Visualization Action Planning
- Direct tasks → Direct Response Generation

**From Code Executor**:
- Execution success → Report/Visualization Generation
- Execution errors → Code Debugging (with retry limits)
- Fallback scenarios → Graceful error handling

### Memory-Driven Context Management

**Context Advising Node**: Provides intelligent recommendations based on:
- Historical analysis patterns from conversation memory
- User preference learning from previous interactions
- Dataset-specific insights from analysis summaries
- Code execution history and optimization patterns

## Environment Configuration

Create a `.env` file with the following variables:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_postgres_password_here
DB_NAME=agent_db

# Redis Configuration
HOST=localhost
PORT=6379
DB=0

# Anthropic API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Security Notes**:
- Store Anthropic API keys securely and rotate regularly
- Use environment-specific database credentials
- Configure Redis authentication in production environments

## Database Setup

The application automatically creates database tables on startup using SQLAlchemy's `Base.metadata.create_all()`.

### Required Database Tables

- **agent_memory**: Multi-agent memory storage
  - `user_id` (integer, composite primary key)
  - `session_id` (UUID, composite primary key, PostgreSQL native)
  - `file_name` (string, composite primary key)
  - `analysis_summary` (large binary, pickled analysis results)
  - `visualization_summary` (large binary, pickled visualization metadata)
  - `code_summary` (large binary, pickled code execution history)
  - `user_preferences_summary` (large binary, pickled user patterns)
  - `variables` (large binary, pickled session variables)
  - `conversation` (large binary, pickled conversation history)
  - `created_at` (timestamp with timezone, auto-generated)
  - `updated_at` (timestamp with timezone, auto-updated)

### Database Schema

```sql
CREATE TABLE agent_memory (
    user_id INTEGER NOT NULL,
    session_id UUID NOT NULL,
    file_name VARCHAR NOT NULL,
    analysis_summary BYTEA NOT NULL,
    visualization_summary BYTEA NOT NULL,
    code_summary BYTEA NOT NULL,
    user_preferences_summary BYTEA NOT NULL,
    variables BYTEA NOT NULL,
    conversation BYTEA NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, session_id, file_name)
);
```

## Redis Setup

The service requires Redis for caching agent memory and execution state:

### Redis Key Structure
- **Pattern**: `agent_memory:session:{session_id}:file:{file_name}`
- **Value**: Pickled Memory schema with binary summaries
- **TTL**: 3600 seconds (1 hour, configurable)

### Redis Configuration
- **Connection Timeout**: 5 seconds for both socket connect and operations
- **Socket Keepalive**: Enabled for persistent connections
- **Decode Responses**: Disabled for binary data handling
- **Error Handling**: Graceful degradation on Redis failures

## Code Execution Environment

### Safe Execution Framework

The agent service includes a secure code execution environment:

- **Dependency Management**: Pre-installed ML/data science libraries
- **Execution Isolation**: Controlled execution context with variable persistence
- **Error Handling**: Automatic error capture and context preservation
- **Memory Management**: Session-scoped variable storage and retrieval

### Available Libraries

The execution environment includes comprehensive ML/data science libraries as defined in the agent state dependencies:

```python
dependencies = [
    "numpy",  # import numpy as np
    "pandas",  # import pandas as pd
    "scipy",  # import scipy
    "sklearn",  # from sklearn import ...
    "statsmodels.api",  # import statsmodels.api as sm
    "joblib",  # import joblib
    "torch",  # import torch
    "torchvision",
    "lightgbm",
    "xgboost",
    "optuna",
    "sentence_transformers",
    "gensim==4.3.2",
    "matplotlib.pyplot",  # import matplotlib.pyplot as plt
    "seaborn",  # import seaborn as sns
    "plotly.express",  # import plotly.express as px
    "nltk",  # import nltk
    "spacy",  # import spacy
    "tqdm",  # from tqdm import tqdm
    "networkx",  # import networkx as nx
]
```

### Code Execution Features

**Code Extraction and Execution**:
- Extracts Python code from triple-backtick code blocks
- Dynamic dependency importing from the predefined library list
- Execution in controlled global and local context environments
- Variable tracking and pickle serialization for session persistence

**Error Handling and Recovery**:
- Automatic error capture and context preservation
- Error message storage in agent state for debugging workflows
- Safe execution environment with exception handling

**Variable Management**:
- Session-scoped variable storage and retrieval
- Pickle-serializable variable filtering
- Context merging between global modules and local variables

## Performance Considerations

### Agent Execution Optimization

- **Memory Efficiency**: Selective memory loading and variable scoping
- **Code Execution**: Controlled execution environment with variable persistence
- **State Management**: Efficient agent state updates and transitions

### Memory Management Performance

- **Cache-First Strategy**: Memory retrieval prioritizes Redis cache (~1-5ms)
- **Database Fallback**: PostgreSQL retrieval on cache miss (~10-50ms)
- **TTL Management**: Fixed cache expiration (3600 seconds) for memory entries
- **Error Resilience**: Graceful fallback to database on Redis failures

### Streaming Response Optimization

- **Chunked Streaming**: Real-time response streaming via Server-Sent Events
- **JSON Format**: Structured streaming output with type and data fields
- **Event-Based Processing**: Handles both text and image streaming events

## Running the Service

### Development Mode
```bash
cd agent_service
python main.py
```

The service starts on `http://localhost:8005` with auto-reload enabled.

### Production Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8005
```

### Application Lifespan
The service includes proper startup/shutdown handling:
- **Startup**: Database table creation and Redis client connection initialization
- **Shutdown**: Graceful Redis client disconnection and resource cleanup

## Dependencies

Core dependencies as defined in `pyproject.toml`:

**Framework and API**:
- `fastapi>=0.116.1`: Modern web framework for APIs
- `uvicorn>=0.35.0`: ASGI server for production deployment

**AI and Agent Framework**:
- `langchain>=0.3.27`: Agent framework and LLM orchestration
- `langchain-anthropic>=0.3.19`: Anthropic Claude integration
- `langgraph>=0.6.5`: State-driven workflow management

**Machine Learning and Data Science**:
- `numpy>=2.3.2`, `pandas>=2.3.1`, `scipy>=1.16.1`: Core data science stack
- `scikit-learn>=1.7.1`: Machine learning algorithms and utilities
- `torch>=2.8.0`, `torchvision>=0.23.0`: Deep learning framework
- `xgboost>=3.0.4`, `lightgbm>=4.6.0`: Gradient boosting implementations
- `statsmodels>=0.14.5`: Statistical modeling and analysis
- `optuna>=4.5.0`: Hyperparameter optimization
- `joblib>=1.5.1`: Parallel computing and model persistence

**Natural Language Processing**:
- `nltk>=3.9.1`: Natural language toolkit
- `spacy>=3.8.7`: Advanced NLP processing
- `sentence-transformers>=5.1.0`: Semantic embeddings and similarity
- `gensim==4.3.2`: Topic modeling and similarity analysis

**Visualization**:
- `plotly>=6.3.0`: Interactive plotting and dashboards
- `seaborn>=0.13.2`: Statistical data visualization
- `networkx>=3.5`: Network analysis and graph visualization

**Data Management**:
- `sqlalchemy>=2.0.43`: ORM and database toolkit
- `psycopg2>=2.9.10`: PostgreSQL adapter
- `redis>=6.4.0`: Redis client library
- `pydantic>=2.11.7`: Data validation and serialization
- `pydantic-settings>=2.10.1`: Environment-based configuration

**Utilities**:
- `tqdm>=4.67.1`: Progress bars and iteration tracking

## Error Handling and Recovery

The service implements comprehensive error handling:

### HTTP Status Codes

- **HTTP 200**: Successful operation completion
- **HTTP 422**: Validation errors (invalid request data, malformed schemas)
- **HTTP 500**: Internal server errors (agent execution failures, database errors)

### Agent Execution Error Recovery

- **Code Execution Errors**: Automatic debugging with up to 5 retry attempts
- **Memory Access Errors**: Graceful fallback to database on cache failures
- **Model API Errors**: Retry logic with exponential backoff for Anthropic API calls
- **Workflow Errors**: Fallback routing to simpler execution paths

### Data Processing Error Handling

- **Data Loading Errors**: Alternative data source suggestions and format conversion
- **Analysis Errors**: Statistical validity checks and alternative method suggestions
- **Visualization Errors**: Fallback to simpler plot types and data aggregation

## Business Rules and Workflow Logic

### Agent Mode Selection
- **Technical Mode**: Selected for complex analysis requiring detailed insights
- **Quick Analysis Mode**: Selected for rapid exploration and simple visualizations
- **Dynamic Selection**: Mode can be overridden based on user preferences or query complexity

### Memory Management Rules
- **Session Isolation**: Memory records are scoped to user, session, and file combinations
- **Cache Consistency**: Updates to memory are atomic across cache and database
- **TTL Management**: Cache entries expire after 1 hour of inactivity
- **Storage Efficiency**: Large binary objects are compressed and optimized for storage

### Code Generation Standards
- **Safety First**: All generated code includes input validation and error handling
- **Reproducibility**: Generated analysis includes random seeds and version information
- **Documentation**: Code includes inline comments and methodology explanations
- **Optimization**: Generated code is optimized for performance and memory usage

### Visualization Guidelines
- **Accessibility**: Generated visualizations include appropriate labels and color schemes
- **Interactivity**: Plotly-based visualizations include zoom, pan, and selection capabilities
- **Export Ready**: Visualizations are generated in multiple formats (PNG, SVG, HTML)
- **Responsive Design**: Visualizations adapt to different display sizes and contexts

## Integration Points

### Anthropic Claude Integration
- **Model Integration**: LangChain integration with Anthropic Claude models
- **Response Streaming**: Real-time response streaming through LangGraph events
- **Prompt Templates**: Structured prompt templates for different agent modes

### Database Integration
- **Connection Pooling**: SQLAlchemy connection pooling for concurrent access
- **Transaction Management**: Atomic operations for data consistency
- **Automatic Schema Creation**: Database tables created automatically on startup

### Cache Integration
- **Redis Connection**: Basic Redis client connection with timeout configuration
- **Error Handling**: Graceful handling of Redis connection errors
- **TTL Management**: Fixed TTL (3600 seconds) for cached memory objects

## Security Considerations

### API Security
- **Input Validation**: Pydantic schema validation for all API inputs
- **SQL Injection Prevention**: SQLAlchemy ORM-based database access
- **Code Execution Control**: Controlled execution environment with error handling

### Data Security
- **Data Isolation**: User data isolation through composite primary keys (user_id, session_id, file_name)
- **Binary Storage**: Secure binary storage of pickled memory components
- **Redis Security**: Redis connection with configurable timeout and keepalive settings

### Model Security
- **API Key Management**: Environment variable-based Anthropic API key configuration
- **LLM Integration**: Secure integration with Anthropic Claude through langchain-anthropic

## Monitoring and Observability

### Application Monitoring
- **Startup/Shutdown**: Proper application lifecycle management with lifespan context
- **Database Connection**: SQLAlchemy-based connection management
- **Redis Connection**: Managed Redis client lifecycle with connection/disconnection
- **Error Logging**: Basic error capture in code execution and memory operations

## Development and Debugging

### Graph Visualization
- **Jupyter Integration**: Graph visualization notebook (`graphs_visualization.ipynb`) for workflow development
- **Print Statements**: Node execution tracking through print statements in invoke methods

### Development Tools
- **Hot Reload**: Development mode with automatic code reloading when running `python main.py`
- **Debug Output**: Print statements in node execution for workflow tracking

## Deployment Considerations

### Resource Requirements
- **Memory**: Sufficient RAM for ML library loading and variable storage
- **CPU**: CPU resources for code execution and LLM processing
- **Storage**: Database storage for persistent memory records
- **Network**: Network connectivity for Anthropic API calls and Redis communication

### Configuration Management
- **Environment Variables**: Configuration through `.env` file
- **Database Setup**: Automatic table creation on startup
- **Redis Setup**: Manual Redis server configuration required

This agent service provides AI-powered data analysis capabilities through a multi-agent orchestration system with memory management and code execution functionality.
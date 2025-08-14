# MLAgent Docker Setup

This document explains the Docker configuration for the MLAgent application.

## Services Overview

The application consists of the following services:

### Infrastructure Services
- **PostgreSQL** (postgres_db): Database server on port 5432
- **Redis** (redis_cache): Cache server on port 6379

### Backend Services
- **Auth Service** (auth_service): Authentication service on port 8000
- **Session Service** (session_service): Session management on port 8061 (mapped from internal port 8001)
- **File Service** (file_service): File management on port 8002
- **Agent Service** (agent_service): ML agent on port 8005
- **API Gateway** (api_gateway): Main API gateway on port 8003

### Frontend Service
- **Frontend** (frontend): Next.js application on port 3000

## Port Mappings

| Service | Internal Port | External Port | Purpose |
|---------|---------------|---------------|---------|
| postgres_db | 5432 | 5432 | PostgreSQL database |
| redis_cache | 6379 | 6379 | Redis cache |
| auth_service | 8000 | 8000 | Authentication API |
| session_service | 8001 | 8061 | Session management API |
| file_service | 8002 | 8002 | File management API |
| api_gateway | 8003 | 8003 | Main API gateway |
| agent_service | 8005 | 8005 | ML agent API |
| frontend | 3000 | 3000 | Web frontend |

## Quick Start

1. **Prerequisites**
   - Docker and Docker Compose installed
   - Environment variables configured in `.env` file

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Stop all services**
   ```bash
   docker-compose down
   ```

4. **View logs**
   ```bash
   docker-compose logs -f [service_name]
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:8003/docs
   - Auth Service: http://localhost:8000/docs

## Useful Commands

### Start services:
```bash
docker-compose up -d
```

### Stop services:
```bash
docker-compose down
```

### View logs:
```bash
docker-compose logs -f [service_name]
```

### Rebuild services:
```bash
docker-compose build
```

### Remove all data (including volumes):
```bash
docker-compose down -v
```

## Development

For development, you can run individual services:

```bash
# Start only database and cache
docker-compose up -d postgres redis

# Then run services individually in development mode
cd auth_service && uvicorn main:app --reload --port 8001
cd session_service && uvicorn main:app --reload --port 8002
# ... etc
```

## Troubleshooting

1. **Port conflicts**: Make sure ports 3000, 6379, 5432, 8000-8004 are not in use
2. **Database connection issues**: Wait for PostgreSQL to be ready (check with `docker-compose logs postgres`)
3. **Permission issues**: Make sure Docker has proper permissions
4. **Out of memory**: Increase Docker memory limit for ML libraries in agent_service

## Health Checks

The services include health checks. You can check status with:
```bash
docker-compose ps
```

All services should show "healthy" status when fully operational.
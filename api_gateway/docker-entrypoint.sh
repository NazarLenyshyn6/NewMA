#!/bin/bash

# Install socat and netcat for port forwarding
apt-get update && apt-get install -y socat netcat-openbsd > /dev/null 2>&1

# Start port forwarding in the background to map 127.0.0.1:XXXX to service:XXXX
echo "Starting socat port forwarding..."
socat TCP-LISTEN:8000,bind=127.0.0.1,fork,reuseaddr TCP:auth_service:8000 &
socat TCP-LISTEN:8001,bind=127.0.0.1,fork,reuseaddr TCP:session_service:8001 &
socat TCP-LISTEN:8002,bind=127.0.0.1,fork,reuseaddr TCP:file_service:8002 &
socat TCP-LISTEN:8005,bind=127.0.0.1,fork,reuseaddr TCP:agent_service:8005 &

# Wait for socat to start and test connections
echo "Waiting for services to be ready..."
sleep 5

# Test connectivity to all services
echo "Testing service connectivity..."
for port in 8000 8001 8002 8005; do
    if nc -z 127.0.0.1 $port 2>/dev/null; then
        echo "Port $port is forwarding correctly"
    else
        echo "Warning: Port $port forwarding may not be working"
    fi
done

echo "Starting FastAPI application..."
# Start the application
exec "$@"
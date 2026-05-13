#!/bin/bash

echo "Cleaning up existing processes..."
# Kill existing Ollama or workers to avoid "address already in use"

sudo pkill -f "src.workers.gpu_worker" || true
sleep 2

echo "Starting Ollama..."
ollama serve &
sleep 3

echo "Starting NGINX..."
sudo systemctl start nginx

echo "Starting workers..."
cd /mnt/c/Users/DELL/server
python3 -m src.workers.gpu_worker --port 8001 &
python3 -m src.workers.gpu_worker --port 8002 &
python3 -m src.workers.gpu_worker --port 8003 &
sleep 2

echo "Reloading NGINX..."
sudo systemctl reload nginx

echo "Testing..."
curl -s -X POST http://localhost/infer \
     -H "Content-Type: application/json" \
     -d '{"query": "How can I remember things better?"}'
echo ""
echo "Server is ready!"

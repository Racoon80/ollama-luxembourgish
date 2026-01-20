#!/bin/bash
# Deployment script for Ollama Luxembourgish on Unraid

set -e

echo "=========================================="
echo "Ollama Luxembourgish Deployment"
echo "=========================================="
echo ""
echo "Model: LLaMAX3-8B-Alpaca"
echo "Language: Luxembourgish (enforced)"
echo "IP: 192.168.106.22:11434"
echo ""

DEPLOY_PATH="/mnt/user/appdata/ai/ollama-luxembourgish"
DATA_PATH="/mnt/user/appdata/ai/ollama-luxembourgish"

# Create directories
echo "[1/6] Creating directories..."
mkdir -p "$DEPLOY_PATH"
mkdir -p "$DATA_PATH"
echo "OK"

# Deploy docker-compose.yml
echo ""
echo "[2/6] Deploying Docker Compose configuration..."
cd "$DEPLOY_PATH"
echo "OK"

# Start container
echo ""
echo "[3/6] Starting Ollama container..."
docker-compose up -d
echo "OK"

# Wait for Ollama to be ready
echo ""
echo "[4/6] Waiting for Ollama to start (30 seconds)..."
sleep 30
echo "OK"

# Pull Luxembourgish model
echo ""
echo "[5/6] Pulling LLaMAX3-8B-Alpaca model..."
echo "This will download ~4.7GB and may take 2-5 minutes..."
docker exec ollama-luxembourgish ollama pull mannix/llamax3-8b-alpaca
echo "OK"

# Create custom Luxembourgish-enforced model
echo ""
echo "[6/6] Creating custom Luxembourgish-enforced model..."
docker exec ollama-luxembourgish ollama create lux-assistant -f /modelfile
echo "OK"

# Test the model
echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Testing Luxembourgish model..."
docker exec ollama-luxembourgish ollama run lux-assistant "Moien! Wéi geet et?" --verbose

echo ""
echo "=========================================="
echo "Model Ready!"
echo "=========================================="
echo ""
echo "Service: http://192.168.106.22:11434"
echo ""
echo "Available models:"
docker exec ollama-luxembourgish ollama list
echo ""
echo "Usage:"
echo "  Interactive: docker exec -it ollama-luxembourgish ollama run lux-assistant"
echo "  API: curl http://192.168.106.22:11434/api/generate -d '{\"model\":\"lux-assistant\",\"prompt\":\"Wéi geet et?\"}'"
echo ""
echo "Integration:"
echo "  - OllamaUI: http://192.168.106.8"
echo "  - Add connection: http://192.168.106.22:11434"
echo ""

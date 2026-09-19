#!/bin/bash

echo "Starting NIDS Data Collector Backend..."

# Check if we are in a virtual environment or if .venv exists
if [ -d ".venv" ]; then
    echo "Using local .venv with sudo..."
    sudo .venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
else
    # Try to use sudo with the current python path, preserving path
    echo "Running with sudo (required for Scapy packet sniffing)..."
    sudo env "PATH=$PATH" uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
fi

#!/bin/bash
# Render startup script for NEEL backend

echo "🚀 Starting NEEL Backend..."
echo "📍 Current directory: $(pwd)"
echo "🐍 Python version: $(python --version)"

# Set PYTHONPATH to include the current directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "📦 PYTHONPATH: $PYTHONPATH"

# Run database migrations (if needed)
# alembic upgrade head

# Start the FastAPI app
echo "🌐 Starting uvicorn server..."
uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info

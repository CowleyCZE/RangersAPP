#!/bin/bash
# Quick Start Script for GDForge AI

set -e

echo "🎮 GDForge AI - Quick Start Setup"
echo "=================================="
echo ""

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✓ Docker found"
    echo ""
    echo "Starting with Docker..."
    docker-compose up
else
    echo "Docker not found. Starting manual setup..."
    echo ""
    
    # Backend setup
    echo "📦 Setting up Backend..."
    cd backend
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate || . venv/Scripts/activate
    pip install -r requirements.txt
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        echo ""
        echo "⚠️  .env file not found!"
        echo "Creating .env from template..."
        cp .env.example .env
        echo "📝 Please edit .env with your API keys!"
    fi
    
    cd ..
    
    # Frontend setup
    echo ""
    echo "🎨 Setting up Frontend..."
    cd frontend
    
    npm install
    
    cd ..
    
    echo ""
    echo "✓ Setup complete!"
    echo ""
    echo "To start the application:"
    echo "1. Backend: cd backend && source venv/bin/activate && python run.py"
    echo "2. Frontend: cd frontend && npm run dev"
fi

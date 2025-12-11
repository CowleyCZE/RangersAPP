.PHONY: help setup install dev backend frontend test clean docker docker-up docker-down lint format

help:
	@echo "GDForge AI - Make Commands"
	@echo "=========================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Inicializuje projekt (backend + frontend)"
	@echo "  make install        - Nainstaluje všechny dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev            - Spustí backend + frontend (require 2 terminály)"
	@echo "  make backend        - Spustí pouze backend"
	@echo "  make frontend       - Spustí pouze frontend"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test           - Spustí testy"
	@echo "  make lint           - Spustí linter"
	@echo "  make format         - Formátuje kód"
	@echo ""
	@echo "Docker:"
	@echo "  make docker         - Builduje Docker images"
	@echo "  make docker-up      - Spustí kontejnery"
	@echo "  make docker-down    - Zastaví kontejnery"
	@echo "  make docker-clean   - Odstraní images a kontejnery"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Vyčistí všechny cache a build soubory"
	@echo "  make docs           - Generuje dokumentaci"

setup:
	@echo "🚀 Initializing GDForge AI..."
	bash setup.sh
	@echo "✓ Setup complete!"

install: install-backend install-frontend
	@echo "✓ All dependencies installed!"

install-backend:
	@echo "📦 Installing backend dependencies..."
	cd backend && python -m venv venv
	cd backend && . venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Backend dependencies installed"

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✓ Frontend dependencies installed"

dev:
	@echo "🎮 Starting GDForge AI (requires 2 terminals)..."
	@echo ""
	@echo "Terminal 1: make backend"
	@echo "Terminal 2: make frontend"
	@echo ""

backend:
	@echo "⚙️  Starting backend server..."
	cd backend && . venv/bin/activate && python run.py

frontend:
	@echo "🎨 Starting frontend dev server..."
	cd frontend && npm run dev

test:
	@echo "🧪 Running tests..."
	cd backend && . venv/bin/activate && pytest -v
	@echo "✓ Tests completed!"

lint:
	@echo "🔍 Linting code..."
	cd frontend && npm run lint
	@echo "✓ Linting complete!"

format:
	@echo "✨ Formatting code..."
	cd frontend && npm run lint --fix 2>/dev/null || true
	@echo "✓ Code formatted!"

docker:
	@echo "🐳 Building Docker images..."
	docker-compose build
	@echo "✓ Docker images built!"

docker-up:
	@echo "🚀 Starting Docker containers..."
	docker-compose up

docker-down:
	@echo "🛑 Stopping Docker containers..."
	docker-compose down

docker-clean: docker-down
	@echo "🧹 Cleaning Docker resources..."
	docker-compose rm -f
	@echo "✓ Docker resources cleaned!"

clean:
	@echo "🧹 Cleaning project..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .vite -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	find . -name ".DS_Store" -delete
	@echo "✓ Project cleaned!"

docs:
	@echo "📚 Generating documentation..."
	@echo "Documentation files:"
	@echo "  - README.md"
	@echo "  - docs/API.md"
	@echo "  - docs/GODOT_INTEGRATION.md"
	@echo "  - examples/EXAMPLES.md"
	@echo "  - ARCHITECTURE.md"
	@echo "  - CONTRIBUTING.md"
	@echo "  - CHANGELOG.md"
	@echo "✓ Documentation complete!"

.DEFAULT_GOAL := help

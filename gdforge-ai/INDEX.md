# GDForge AI - Kompletní Projektový Index

## 📍 Lokace Projektu
```
/workspaces/RangersAPP/gdforge-ai/
```

---

## 📂 Projektová Struktura (Kompletní Index)

### 🔙 Backend (Python/FastAPI)

**Core Konfigurační Soubory:**
- `backend/app/main.py` - FastAPI aplikace s middleware
- `backend/app/core/config.py` - Settings a konfigurace
- `backend/app/core/exceptions.py` - Custom výjimky

**Service Layer:**
- `backend/app/services/llm_provider.py` - LLM abstrakce (OpenAI + Anthropic)
- `backend/app/services/gdscript_generator.py` - Code generation engine

**API Layer:**
- `backend/app/api/models.py` - Pydantic request/response modely
- `backend/app/api/routes.py` - REST API endpoints (3x)

**Ostatní:**
- `backend/app/__init__.py` - Package init
- `backend/app/services/__init__.py` - Services init
- `backend/app/api/__init__.py` - API init
- `backend/app/core/__init__.py` - Core init

**Testy:**
- `backend/tests/test_api.py` - Unit testy
- `backend/tests/__init__.py` - Tests init

**Spouštěcí Body:**
- `backend/run.py` - Entry point pro spuštění serveru

**Konfigurace:**
- `backend/requirements.txt` - Python dependencies
- `backend/.env.example` - Environment variables template
- `backend/.gitignore` - Git ignore rules
- `backend/Dockerfile` - Docker image
- `backend/README.md` - Backend dokumentace

---

### 🎨 Frontend (React/TypeScript)

**Komponenty:**
- `frontend/src/components/Header.tsx` - Top navigation bar
- `frontend/src/components/PromptInput.tsx` - Prompt textarea
- `frontend/src/components/CodeOutput.tsx` - Code preview
- `frontend/src/components/Examples.tsx` - Example prompts

**Services:**
- `frontend/src/services/api.ts` - API client
- `frontend/src/services/__init__.ts` - Services init

**State Management:**
- `frontend/src/store.ts` - Zustand store

**Core:**
- `frontend/src/App.tsx` - Root component
- `frontend/src/main.tsx` - React entry point
- `frontend/src/index.css` - Global styles
- `frontend/src/__init__.ts` - Frontend init

**Public Assets:**
- `frontend/public/index.html` - HTML template

**Konfigurace:**
- `frontend/package.json` - NPM dependencies
- `frontend/tsconfig.json` - TypeScript config
- `frontend/tsconfig.node.json` - Node TypeScript config
- `frontend/vite.config.ts` - Vite build config
- `frontend/tailwind.config.js` - Tailwind CSS config
- `frontend/.postcssrc.cjs` - PostCSS config
- `frontend/.env.example` - Environment variables
- `frontend/.gitignore` - Git ignore rules
- `frontend/Dockerfile` - Docker image
- `frontend/README.md` - Frontend dokumentace

---

### 📚 Dokumentace

**Hlavní Dokumenty:**
- `README.md` - Main readme v kořeni projektu
- `gdforge-ai/README.md` - Hlavní projekt README
- `gdforge-ai/QUICK_REFERENCE.md` - Quick reference guide

**Technická Dokumentace:**
- `gdforge-ai/ARCHITECTURE.md` - Technická architektura
- `gdforge-ai/PROJECT_SUMMARY.md` - Kompletní projekt overview
- `gdforge-ai/docs/API.md` - REST API reference
- `gdforge-ai/docs/GODOT_INTEGRATION.md` - Godot integrační průvodce

**Developer Docs:**
- `gdforge-ai/CONTRIBUTING.md` - Contributing guidelines
- `gdforge-ai/CHANGELOG.md` - Version history
- `gdforge-ai/DEPLOYMENT.md` - Deployment guides

**Příklady:**
- `gdforge-ai/examples/EXAMPLES.md` - 10+ příkladů promptů

---

### 🛠️ DevOps & Konfigurace

**Docker:**
- `gdforge-ai/docker-compose.yml` - Multi-container orchestration
- `gdforge-ai/backend/Dockerfile` - Backend image
- `gdforge-ai/frontend/Dockerfile` - Frontend image

**Skripty & Automatizace:**
- `gdforge-ai/Makefile` - Development commands
- `gdforge-ai/setup.sh` - Quick setup script
- `PROJECT_REPORT.sh` - Project report script

**Git:**
- `gdforge-ai/.gitignore` - Root .gitignore
- `gdforge-ai/backend/.gitignore` - Backend .gitignore
- `gdforge-ai/frontend/.gitignore` - Frontend .gitignore

**Environment:**
- `gdforge-ai/backend/.env.example` - Backend config template
- `gdforge-ai/frontend/.env.example` - Frontend config template

---

## 🚀 Jak Začít

### 1. Příprava
```bash
cd /workspaces/RangersAPP/gdforge-ai
bash setup.sh
```

### 2. Konfigurace
```bash
cd backend
cp .env.example .env
# Edit .env with your API key
```

### 3. Spuštění Backend
```bash
cd backend
source venv/bin/activate
python run.py
```

### 4. Spuštění Frontend
```bash
cd frontend
npm run dev
```

### 5. Navštívit
```
http://localhost:5173
```

---

## 📊 Soubory dle Typu

### Python Soubory (.py)
| Soubor | Obsah |
|--------|-------|
| app/main.py | FastAPI app factory |
| app/core/config.py | Settings |
| app/core/exceptions.py | Custom exceptions |
| app/services/llm_provider.py | LLM integration |
| app/services/gdscript_generator.py | Code generation |
| app/api/models.py | Pydantic models |
| app/api/routes.py | REST endpoints |
| run.py | Entry point |
| tests/test_api.py | Tests |

### TypeScript/React Soubory (.tsx, .ts)
| Soubor | Obsah |
|--------|-------|
| App.tsx | Root component |
| main.tsx | React entry |
| store.ts | Zustand |
| services/api.ts | HTTP client |
| components/Header.tsx | Top bar |
| components/PromptInput.tsx | Input |
| components/CodeOutput.tsx | Output |
| components/Examples.tsx | Examples |

### Dokumentace (.md)
| Soubor | Obsah |
|--------|-------|
| README.md | Main intro |
| QUICK_REFERENCE.md | Cheat sheet |
| ARCHITECTURE.md | Tech details |
| docs/API.md | API reference |
| docs/GODOT_INTEGRATION.md | Godot guide |
| examples/EXAMPLES.md | Prompt examples |
| CONTRIBUTING.md | Dev guidelines |
| DEPLOYMENT.md | Deploy guides |
| CHANGELOG.md | Version history |

### Konfigurace (.json, .yml, .js)
| Soubor | Obsah |
|--------|-------|
| docker-compose.yml | Docker setup |
| Makefile | Dev commands |
| package.json | NPM deps |
| tsconfig.json | TypeScript |
| vite.config.ts | Build config |
| tailwind.config.js | Tailwind |

---

## 📈 Statistika Projektu

```
Celkem souborů:           60+
Python soubory:           15
TypeScript soubory:       10
Dokumentace (Markdown):   10
JSON/Config:              8
Docker:                   3
Bash/Scripts:             2

Celkové řádky kódu:       ~2,300
Backend (Python):         ~1,500
Frontend (React/TS):      ~800

Dokumentace:              100+ stran
Příklady:                 10+
```

---

## 🔗 Klíčové Linky

### Porty
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### GitHub
- **Repository**: https://github.com/CowleyCZE/RangersAPP
- **Issues**: https://github.com/CowleyCZE/RangersAPP/issues
- **Discussions**: https://github.com/CowleyCZE/RangersAPP/discussions

---

## 📝 API Endpoints

```
GET  /api/health              - Health check
POST /api/generate            - Generuj Installer.gd
POST /api/generate/json       - Generuj Blueprint
```

---

## 🎯 Důležité Příkazy

```bash
# Development
make setup              # Setup projekt
make backend            # Run backend
make frontend           # Run frontend
make test               # Run tests
make lint               # Run linter
make format             # Format code

# Docker
make docker             # Build images
make docker-up          # Start containers
make docker-down        # Stop containers

# Cleanup
make clean              # Clean caches
```

---

## 📦 Dependencies

### Backend
```
FastAPI 0.104.1
Pydantic 2.5.0
OpenAI 1.3.8
Anthropic 0.7.8
Jinja2 3.1.2
Uvicorn 0.24.0
```

### Frontend
```
React 18.2.0
TypeScript 5.2.2
Zustand 4.4.1
Axios 1.6.2
Tailwind CSS 3.3.6
Vite 5.0.7
```

---

## 🚀 Deployment Paths

1. **Local Development**
   - `backend/run.py`
   - `npm run dev`

2. **Docker**
   - `docker-compose up`

3. **Production (Heroku)**
   - `git push heroku main`

4. **Production (AWS)**
   - See DEPLOYMENT.md

5. **Production (GCP)**
   - See DEPLOYMENT.md

---

## 🧪 Testing

```bash
# Backend
pytest backend/tests/ -v

# Frontend
npm run lint
npm run type-check
```

---

## 📚 Kde Hledat Konkrétní Info

| Otázka | Kde najít |
|--------|-----------|
| Jak spustit? | QUICK_REFERENCE.md |
| Jak to funguje? | ARCHITECTURE.md |
| Godot integrace? | docs/GODOT_INTEGRATION.md |
| API reference? | docs/API.md |
| Příklady promptů? | examples/EXAMPLES.md |
| Jak deploy? | DEPLOYMENT.md |
| Jak přispět? | CONTRIBUTING.md |
| Backend specifika? | backend/README.md |
| Frontend specifika? | frontend/README.md |

---

## 🎓 Learning Path

1. **Úvod**: README.md
2. **Quick Start**: QUICK_REFERENCE.md
3. **Příklady**: examples/EXAMPLES.md
4. **Architektura**: ARCHITECTURE.md
5. **API Details**: docs/API.md
6. **Contributing**: CONTRIBUTING.md

---

## ✅ Checklist Onboarding

- [ ] Přečetl jsem README.md
- [ ] Nainstaloval jsem závislosti (`make setup`)
- [ ] Konfiguroval jsem API klíče (`.env`)
- [ ] Spustil jsem backend (`make backend`)
- [ ] Spustil jsem frontend (`make frontend`)
- [ ] Navštívil jsem http://localhost:5173
- [ ] Vygeneroval jsem svůj první skript
- [ ] Přečetl jsem ARCHITECTURE.md
- [ ] Podíval jsem se na CONTRIBUTING.md
- [ ] Jsem připraven přispívat!

---

## 🎉 Hotovo!

Projekt GDForge AI je kompletně vytvořený a připraven pro:

- ✅ Vývoj
- ✅ Testování
- ✅ Produkční nasazení
- ✅ Komunitní příspěvky

**Začni teď:**
```bash
cd gdforge-ai
bash setup.sh
```

---

**Verze**: 0.1.0  
**Status**: ✅ Production-Ready  
**Licence**: MIT  
**Aktualizováno**: 11. prosince 2024

🚀 **Šťastného vývoje!** 🎮✨

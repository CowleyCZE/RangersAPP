# GDForge AI - Project Structure Overview

```
gdforge-ai/
│
├── backend/                          # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py              # Package init
│   │   ├── main.py                  # FastAPI application
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # Settings & configuration
│   │   │   └── exceptions.py        # Custom exceptions
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── llm_provider.py      # LLM abstraction (OpenAI/Anthropic)
│   │   │   └── gdscript_generator.py # GDScript generation logic
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # Pydantic models
│   │   │   └── routes.py            # API endpoints
│   │   └── templates/               # Jinja2 templates (future)
│   ├── tests/
│   │   └── test_api.py              # API tests
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Docker image
│   ├── .env.example                 # Environment template
│   ├── .gitignore
│   └── run.py                       # Entry point
│
├── frontend/                         # React + TypeScript Frontend
│   ├── src/
│   │   ├── main.tsx                 # React entry point
│   │   ├── App.tsx                  # Main component
│   │   ├── index.css                # Global styles
│   │   ├── store.ts                 # Zustand state management
│   │   ├── components/
│   │   │   ├── Header.tsx           # Top navigation
│   │   │   ├── PromptInput.tsx      # Prompt textarea & controls
│   │   │   ├── CodeOutput.tsx       # Generated code display
│   │   │   └── Examples.tsx         # Example prompts
│   │   └── services/
│   │       └── api.ts              # API client
│   ├── public/
│   │   └── index.html              # HTML template
│   ├── package.json                # NPM dependencies
│   ├── tsconfig.json               # TypeScript config
│   ├── vite.config.ts              # Vite config
│   ├── tailwind.config.js          # Tailwind CSS
│   ├── Dockerfile
│   ├── .env.example
│   ├── .gitignore
│   └── .postcssrc.cjs              # PostCSS config
│
├── docs/                            # Documentation
│   ├── API.md                       # API Reference
│   └── GODOT_INTEGRATION.md         # Godot setup guide
│
├── examples/                        # Usage examples
│   └── EXAMPLES.md                  # Example prompts
│
├── README.md                        # Main documentation
├── docker-compose.yml               # Docker orchestration
├── setup.sh                         # Quick setup script
└── .gitignore                      # Git ignore rules

```

## Key Technologies

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **OpenAI/Anthropic API** - LLM integration
- **Jinja2** - Template rendering for GDScript

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Zustand** - State management
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Vite** - Build tool

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Architecture Patterns

### Services Layer
- `llm_provider.py` - Abstract LLM interface with multiple implementations
- `gdscript_generator.py` - Template-based code generation

### API Design
- RESTful endpoints in `api/routes.py`
- Pydantic models for validation in `api/models.py`
- Global exception handling via FastAPI middleware

### Frontend State
- Zustand store (`store.ts`) for reactive state
- API service (`services/api.ts`) for HTTP communication
- Component composition for reusable UI

## Data Flow

```
User Input (UI)
    ↓
PromptInput Component
    ↓
API Service (axios POST)
    ↓
[Backend] /api/generate endpoint
    ↓
LLM Provider (OpenAI/Anthropic)
    ↓
Blueprint JSON
    ↓
GDScript Generator (Jinja2)
    ↓
Installer.gd (EditorScript)
    ↓
Download or View
    ↓
User imports to Godot
    ↓
Godot Editor runs File → Run
    ↓
✨ Scenes & Scripts Created ✨
```

## Extensibility

### Adding New LLM Providers
1. Create class inheriting from `LLMProvider`
2. Implement `analyze_prompt()` method
3. Register in `get_llm_provider()` function

### Adding New Node Types
1. Extend Jinja2 templates in `gdscript_generator.py`
2. Add support in LLM prompt engineering

### Custom UI Components
1. Add React component to `components/`
2. Import in `App.tsx`
3. Use Zustand store for state

## Configuration Management

- Environment variables via `.env` file
- Pydantic `Settings` class in `core/config.py`
- Per-environment configuration support

## Testing

- Basic API tests in `backend/tests/test_api.py`
- Run with: `pytest backend/tests/`

---

**This architecture is designed for scalability, maintainability, and ease of contribution.**

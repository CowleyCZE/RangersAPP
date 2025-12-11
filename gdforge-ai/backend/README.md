# GDForge AI - Backend

Python FastAPI backend pro GDForge AI.

## Struktura Projektu

```
app/
├── __init__.py
├── main.py               # FastAPI aplikace
├── core/
│   ├── config.py         # Settings & configuration
│   └── exceptions.py     # Custom exceptions
├── services/
│   ├── llm_provider.py   # LLM abstraction
│   └── gdscript_generator.py # Code generation
├── api/
│   ├── models.py         # Pydantic models
│   ├── routes.py         # API endpoints
│   └── __init__.py
└── templates/            # Jinja2 (future)

tests/
└── test_api.py

requirements.txt
run.py                   # Entry point
```

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` a vyplňte API klíče:

```bash
cp .env.example .env
```

Vyžadované:
- `OPENAI_API_KEY` nebo `ANTHROPIC_API_KEY`

## Development

```bash
python run.py
```

Backend poběží na http://localhost:8000

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
pytest -v
```

## Architecture

### Services

**LLM Provider** (`services/llm_provider.py`):
- Abstract interface `LLMProvider`
- Implementation: `OpenAIProvider`, `AnthropicProvider`
- Lze snadno přidat nové providery

**GDScript Generator** (`services/gdscript_generator.py`):
- Generuje Installer.gd z blueprintu
- Jinja2 templates pro flexibilitu
- Validace vstupů

### API Routes

```
GET    /api/health              - Health check
POST   /api/generate            - Generate Installer.gd
POST   /api/generate/json       - Generate blueprint
```

## Core Configuration

Settings v `app/core/config.py`:

```python
class Settings(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    llm_provider: str = "openai"
    llm_model: str = "gpt-4-turbo-preview"
    debug: bool = False
    cors_origins: list = [...]
```

## Error Handling

Custom exceptions v `app/core/exceptions.py`:

```python
class GDForgeException(Exception)
class LLMException(GDForgeException)
class GenerationException(GDForgeException)
class ValidationException(GDForgeException)
```

## Adding New Features

### New LLM Provider

1. Vytvořte třídu v `services/llm_provider.py`:

```python
class MyProvider(LLMProvider):
    async def analyze_prompt(self, prompt: str) -> dict:
        # Implementation
        pass
```

2. Zaregistrujte v `get_llm_provider()`:

```python
def get_llm_provider() -> LLMProvider:
    if provider == "my_provider":
        return MyProvider()
```

### New API Endpoint

1. Vytvořte route v `api/routes.py`:

```python
@router.post("/my-endpoint", response_model=MyResponse)
async def my_endpoint(request: MyRequest):
    # Implementation
    return MyResponse(...)
```

2. Přidejte modely v `api/models.py`:

```python
class MyRequest(BaseModel):
    param: str = Field(..., description="...")

class MyResponse(BaseModel):
    result: str = Field(...)
```

## Dependencies

- **fastapi** - Web framework
- **pydantic** - Data validation
- **openai** - OpenAI API client
- **anthropic** - Anthropic API client
- **jinja2** - Template rendering

Viz `requirements.txt` pro kompletní seznam.

## Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
DEBUG=false
HOST=0.0.0.0
PORT=8000
```

## Docker

```bash
docker build -t gdforge-ai-backend .
docker run -p 8000:8000 gdforge-ai-backend
```

## Troubleshooting

**API Key Error:**
```
LLM Error (openai): OpenAI API key not configured
```
→ Zkontrolujte `.env` soubor

**CORS Error:**
```
Access to XMLHttpRequest blocked by CORS
```
→ Zkontrolujte `CORS_ORIGINS` v config

**JSON Decode Error:**
```
InvalidJSON response: {...}
```
→ LLM API vrátil nevalidní JSON, zkuste znovu

## Performance Tips

- Asynchronní API calls s `async/await`
- Template caching (Jinja2)
- Connection pooling pro HTTP requests
- LRU cache pro settings

## Contributing

Viz `CONTRIBUTING.md` pro guidelines.

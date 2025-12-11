# Contributing to GDForge AI

Děkuji za zájem o přispívání! Toto je open-source projekt a vítáme všechny formy příspěvků.

## 🚀 Jak Začít

### 1. Fork a Clone

```bash
git clone https://github.com/YOUR_USERNAME/gdforge-ai.git
cd gdforge-ai
```

### 2. Setup Development Environment

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend (v novém terminálu)
cd frontend
npm install
```

### 3. Configure API Keys

```bash
# Backend
cd backend
cp .env.example .env
# Edit .env with your OpenAI/Anthropic keys
```

## 💻 Development Workflow

### Backend Development

```bash
cd backend
source venv/bin/activate
python run.py
```

Backend poběží na `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Development

```bash
cd frontend
npm run dev
```

Frontend poběží na `http://localhost:5173`

### Spuštění Testů

```bash
# Backend tests
cd backend
pytest

# Frontend lint
cd frontend
npm run lint
```

## 📝 Typy Příspěvků

### Bug Reports
- Otevřete Issue s popisem
- Přidejte steps to reproduce
- Ověřte, že bug nebyl hlášen

### Feature Requests
- Otevřete Discussion
- Vysvětlete use case
- Čekejte feedback

### Code Contributions
1. Otevřete Issue nebo Discussion
2. Počkejte na feedback
3. Vytvořte feature branch: `git checkout -b feature/my-feature`
4. Commitujte se jasným popisem
5. Push do fork a otevřete Pull Request

## 🎯 Development Guidelines

### Code Style

**Python:**
- Používáme PEP 8
- Type hints jsou povinné
- Docstrings pro všechny public funkce

```python
def analyze_prompt(self, prompt: str) -> dict:
    """Analyzuje prompt a vrací strukturu.
    
    Args:
        prompt: Zadání v přirozeném jazyce
        
    Returns:
        dict: Strukturovaný plán
        
    Raises:
        LLMException: Pokud je chyba LLM API
    """
    pass
```

**TypeScript/React:**
- ESLint + Prettier
- Componenty jsou funkční s hooks
- Propery mají type annotations

```typescript
interface PromptInputProps {
  onGenerate: (prompt: string) => Promise<void>
  isLoading?: boolean
}

export const PromptInput: React.FC<PromptInputProps> = ({
  onGenerate,
  isLoading = false
}) => {
  // ...
}
```

### Commit Messages

Používejte konvenci:
```
type(scope): subject

description (if needed)
```

Příklady:
```
feat(llm): add Claude 3 support
fix(generator): correct node initialization order
docs(api): update endpoint documentation
refactor(frontend): simplify state management
test(backend): add LLM provider tests
```

### Git Branches

Používejte prefixes:
- `feature/` - Nová funkce
- `fix/` - Oprava bugu
- `docs/` - Dokumentace
- `refactor/` - Refaktorování
- `test/` - Testy

### Pull Requests

Template:

```markdown
## Popis
Stručný popis změn.

## Typ
- [ ] Bug fix
- [ ] Nová funkce
- [ ] Breaking change
- [ ] Documentation update

## Testing
Jak jste testovali?

## Checklist
- [ ] Kod splňuje style guide
- [ ] Přidány nové testy
- [ ] Dokumentace updatována
- [ ] Žádné warning messages
```

## 🏗️ Architecture Guidelines

### Přidání Nového LLM Provideru

1. Vytvořte novou třídu v `backend/app/services/llm_provider.py`:

```python
class MyLLMProvider(LLMProvider):
    async def analyze_prompt(self, prompt: str) -> dict:
        # Implementation
        pass
```

2. Zaregistrujte v `get_llm_provider()`:

```python
def get_llm_provider() -> LLMProvider:
    if provider == "my_provider":
        return MyLLMProvider()
```

3. Updatujte config a dokumentaci

### Přidání Nového Generátoru

1. Rozšiřte `GDScriptGenerator` v `backend/app/services/gdscript_generator.py`
2. Updatujte Jinja2 templates
3. Updatujte blueprint strukturu v LLM prompts

### Frontend Komponenty

Všechny komponenty by měly:
- Mít Props interface
- Používat Zustand store pro state
- Mít TypeScript types
- Obsahovat JSDoc comments

## 📚 Dokumentace

Při přidání features, updatujte:
- API dokumentaci: `docs/API.md`
- Godot guide: `docs/GODOT_INTEGRATION.md`
- README s příklady
- ARCHITECTURE.md pro komplexní změny

## 🚨 Reporting Issues

Když hlásíte bug, uveďte:
1. Verzi aplikace
2. OS a verzi
3. Steps to reproduce
4. Expected vs actual behavior
5. Logs/error messages

Příklad:

```
**Verze:** 0.1.0
**OS:** Ubuntu 22.04
**LLM:** OpenAI GPT-4

**Problém:** Skript se nevytvoří když prompt obsahuje UTF-8 znaky

**Kroky:**
1. Zadejte prompt: "Vytvoř UI s "Hello 🎮 World""
2. Klikněte "Vygeneruj"
3. Chyba nastane v bodě...

**Chyba:**
```
UnicodeDecodeError: ...
```
```

## 🤝 Review Process

- Minimálně 1 review před merge
- CI/CD pipeline musí projít
- Při velkých změnách čekejte 2 reviews
- Maintainers mají finální slovo

## 📋 Roadmap

Plánované features:
- [ ] Fine-tuned models pro domény (2D platformers, RPG, atd)
- [ ] Godot plugin extension
- [ ] Collaborative prompt engineering
- [ ] Model caching & optimization
- [ ] Custom blueprint templating
- [ ] Web3 integration (optional)

## 💬 Komunikace

- **Issues:** Bug reports a feature requests
- **Discussions:** Náměty a otázky
- **Pull Requests:** Kód contributions
- **Email:** kontakt@gdforge.ai (TBA)

## 📄 Licence

Přispíváním souhlasíte, že váš kód bude pod MIT licencí.

---

**Děkujeme za přispívání!** 🎉

Máte otázky? Otevřete Discussion nebo Issue.

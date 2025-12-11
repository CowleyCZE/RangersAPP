# Changelog

Všechny pozoruhodné změny v tomto projektu budou dokumentovány v tomto souboru.

## [0.1.0] - 2024-12-11

### ✨ Přidáno

#### Core Features
- **Text-to-Engine Automatizace**: Převod přirozeného jazyka do GDScript EditorScriptů
- **AI-Powered Analysis**: Integrace s OpenAI GPT-4 a Anthropic Claude
- **Zero-Dependency Generation**: Vygenerované instalační skripty běží bez dalších pluginů
- **Idempotent Installation**: Bezpečné opakované spuštění bez poškození projektu

#### Backend
- FastAPI REST API s endpoints:
  - `GET /api/health` - Health check
  - `POST /api/generate` - Generování GDScript instalačního skriptu
  - `POST /api/generate/json` - Generování samotného blueprintu
- Abstraktní LLM interface s podporou:
  - OpenAI GPT-4
  - Anthropic Claude 3
- GDScript generátor s Jinja2 templates
- Validace a error handling
- Pydantic modely pro request/response

#### Frontend
- React + TypeScript webové rozhraní
- Zustand state management
- Prompt input textarea s příklady
- Real-time code preview
- Tlačítko pro stažení skriptu
- Responsive design (Tailwind CSS)
- API client s axios

#### Documentation
- Kompletní README s installation guides
- API dokumentace (`docs/API.md`)
- Godot integrační průvodce (`docs/GODOT_INTEGRATION.md`)
- Příklady promptů (`examples/EXAMPLES.md`)
- Architektura (`ARCHITECTURE.md`)
- Contributing guidelines (`CONTRIBUTING.md`)

#### DevOps
- Docker & Docker Compose setup
- Multi-container orchestration
- Environment-based configuration

### 🔧 Changed

- N/A (První release)

### 🐛 Fixed

- N/A (První release)

### 🚀 Performance

- Template-based code generation pro maximální rychlost
- Asynchronní LLM API calls

### 📋 Known Limitations

- Zatím bez authentication
- Bez rate limiting (bude přidáno v 0.2.0)
- Pouze textový prompt input (drag-drop bude v 0.2.0)
- Godot 4.0+ vyžadován (kompatibilita s GDScript 2.0)

## [Unreleased]

### Plánované Features (0.2.0)
- [ ] Godot Editor Plugin extension
- [ ] Domain-specific model fine-tuning
- [ ] Collaborative prompt engineering
- [ ] Blueprint caching & optimization
- [ ] Custom template system
- [ ] Multi-select LLM providers
- [ ] Prompt versioning & history
- [ ] Export to Godot Asset Library
- [ ] WebSocket real-time streaming
- [ ] GitHub Actions integration

### Plánované Features (0.3.0)
- [ ] Visual Blueprint Editor
- [ ] Drag-drop template builder
- [ ] Team collaboration (Figma-style)
- [ ] AI-powered code review
- [ ] Performance optimization suggestions
- [ ] Cloud deployment helpers
- [ ] Mobile app (React Native)

### Plánované Features (0.4.0+)
- [ ] 3D asset generation
- [ ] Physics simulation setup
- [ ] Audio integration
- [ ] Networking setup templates
- [ ] Save/load Godot project presets
- [ ] Subscription model s premium features

## Migrace z Předchozích Verzí

N/A (První release)

## Support

- **Issues**: https://github.com/CowleyCZE/RangersAPP/issues
- **Discussions**: https://github.com/CowleyCZE/RangersAPP/discussions
- **Email**: support@gdforge.ai (TBA)

---

**Format:** Tento changelog následuje [Keep a Changelog](https://keepachangelog.com/) konvenci.

**Versionování:** Projekt používá [Semantic Versioning](https://semver.org/).

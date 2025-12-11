# GDForge AI - Quick Reference

## 🚀 Spuštění

### Backend (Port 8000)
```bash
cd backend
source venv/bin/activate
python run.py
```

### Frontend (Port 5173)
```bash
cd frontend
npm run dev
```

### Docker
```bash
docker-compose up
```

## 📚 Dokumentace

| Dokument | Obsah | Pro |
|----------|-------|-----|
| [README.md](README.md) | Přehled & setup | Všichni |
| [docs/API.md](docs/API.md) | REST API | Vývojáři |
| [docs/GODOT_INTEGRATION.md](docs/GODOT_INTEGRATION.md) | Godot integrace | Game Dev |
| [examples/EXAMPLES.md](examples/EXAMPLES.md) | 10+ příkladů | Všichni |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technické detaily | Vývojáři |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributing guide | Přispěvatelé |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deployment guides | DevOps |

## 🔗 Klíčové Linky

| Prostředek | URL |
|------------|-----|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **GitHub** | https://github.com/CowleyCZE/RangersAPP |

## 📝 API Endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# Generate installer
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Vytvoř level s tilemapou",
    "project_root": "scenes",
    "format": "gdscript"
  }'

# Generate blueprint
curl -X POST http://localhost:8000/api/generate/json \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Inventář se 4 sloupci"}'
```

## 🛠️ Development Commands

```bash
# Setup (first time)
make setup

# Install dependencies
make install

# Run backend
make backend

# Run frontend
make frontend

# Run tests
make test

# Format code
make format

# Clean cache
make clean

# Docker
make docker-up
make docker-down
```

## 📁 Important Files

```
backend/
├── app/main.py              # FastAPI app
├── app/services/llm_provider.py    # LLM abstraction
├── app/services/gdscript_generator.py # Code generation
└── requirements.txt         # Python dependencies

frontend/
├── src/App.tsx              # Root component
├── src/components/          # React components
├── src/services/api.ts      # API client
└── package.json             # NPM dependencies
```

## 🔑 Configuration

### Backend (.env)
```env
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
DEBUG=false
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 📊 Architecture Overview

```
User Input
    ↓
[Frontend] React UI
    ↓
[Backend] FastAPI
    ↓
[LLM] OpenAI/Anthropic
    ↓
[Generator] Jinja2 Templates
    ↓
[Output] Installer.gd
    ↓
[Download] User
    ↓
[Godot] File → Run
    ↓
✨ Hotovo!
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend lint
cd frontend
npm run lint

# Type check
npm run type-check
```

## 🐛 Troubleshooting

### Backend
```bash
# Check health
curl http://localhost:8000/api/health

# View logs
docker logs gdforge-backend

# Check API key
cat backend/.env | grep API_KEY
```

### Frontend
```bash
# Clear cache
rm -rf frontend/node_modules frontend/dist

# Reinstall
cd frontend && npm install

# Rebuild
npm run build
```

## 🚀 Deployment

### Local
```bash
make setup
make backend &
make frontend &
```

### Docker
```bash
docker-compose up -d
```

### Production
Viz [DEPLOYMENT.md](DEPLOYMENT.md) pro detaily:
- AWS EC2
- Heroku
- Google Cloud Run
- DigitalOcean
- Docker Hub

## 💡 Example Prompts

1. **Level s tilemapou**
   ```
   Vytvoř level pro plošinovku. TileMap, hráč, kamera, parallax.
   ```

2. **Inventář**
   ```
   UI panel se 4x GridContainer, Inventory.gd skript.
   ```

3. **3D scéna**
   ```
   3D Node3D, osvětlení, mesh, kamera s rotací.
   ```

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Docs**: Viz dokumentační soubory

## 🔄 Update & Maintenance

```bash
# Pull latest
git pull origin main

# Update dependencies
cd backend && pip install -r requirements.txt -U
cd frontend && npm update

# Restart services
docker-compose restart
```

## 📄 Licence

MIT - Volně použitelný

## 🎯 Next Steps

1. Setup project: `make setup`
2. Run backend: `make backend`
3. Run frontend: `make frontend`
4. Visit: http://localhost:5173
5. Generate your first script! ✨

---

**Version:** 0.1.0  
**Last Updated:** 2024-12-11  
**Status:** ✅ Ready for Use

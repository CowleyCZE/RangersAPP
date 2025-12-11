# GDForge AI - Godot Infrastructure as Code

**GDForge AI** je revoluční nástroj pro text-to-engine automatizaci v Godot 4. Místo ručního klikání v editoru, definujete záměr v přirozeném jazyce a aplikace vygeneruje kompletní instalační skript (EditorScript), který automaticky vytvoří scény, skripty a jejich propojení.

## 🎯 Hlavní Charakteristiky

- **🤖 AI-Powered**: Integruje OpenAI GPT-4 nebo Anthropic Claude pro analýzu vašeho promptu
- **⚡ Zero-Dependency**: Vygenerované instalační skripty běží přímo v Godot Editoru bez dalších pluginů
- **🔄 Idempotentní**: Bezpečně opakovaně spustitelné bez duplikace nebo poškození projektu
- **🎨 Full-Stack**: Generuje scény, skripty, resources a automaticky propojuje signály
- **📦 Přenositelný**: Uložené prompty lze znovu použít v různých projektech

## 📋 Obsah

- [Instalace](#instalace)
- [Použití](#použití)
- [Architektura](#architektura)
- [API Dokumentace](#api-dokumentace)
- [Příklady](#příklady)
- [Godot Integrace](#godot-integrace)

## 🚀 Instalace

### Požadavky

- Python 3.10+
- Node.js 18+ (pro frontend)
- Godot 4.0+ (pro spuštění vygenerovaných skriptů)
- OpenAI API klíč nebo Anthropic API klíč

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Vytvořte `.env` soubor:

```env
OPENAI_API_KEY=sk-...
# nebo
ANTHROPIC_API_KEY=sk-ant-...

LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
```

Spusťte backend:

```bash
python run.py
# Backend bude běžet na http://localhost:8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Frontend bude běžet na http://localhost:5173
```

## 💻 Použití

### Web Rozhraní

1. Otevřete http://localhost:5173
2. Zadejte popis vašeho projektu v přirozeném jazyce
3. Klikněte "Vygeneruj Skript"
4. Stáhněte si vygenerovaný `setup_*.gd` soubor

### Příklad Promptu

```
Vytvoř mi level pro plošinovku. Chci scénu 'Level1' s TileMapou, 
hráčem (CharacterBody2D), kamerou která ho sleduje, a parallax 
pozadím. Hráč má mít základní pohybový skript s WASD kontrolou.
```

### Godot Integrace

1. **Stáhni si soubor** `setup_Level1.gd`
2. **Přetáhni do projektu** do libovolného adresáře (např. `res://scripts/`)
3. **Spusť v editoru**:
   - Výběr souboru v FileSystem
   - Ctrl+Shift+F5 nebo File → Run
   - Během sekund se vytvoří všechny scény a skripty!

## 🏗️ Architektura

```
gdforge-ai/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── core/           # Config, exceptions
│   │   ├── services/       # LLM & Generator
│   │   ├── api/            # REST endpoints
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── run.py
├── frontend/               # React + TypeScript UI
│   ├── src/
│   │   ├── components/     # UI komponenty
│   │   ├── services/       # API klient
│   │   └── store.ts        # Zustand store
│   └── package.json
├── docs/                   # Dokumentace
├── examples/               # Příklady promptů
└── docker-compose.yml
```

### Datový Tok

```
User Prompt
    ↓
[Web Frontend] → POST /api/generate → [FastAPI Backend]
    ↓
[LLM Analyzer] (GPT-4 / Claude)
    ↓
[Blueprint Parser] → Strukturovaný JSON
    ↓
[GDScript Generator] → Jinja2 Templates
    ↓
Installer.gd (EditorScript)
    ↓
[Download] → User Machine
    ↓
[Godot Editor] → Ctrl+Shift+F5
    ↓
✨ Hotovo! Scény a Skripty Vytvořeny ✨
```

## 📚 API Dokumentace

### Health Check

```bash
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "llm_provider": "openai"
}
```

### Generate Installer

```bash
POST /api/generate
Content-Type: application/json

{
  "prompt": "Vytvoř mi level...",
  "project_root": "scenes",
  "format": "gdscript"
}
```

Response:
```json
{
  "success": true,
  "installer_code": "@tool\nextends EditorScript\n...",
  "blueprint": { ... },
  "filename": "setup_Level1.gd",
  "message": "Successfully generated installer for 1 scenes"
}
```

### Generate Blueprint (JSON Only)

```bash
POST /api/generate/json

{
  "prompt": "Vytvoř mi..."
}
```

Response:
```json
{
  "success": true,
  "blueprint": {
    "scenes": [...],
    "scripts": [...],
    "resources": [...],
    "signals": [...]
  }
}
```

## 🎓 Příklady

### 1. Inventář Systém

**Prompt:**
```
Potřebuji Inventář systém. Scéna 'Inventory.tscn' jako UI panel 
uprostřed obrazovky. Obsahuje GridContainer se 4 sloupci. Chci 
k tomu skript 'Inventory.gd', který má pole 'items' a funkci 
'add_item(name: String)'.
```

**Co se vytvoří:**
- ✅ `res://Inventory.tscn` - Scéna s UI layout
- ✅ `res://Inventory.gd` - Skript s item managementem
- ✅ Propojení skriptu na scénu

### 2. 3D Scéna

**Prompt:**
```
Vytvoř 3D scénu 'MainScene' s Node3D rootem. Přidej osvětlení 
(DirectionalLight3D), mesh (CSGBox3D) s StandardMaterial3D 
a kameru která se otáčí okolo objektu.
```

**Co se vytvoří:**
- ✅ 3D scéna s osvětlením
- ✅ Mesh objekty s materiály
- ✅ Kamera s pohybovým skriptem

### 3. Hlavní Menu

**Prompt:**
```
Vytvoř hlavní menu. Scéna 'MainMenu.tscn' s VBoxContainer 
a tlačítky: Start Game, Settings, Credits, Quit. Každé 
tlačítko má signál connected na handler.
```

**Co se vytvoří:**
- ✅ UI menu scéna
- ✅ Tlačítka s signály
- ✅ Handlery připravené k implementaci

Další příklady najdete v [`/examples`](./examples).

## 🔗 Godot Integrace

### Jak Funguje EditorScript

Vygenerovaný skript je `@tool extends EditorScript` což znamená:

1. **@tool** - Běží i v editoru (ne jen v runtime)
2. **extends EditorScript** - Má přístup k _run() metodě
3. **Automatické vytvoření** - _run() se spustí když vybereš File → Run

```gdscript
@tool
extends EditorScript

func _run():
    # Vytvoří adresáře
    var dir = DirAccess.open("res://")
    dir.make_dir_recursive("res://scenes")
    
    # Vytvoří scény
    _create_scene_0("res://")
    
    # Vytvoří skripty
    _create_script_0("res://")
    
    # Propojí signály
    _connect_signals()
    
    print("✓ Projekt vytvořen!")
```

### Idempotence & Bezpečnost

Skript se automaticky ptá:
- "Soubor `Level1.tscn` již existuje. Přepsat? (Y/n)"
- Vždy bezpečné - nikdy neodstraňuje existující projekty
- Můžeš spustit vícekrát bez obav o duplikaci

## 🐳 Docker

Kompletní aplikaci spusť přes Docker:

```bash
docker-compose up
```

Pak navštiv:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📄 Licence

MIT

## 🤝 Příspívání

Vítáme pull requesty! 

## 📞 Kontakt

- **Issues**: GitHub Issues
- **Diskuze**: GitHub Discussions
- **Twitter**: @GDForgeAI

---

**Made with ❤️ for Godot Game Developers**

*GDForge AI - Because Game Dev Should Be Magical* ✨🎮

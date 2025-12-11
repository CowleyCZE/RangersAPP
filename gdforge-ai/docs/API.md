# API Reference

## Base URL

```
http://localhost:8000/api
```

## Endpoints

### Health Check

Ověří, zda je backend v provozu.

**Request:**
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "llm_provider": "openai"
}
```

---

### Generate Installer

Hlavní endpoint pro generování Installer.gd skriptu.

**Request:**
```bash
POST /generate
Content-Type: application/json

{
  "prompt": "Vytvoř mi level s tilemapou...",
  "project_root": "scenes",
  "format": "gdscript"
}
```

**Parameters:**

| Parametr | Typ | Popis | Default |
|----------|-----|-------|---------|
| `prompt` | string | Popis v přirozeném jazyce | **Required** |
| `project_root` | string | Kořenový adresář (res://...) | `"scenes"` |
| `format` | string | `"gdscript"` nebo `"json"` | `"gdscript"` |

**Response:**
```json
{
  "success": true,
  "blueprint": {
    "scenes": [...],
    "scripts": [...],
    "resources": [...],
    "signals": [...]
  },
  "installer_code": "@tool\nextends EditorScript\n...",
  "filename": "setup_Level1.gd",
  "message": "Successfully generated installer for 1 scenes"
}
```

**Chyby:**

```json
{
  "success": false,
  "error": "LLM Error: Invalid API key"
}
```

---

### Generate Blueprint (JSON Only)

Generuje pouze strukturovaný blueprint bez GDScript kódu.

**Request:**
```bash
POST /generate/json
Content-Type: application/json

{
  "prompt": "Vytvoř inventář systém..."
}
```

**Response:**
```json
{
  "success": true,
  "blueprint": {
    "scenes": [
      {
        "name": "Inventory",
        "path": "res://scenes/Inventory.tscn",
        "root_node": {
          "type": "Control",
          "name": "Inventory"
        },
        "nodes": [
          {
            "name": "Center",
            "type": "CenterContainer",
            "properties": {
              "anchors_preset": 15
            },
            "children": []
          }
        ],
        "script": "res://scripts/Inventory.gd"
      }
    ],
    "scripts": [
      {
        "path": "res://scripts/Inventory.gd",
        "class_name": "Inventory",
        "extends": "Control",
        "properties": [
          {
            "name": "items",
            "type": "Array",
            "default": "[]"
          }
        ],
        "methods": [
          {
            "name": "add_item",
            "signature": "func add_item(name: String) -> bool:",
            "docstring": "Přidá item do inventáře"
          }
        ]
      }
    ],
    "resources": [],
    "signals": [],
    "summary": "Inventář systém se GridContainer 4x sloupců"
  }
}
```

---

## Blueprint Struktura

Vnitřní struktura blueprintu, kterou vygeneruje LLM:

### Scény (Scenes)

```json
{
  "scenes": [
    {
      "name": "SceneName",
      "path": "res://scenes/SceneName.tscn",
      "root_node": {
        "type": "Node2D|Control|Node3D",
        "name": "RootNodeName"
      },
      "nodes": [
        {
          "name": "ChildNodeName",
          "type": "Sprite2D|TileMap|etc",
          "properties": {
            "position": "[100, 200]",
            "rotation": "0.5"
          },
          "children": []
        }
      ],
      "script": "res://scripts/SceneName.gd"
    }
  ]
}
```

### Skripty (Scripts)

```json
{
  "scripts": [
    {
      "path": "res://scripts/PlayerScript.gd",
      "class_name": "Player",
      "extends": "CharacterBody2D",
      "properties": [
        {
          "name": "speed",
          "type": "float",
          "default": "300.0"
        }
      ],
      "methods": [
        {
          "name": "_physics_process",
          "signature": "func _physics_process(delta: float) -> void:",
          "docstring": "Zpracovává fyziku"
        }
      ]
    }
  ]
}
```

### Zdroje (Resources)

```json
{
  "resources": [
    {
      "type": "StandardMaterial3D|NoiseTexture|BoxMesh",
      "path": "res://resources/Material.tres",
      "properties": {
        "albedo_color": "[1.0, 0.0, 0.0, 1.0]",
        "roughness": "0.5"
      }
    }
  ]
}
```

### Signály (Signals)

```json
{
  "signals": [
    {
      "scene": "Level1.tscn",
      "emitter": "PlayerNode",
      "signal_name": "health_changed",
      "receiver": "HealthBarNode",
      "handler": "_on_health_changed"
    }
  ]
}
```

---

## Příklady Použití

### cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Generuj skript
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Vytvoř jednoduchy level",
    "project_root": "scenes",
    "format": "gdscript"
  }'

# Jen blueprint
curl -X POST http://localhost:8000/api/generate/json \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Inventář se 4 sloupci"}'
```

### JavaScript/TypeScript

```typescript
// Health check
const health = await fetch('http://localhost:8000/api/health')
  .then(r => r.json())
console.log(health.status)

// Generate installer
const result = await fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Vytvoř level s hráčem',
    project_root: 'scenes'
  })
}).then(r => r.json())

console.log(result.installer_code)
// Stáhni soubor
const element = document.createElement('a')
element.href = `data:text/plain;charset=utf-8,${result.installer_code}`
element.download = result.filename
element.click()
```

### Python

```python
import requests

# Health check
response = requests.get('http://localhost:8000/api/health')
print(response.json())

# Generate installer
response = requests.post('http://localhost:8000/api/generate', json={
    'prompt': 'Vytvoř level pro plošinovku',
    'project_root': 'scenes',
    'format': 'gdscript'
})

data = response.json()
with open(data['filename'], 'w') as f:
    f.write(data['installer_code'])
```

---

## HTTP Status Kódy

| Kód | Popis |
|-----|-------|
| 200 | OK - Úspěšný request |
| 400 | Bad Request - Chyba validace vstupu |
| 422 | Unprocessable Entity - Chybějící/nevalidní parametr |
| 500 | Internal Server Error - Chyba na serveru |
| 503 | Service Unavailable - LLM API nedostupné |

---

## Rate Limiting

*Zatím nejsou nastaveny limity. Budou přidány v budoucích verzích.*

---

## Autentizace

*V0.1 není vyžadována. Budou přidány JWT tokeny v budoucích verzích.*

---

## Versioning

Aktuální verze: **0.1.0**

API se přímo zajímá o kompatibilitu zpět. Všechny budoucí verze budou
podporovat endpoints z 0.1.0.

---

**Poslední aktualizace**: 2024-12-11

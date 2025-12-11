<!-- GDForge AI - Frontend -->

# GDForge AI Frontend

React + TypeScript webové rozhraní pro GDForge AI.

## Struktura Projektu

```
src/
├── main.tsx              # Entrypoint
├── App.tsx               # Root component
├── index.css             # Global styles
├── store.ts              # Zustand state management
├── components/           # React componenty
│   ├── Header.tsx        # Top bar
│   ├── PromptInput.tsx   # Prompt textarea
│   ├── CodeOutput.tsx    # Code preview
│   └── Examples.tsx      # Example prompts
├── services/             # API client
│   └── api.ts            # Axios HTTP client
└── public/               # Static assets
    └── index.html        # HTML template
```

## Development

```bash
cd frontend
npm install
npm run dev
```

Frontend poběží na http://localhost:5173

## Build

```bash
npm run build
npm run preview
```

## Type Checking

```bash
npm run type-check
```

## Styling

Projekt používá Tailwind CSS pro styling.

- Config: `tailwind.config.js`
- Global styles: `src/index.css`

## State Management

Zustand store v `src/store.ts`:

```typescript
interface GenerateState {
  prompt: string
  isLoading: boolean
  generatedCode: string | null
  generatedBlueprint: any | null
  filename: string | null
  error: string | null
  
  // Actions
  setPrompt: (prompt: string) => void
  // ...
}
```

## API Integration

API client v `src/services/api.ts`:

```typescript
await apiService.generateInstaller({
  prompt: 'Your prompt here',
  project_root: 'scenes',
  format: 'gdscript'
})
```

## Components

### Header
- Top navigation
- "New Project" button

### PromptInput
- Textarea pro zadání promptu
- Konfiguraci project_root
- Format selector
- Generate button

### CodeOutput
- Zobrazení vygenerovaného kódu
- Copy to clipboard
- Download button
- Godot integration instructions

### Examples
- Předdefinované příklady promptů
- Copy-on-click

## Tailwind Setup

Tailwind CSS je konfigurován v `tailwind.config.js`.

Custom utilities v `src/index.css`:
```css
.btn-primary { /* ... */ }
.card { /* ... */ }
.input-field { /* ... */ }
```

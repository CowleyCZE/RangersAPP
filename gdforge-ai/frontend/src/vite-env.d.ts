/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string;
  // přidejte další VITE_* proměnné pokud potřebujete
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
import React, { useRef } from 'react'
import toast from 'react-hot-toast'
import { useGenerateStore } from '../store'
import { apiService } from '../services/api'

export const CodeOutput: React.FC = () => {
  const { generatedCode, filename, isLoading } = useGenerateStore()
  const codeRef = useRef<HTMLPreElement>(null)

  const handleDownload = () => {
    if (!generatedCode || !filename) {
      toast.error('Žádný kód k stažení')
      return
    }

    apiService.downloadFile(generatedCode, filename)
    toast.success(`Soubor ${filename} byl stažen!`)
  }

  const handleCopy = () => {
    if (!generatedCode) return

    navigator.clipboard.writeText(generatedCode)
    toast.success('Kód byl zkopírován do schránky!')
  }

  if (!generatedCode) {
    return (
      <div className="w-full max-w-4xl text-center py-12">
        <div className="text-gray-400 text-lg">
          {isLoading ? '⏳ Generuji tvůj skript...' : '👈 Vyplň prompt a stiskni Generuj'}
        </div>
      </div>
    )
  }

  return (
    <div className="w-full max-w-4xl space-y-4">
      <div className="flex gap-2">
        <button onClick={handleCopy} className="btn-secondary flex-1">
          📋 Zkopírovat
        </button>
        <button onClick={handleDownload} className="btn-success flex-1">
          ⬇️ Stáhnout: {filename}
        </button>
      </div>

      <div className="relative">
        <div className="absolute top-3 right-3 text-xs text-gray-400">
          {generatedCode.split('\n').length} řádků
        </div>
        <pre ref={codeRef} className="code-block max-h-96">
          {generatedCode}
        </pre>
      </div>

      <div className="text-sm text-gray-600 bg-blue-50 p-4 rounded-lg">
        <p className="font-semibold mb-2">📌 Jak v Godotu?</p>
        <ol className="list-decimal list-inside space-y-1">
          <li>Stáhni si soubor <code className="bg-white px-2 py-1 rounded">{filename}</code></li>
          <li>Přetáhni jej do adresáře svého Godot projektu</li>
          <li>V Godot Editoru: File → Run (nebo Ctrl+Shift+F5)</li>
          <li>Hotovo! ✨ Scény a skripty se vytvoří automaticky</li>
        </ol>
      </div>
    </div>
  )
}

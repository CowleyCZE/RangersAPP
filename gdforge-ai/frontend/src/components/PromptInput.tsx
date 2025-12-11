import React, { useState } from 'react'
import toast from 'react-hot-toast'
import { useGenerateStore } from '../store'
import { apiService } from '../services/api'

export const PromptInput: React.FC = () => {
  const { prompt, setPrompt, setLoading, setGeneratedCode, setFilename, setError } = useGenerateStore()
  const [projectRoot, setProjectRoot] = useState('scenes')
  const [format, setFormat] = useState<'gdscript' | 'json'>('gdscript')

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Prosím zadej popis projektu')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await apiService.generateInstaller({
        prompt,
        project_root: projectRoot,
        format,
      })

      if (response.success) {
        setGeneratedCode(response.installer_code || null)
        setFilename(response.filename || 'installer.gd')
        toast.success(response.message || 'Skript byl úspěšně vygenerován!')
      } else {
        throw new Error(response.error || 'Generování selhalo')
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Neznámá chyba'
      setError(errorMessage)
      toast.error(`Chyba: ${errorMessage}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="w-full max-w-2xl space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Popis projektu (Prompt)
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Např: Vytvoř mi level pro plošinovku. Chci scénu 'Level1' s TileMapou, hráčem (CharacterBody2D), kamerou, která ho sleduje, a parallax pozadím..."
          className="input-field min-h-32 resize-none"
          disabled={useGenerateStore((s) => s.isLoading)}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Kořenový adresář
          </label>
          <input
            type="text"
            value={projectRoot}
            onChange={(e) => setProjectRoot(e.target.value)}
            className="input-field"
            placeholder="res://scenes"
            disabled={useGenerateStore((s) => s.isLoading)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Formát výstupu
          </label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value as 'gdscript' | 'json')}
            className="input-field"
            disabled={useGenerateStore((s) => s.isLoading)}
          >
            <option value="gdscript">GDScript (.gd)</option>
            <option value="json">Blueprint (JSON)</option>
          </select>
        </div>
      </div>

      <button
        onClick={handleGenerate}
        disabled={useGenerateStore((s) => s.isLoading) || !prompt.trim()}
        className="btn-primary w-full"
      >
        {useGenerateStore((s) => s.isLoading) ? '⏳ Generuji...' : '✨ Vygeneruj Skript'}
      </button>
    </div>
  )
}

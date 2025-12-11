import React from 'react'
import { useGenerateStore } from '../store'

export const Header: React.FC = () => {
  const { reset } = useGenerateStore()

  return (
    <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-8 shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold">🎮 GDForge AI</h1>
            <p className="text-blue-100 mt-2">
              Infrastructure as Code pro Godot herní vývoj
            </p>
          </div>
          <button
            onClick={reset}
            className="bg-white text-blue-600 px-6 py-2 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
          >
            Nový Projekt
          </button>
        </div>
      </div>
    </header>
  )
}

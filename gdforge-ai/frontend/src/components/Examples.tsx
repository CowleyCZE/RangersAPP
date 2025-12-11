import React from 'react'

export const Examples: React.FC = () => {
  const examples = [
    {
      title: 'Inventář Systém',
      description: 'UI panel s grid containetem pro Item management',
      prompt: 'Potřebuji Inventář systém. Scéna "Inventory.tscn" jako UI panel uprostřed obrazovky. Obsahuje GridContainer se 4 sloupci. Chci k tomu skript "Inventory.gd", který má pole "items" a funkci "add_item(name)".',
    },
    {
      title: 'Level s Platformami',
      description: 'Plošinovka level s TileMapou a hráčem',
      prompt: 'Vytvoř mi level pro plošinovku. Chci scénu "Level1" s TileMapou, hráčem (CharacterBody2D), kamerou která ho sleduje, a parallax pozadím. Hráč má mít základní pohybový skript.',
    },
    {
      title: '3D Scéna',
      description: 'Jednoduchá 3D scéna se osvětlením',
      prompt: 'Vytvoř 3D scénu "MainScene" s Node3D rootem, přidej osvětlení (DirectionalLight3D), mesh (CSGBox3D) a kameru která se otáčí okolo objektu.',
    },
    {
      title: 'Hlavní Menu',
      description: 'UI menu s tlačítky pro navigaci',
      prompt: 'Vytvoř hlavní menu aplikace. Scéna "MainMenu.tscn" s VBoxContainer. Přidej tlačítka: Start Game, Settings, Credits, Quit. Každé tlačítko má mít signál connected na odpovídající handler.',
    },
  ]

  return (
    <div className="w-full max-w-6xl mt-12">
      <h2 className="text-2xl font-bold text-white mb-6">📚 Příklady Promptů</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {examples.map((example, idx) => (
          <div key={idx} className="card p-4 hover:shadow-xl transition-shadow cursor-pointer group">
            <h3 className="font-bold text-lg text-gray-900 group-hover:text-blue-600 transition-colors">
              {example.title}
            </h3>
            <p className="text-sm text-gray-600 mt-1">{example.description}</p>
            <div className="mt-3 p-3 bg-gray-100 rounded text-sm text-gray-700 font-mono line-clamp-3">
              "{example.prompt}"
            </div>
            <p className="text-xs text-gray-500 mt-2">Klikni na kartičku pro zkopírování promptu</p>
          </div>
        ))}
      </div>
    </div>
  )
}

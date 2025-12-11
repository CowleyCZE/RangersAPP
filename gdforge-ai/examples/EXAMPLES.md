# Příklady Promptů pro GDForge AI

Tady jsou připravené příklady promptů, které můžete zkopírovat a upravit podle svých potřeb.

## 1. Inventář Systém

```
Potřebuji Inventář systém. Scéna 'Inventory.tscn' jako UI panel 
uprostřed obrazovky. Obsahuje CenterContainer s PanelContainer 
a uvnitř GridContainer se 4 sloupci. Chci k tomu skript 
'Inventory.gd', který:
- má pole 'items: Array[String]'
- má funkci 'add_item(name: String) -> bool'
- má funkci 'remove_item(name: String) -> bool'
- má signál 'item_added(name: String)'
```

## 2. Level pro Plošinovku

```
Vytvoř mi level pro 2D plošinovku. Chci scénu 'Level1':
- Root node: Node2D
- TileMap s základní strukturou (floor, platformy)
- Player: CharacterBody2D s:
  - Sprite2D
  - CollisionShape2D
  - Skript 'Player.gd' s pohybem (WASD + Space jump)
  - Proměnné: speed=300, jump_force=400
- Camera2D která sleduje hráče
- ParallaxBackground se 2 vrstvami pozadí
```

## 3. 3D Scéna s Modely

```
Vytvoř 3D scénu 'MainScene':
- Node3D root
- DirectionalLight3D (slunce)
- OmniLight3D (местное osvětlení)
- CSGBox3D s StandardMaterial3D (červená barva)
- CSGSphere3D s StandardMaterial3D (modrá barva)
- Camera3D s skriptem pro rotaci okolo objektu
```

## 4. Hlavní Menu

```
Vytvoř hlavní menu aplikace. Scéna 'MainMenu.tscn':
- Root: Control na celou obrazovku s gradientem pozadí
- VBoxContainer s buttons:
  - "Start Game" → signál connected na _on_start_pressed()
  - "Settings" → signál connected na _on_settings_pressed()
  - "Credits" → signál connected na _on_credits_pressed()
  - "Quit" → signál connected na _on_quit_pressed()
- Skript 'MainMenu.gd' s implementací handleru
```

## 5. Herní Skóre Systém

```
Vytvoř Game Over panel scénu 'GameOver.tscn':
- Root: CanvasLayer (aby overlay byl nad vším)
- PanelContainer se tmavým pozadím
- VBoxContainer:
  - Label "Game Over" (velký font)
  - HBoxContainer se skóre:
    - Label "Final Score: "
    - Label s číslem (binding)
  - Tlačítka: "Restart", "Main Menu", "Quit"
- Skript 'GameOver.gd' s proměnnou 'final_score'
- Signály: game_over_confirmed, main_menu_requested
```

## 6. Enemy Systém

```
Vytvoř základní Enemy skript a scénu 'Enemy.tscn':
- Root: CharacterBody2D s název 'Enemy'
- Sprite2D
- CollisionShape2D
- AnimationPlayer (prázdný, jen struktura)
- Skript 'Enemy.gd' s:
  - Properties: speed=100, health=10, damage=5
  - Metody: take_damage(amount), die()
  - Signály: died, took_damage(amount)
```

## 7. Dialóg Systém

```
Vytvoř Dialog UI scénu 'DialogBox.tscn':
- Root: CanvasLayer 
- PanelContainer s black border
- VBoxContainer:
  - Label pro jméno postavy
  - Label pro dialog text (multiline)
  - HBoxContainer s volbami (např. [Yes], [No])
- Skript 'DialogBox.gd' s:
  - Metodou show_dialog(character, text, options)
  - Signály: option_selected(option_index)
```

## 8. Particle Efekt

```
Vytvoř scénu 'ExplosionEffect.tscn':
- Root: Node2D
- GPUParticles2D s:
  - Texture: CircleTexture (procedurální)
  - Speed: 200
  - Lifetime: 1.0
- AudioStreamPlayer2D pro sound efekt
- Skript který odstraní node po skončení animace
```

## 9. Tile-Based Mapa Editor

```
Vytvoř jednoduchou grid-based mapu 'TileMap.tscn':
- Root: Node2D
- TileMap s grid strukturou (8x8)
- Skript 'TileMap.gd' s:
  - Metodou set_tile(x, y, tile_id)
  - Metodou get_tile(x, y) -> int
  - Metodou save_map()
  - Signál: map_changed
```

## 10. Notification Systém

```
Vytvoř UI panel 'NotificationPanel.tscn':
- Root: CanvasLayer
- VBoxContainer pro seznam notifikací
- Skript 'NotificationPanel.gd' s:
  - Metodou show_notification(message, duration=3.0)
  - Automatickým zmizením po čase
  - Animace fade-in/fade-out
```

## Jak Použít Příklady

1. Zkopíruj si prompt z výše
2. Přejdi do GDForge AI webového rozhraní
3. Vleč prompt do textového pole
4. Klikni "Vygeneruj Skript"
5. Stáhni si vygenerovaný soubor
6. Přetáhni ho do svého Godot projektu
7. V editoru spusť File → Run
8. Voilà! ✨

## Tipy pro Psaní Vlastních Promptů

- **Buď specifický**: Pojmenuj scény, uzly, proměnné
- **Popišuj strukturu**: Kterou Node2D/Control/Node3D budeš mít
- **Požaduj skripty**: Jaké metody a signály chceš
- **Zmíň odvětví**: "Plošinovka", "3D RPG", "UI", atd.

Příklad dobrého promptu:

```
Vytvoř Health Bar UI scénu 'HealthBar.tscn':
- Root: Control
- Background: ColorRect (tmavě šedá)
- Health Fill: ProgressBar (zelená na začátku, červená na konci)
- Label "HP: 100/100"
- Skript 'HealthBar.gd' s:
  - max_health = 100
  - set_health(value) 
  - animace přechodu barvy
```

Více příkladů přidáme postupem času! 🚀

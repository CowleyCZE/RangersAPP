# Godot Integration Guide

## Jak Integrovat GDForge AI Výstup do Vašeho Godot Projektu

### Krok 1: Příprava Projektu

1. Otevřete váš Godot 4.0+ projekt
2. Ve File System panelu proveďte pravým klikem → "Open in File Manager"
3. Vytvořte nový adresář pro instalační skripty: `res://gdforge_installers/`

### Krok 2: Stažení Instalačního Skriptu

1. Jděte na http://localhost:5173
2. Zadejte svůj prompt (např: "Vytvoř level pro plošinovku...")
3. Klikněte "Vygeneruj Skript"
4. Klikněte "Stáhnout: setup_*.gd"

### Krok 3: Import do Godotu

1. Přetáhněte stažený soubor `setup_*.gd` do adresáře `res://gdforge_installers/`
2. V Godot editoru by měl soubor automaticky vidět v FileSystem panelu

### Krok 4: Spuštění Instalace

**Metoda 1: Kontextové Menu**
1. Pravým klikem na soubor `setup_*.gd` v FileSystem
2. Vyberte "Open in External Program"
3. Nebo: Klikněte na soubor a stiskněte Ctrl+Shift+F5

**Metoda 2: Menu Bar**
1. Klikněte na soubor v FileSystem
2. Jděte do File → Run

**Metoda 3: Přetažení do Editoru**
1. Přetáhněte soubor na scene editor
2. Automaticky se spustí

### Co Se Stane?

Po spuštění skriptu:

1. 📁 Vytvoří se nové adresáře (pokud neexistují)
2. 🎬 Vytvoří se scény (.tscn soubory)
3. 📝 Vytvoří se skripty (.gd soubory)
4. 🔗 Propojí se signály mezi komponentami
5. 📊 V Godot Console se zobrazí status zprávy:
   ```
   ✓ Scene created: res://scenes/Level1.tscn
   ✓ Script created: res://scripts/Player.gd
   ✓ Signal connected: Player.health_changed -> HealthBar._on_health_changed
   ✓ GDForge project initialized successfully!
   ```

### Ověření

Po spuštění:

1. Otevřete Project → Project Settings → Autoload
2. Měly by vidět nové scény v seznamu
3. Ve FileSystem by měly vidět nové soubory

### Troubleshooting

**Problém: "Script error at line X"**
- Zkontrolujte, zda máte Godot 4.0+
- Zkuste znovu spustit skript

**Problém: "res:// not recognized"**
- Spusťte skript z v Godot editoru, ne mimo něj
- Ujistěte se, že projekt je otevřen

**Problém: Soubory se nevytvořily**
- Zkontrolujte oprávnění k zápisu do adresáře
- Zkuste vytvořit adresář ručně: res://scenes/

### Best Practices

1. **Verzování**: Ukládejte .gdforge instalační skripty do git pro reprodukci
2. **Organizace**: Vytvořte adresář `res://gdforge_installers/` pro všechny skripty
3. **Bezpečnost**: Skript vždy ptá před přepsáním existujících souborů
4. **Čištění**: Po instalaci můžete odstranit .gd skript (není více potřeba)

### Příklad Workflow

```
1. Spustím GDForge AI v prohlížeči
2. Zadám: "Vytvoř level s tilemapou a hráčem"
3. Stáhnu: setup_Level1.gd
4. Přetáhnu do: res://gdforge_installers/
5. Spustím: File → Run
6. Během 1 sekundy je vše připraveno! ✨
```

### Ruční Úpravy po Instalaci

I když je vše automatické, můžete:

- Editovat scény v Scene Editor
- Upravit vygenerované skripty
- Přidat svoje vlastní logiku
- Přidat assets/textury

Vygenerované soubory jsou normální Godot assets!

### Sdílení s Týmem

1. Uložte instalační skript do git: `gdforge_installers/setup_Level1.gd`
2. Kolega si vybere a spustí v editoru
3. Automaticky získá stejnou strukturu! 🎉

---

**Hotovější? Pokračuj v Editoru! 🎮✨**

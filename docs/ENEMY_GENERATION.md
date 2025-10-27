# Enemy Sprite Generation

This project uses **PixelLab API** for fast, AI-powered sprite generation. The Blender generator is kept as a reference in `blender_scripts/create_enemy_sprite.py`.

## Setup

### 1. Configure PixelLab API Key

Edit `scripts/pixellab_config.py` and add your API key:

```python
PIXELLAB_API_KEY = "your_actual_api_key_here"
```

**Important:** This file is git-ignored to protect your API key. Never commit it!

### 2. Install Python Dependencies

```powershell
python -m pip install requests
```

## Usage

### Generate a New Enemy

Use the PowerShell wrapper for the easiest workflow:

```powershell
.\scripts\generate_enemy.ps1 -Name "goblin" -Description "small brown goblin creature with pointy ears"
```

This will:
1. Generate all 4 animations (idle, walk, attack, death) using PixelLab
2. Download sprites to `assets/enemies/[name]/`
3. Auto-import into Godot
4. Make the enemy ready to use!

### Advanced Options

```powershell
# Custom output directory
.\scripts\generate_enemy.ps1 -Name "bat" -Description "dark flying bat" -OutputDir "assets/flying_enemies"

# Custom sprite size
.\scripts\generate_enemy.ps1 -Name "giant" -Description "huge rock giant" -Size 128
```

### Direct Python Usage

```powershell
python .\scripts\generate_enemy_pixellab.py `
  --name "skeleton" `
  --description "undead skeleton warrior" `
  --size 64
```

## Animation Frame Counts

Default frame counts (configured in `pixellab_config.py`):
- **Idle**: 4 frames - Subtle breathing/bobbing
- **Walk**: 8 frames - Movement cycle
- **Attack**: 6 frames - Wind-up, strike, return
- **Death**: 8 frames - Collapse/fade animation

## Examples

```powershell
# Generate various enemy types
.\scripts\generate_enemy.ps1 -Name "slime" -Description "green puddle of slime"
.\scripts\generate_enemy.ps1 -Name "ghost" -Description "translucent white ghost, ethereal"
.\scripts\generate_enemy.ps1 -Name "spider" -Description "large black spider with red eyes"
.\scripts\generate_enemy.ps1 -Name "demon" -Description "red demon with horns and wings"
```

## Troubleshooting

**"Please set your PixelLab API key"**
- Edit `scripts/pixellab_config.py` with your actual API key

**"Python not found"**
- Install Python 3.7+ from https://python.org

**"Module 'requests' not found"**
- Run: `python -m pip install requests`

**API Timeout**
- Increase `PIXELLAB_TIMEOUT` in `pixellab_config.py` (default: 300 seconds)
- PixelLab may be experiencing high load

**Generation Failed**
- Check your API key is valid
- Verify you have API credits remaining
- Try a simpler description

## Legacy Blender Generator

The original Blender-based generator is still available in `blender_scripts/create_enemy_sprite.py` as a reference or fallback option.

To use it:
```powershell
& .\bin\blender-4.5.3-windows-x64\blender.exe --background --python .\blender_scripts\create_enemy_sprite.py -- --enemy-name "slime" --body-color "0.2,0.8,0.3,1.0"
```

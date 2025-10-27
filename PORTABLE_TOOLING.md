# Portable Tooling Setup Guide

This project follows a **portable tooling** philosophy - all development tools are stored in the `./bin/` directory to ensure a uniform development experience across all workstations.

## 🎯 Philosophy

**No machine-specific paths. Ever.**

- ❌ NEVER: `C:\Users\Ben\code\cave-crawler\...`
- ❌ NEVER: `C:\Program Files\Godot\...`
- ✅ ALWAYS: `./bin/Godot_v4.5.1-stable_win64.exe`
- ✅ ALWAYS: Relative paths from project root

## 📁 Directory Structure

```
cave-crawler/
├── bin/                              # All executables (gitignored)
│   ├── Godot_v4.5.1-stable_win64.exe
│   └── blender-4.5.0-windows-x64/
│       └── blender.exe
├── blender_scripts/                  # Blender automation scripts
│   ├── create_pixel_textures.py
│   └── create_iso_tiles.py
├── scripts/                          # Helper scripts
│   └── run_blender.ps1              # Portable Blender runner
└── assets/                          # Generated assets
    ├── textures/
    └── tiles/
```

## 🔧 Setup Instructions

### 1. Install Godot (Portable)

```powershell
# Download Godot 4.5.1+ from https://godotengine.org/download/
# Extract to ./bin/ directory
cd cave-crawler
# Place the executable directly in bin/
./bin/Godot_v4.5.1-stable_win64.exe
```

### 2. Install Blender (Portable)

```powershell
# Download Blender 4.5+ portable from https://www.blender.org/download/
# Extract the entire folder to ./bin/
cd cave-crawler/bin
# Extract blender-4.5.0-windows-x64.zip here
# Result: ./bin/blender-4.5.0-windows-x64/blender.exe
```

### 3. Verify Setup

```powershell
# Check that executables exist
Test-Path ./bin/Godot_v4.5.1-stable_win64.exe
Test-Path ./bin/blender-4.5.0-windows-x64/blender.exe
```

## 🚀 Usage

### Running Godot

```powershell
# From project root
.\bin\Godot_v4.5.1-stable_win64.exe --path . scenes/generation/procedural_cave.tscn
```

### Running Blender Scripts

```powershell
# Use the portable helper script
.\scripts\run_blender.ps1 create_pixel_textures.py

# Or manually:
.\bin\blender-4.5.0-windows-x64\blender.exe --background --python .\blender_scripts\create_pixel_textures.py
```

### Generating Textures

```powershell
# Generate all SNES-style textures (16 textures)
.\scripts\run_blender.ps1 create_pixel_textures.py

# Generate isometric tiles
.\scripts\run_blender.ps1 create_iso_tiles.py
```

## 📝 Script Guidelines

All scripts MUST use portable relative paths:

### Python (Blender Scripts)

```python
import os

# ✅ CORRECT: Portable relative path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'assets', 'textures')

# ❌ WRONG: Absolute path
OUTPUT_DIR = r"C:\Users\Ben\code\cave-crawler\assets\textures"
```

### GDScript (Godot)

```gdscript
# ✅ CORRECT: Use res:// paths
var texture = load("res://assets/textures/cave_floor_tile.png")

# ❌ WRONG: Absolute paths
var texture = load("C:/Users/Ben/code/cave-crawler/assets/textures/cave_floor_tile.png")
```

### PowerShell Scripts

```powershell
# ✅ CORRECT: Relative to script location
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BinDir = Join-Path $ProjectRoot "bin"

# ❌ WRONG: Hardcoded paths
$BinDir = "C:\Users\Ben\code\cave-crawler\bin"
```

## 🌍 Cross-Workstation Workflow

1. **Clone the repository** on any workstation
2. **Download portable tools** (Godot, Blender) to `./bin/`
3. **Run scripts** - they automatically find tools in `./bin/`
4. **Commit your work** - tools are gitignored, only code is versioned

### Example: New Workstation Setup

```powershell
# 1. Clone the repo
git clone https://github.com/willowduster/cave-crawler.git
cd cave-crawler

# 2. Create bin directory
mkdir bin

# 3. Download Godot portable
# Place in: ./bin/Godot_v4.5.1-stable_win64.exe

# 4. Download Blender portable
# Extract to: ./bin/blender-4.5.0-windows-x64/

# 5. Done! All scripts now work
.\scripts\run_blender.ps1 create_pixel_textures.py
.\bin\Godot_v4.5.1-stable_win64.exe --path . scenes/generation/procedural_cave.tscn
```

## ⚙️ .gitignore Configuration

The `./bin/` directory is gitignored to keep executables out of version control:

```gitignore
# Development tools (portable, not versioned)
bin/
*.exe
*.app
*.dmg
```

## 🤖 MCP Server Portability (AI Assistant Integration)

### Important: MCP Servers Are NOT Fully Portable

While **executables** (Godot, Blender) are portable via `./bin/`, **MCP servers** require per-workstation setup:

#### Godot MCP ✅ Semi-Portable
- **Requires**: Node.js installed globally on system
- **Setup**: `cd godot-mcp && npm install && npm run build`
- **Portability**: Can be cloned, but needs build step per workstation
- **Config**: Uses relative paths (portable once built)

#### Blender MCP ⚠️ NOT Portable
- **Requires**: 
  - Blender installed and running
  - Manual addon installation via Blender UI (Edit → Preferences → Add-ons → Install)
  - Clicking "Start Server" button in Blender each session
  - Python environment setup with `uv`
- **Portability**: ❌ **NOT portable** - requires manual UI steps
- **Alternative**: Use `blender_scripts/` with `run_blender.ps1` (fully portable)

#### Filesystem & Git MCP ✅ Portable
- Official Anthropic servers
- Installed globally via MCP client (Claude Desktop/Cursor)
- Work automatically once configured

### Recommendation: Use Blender Scripts, Not Blender MCP

For **portable, repeatable asset generation**, use the Blender automation scripts:

```powershell
# ✅ PORTABLE: Works on any machine with Blender in ./bin/
.\scripts\run_blender.ps1 create_pixel_textures.py

# ❌ NOT PORTABLE: Requires Blender UI setup, manual button clicks
# MCP server approach - avoid for portability
```

### Why Blender Scripts Are Better

| Feature | Blender MCP | Blender Scripts |
|---------|-------------|-----------------|
| Portability | ❌ Manual setup required | ✅ Fully automated |
| Cross-workstation | ❌ Need to setup each time | ✅ Clone and run |
| Repeatability | ⚠️ Depends on server state | ✅ Same output every time |
| Version control | ❌ Server config not versioned | ✅ Scripts fully versioned |
| Dependencies | ❌ Running Blender + addon + uv | ✅ Just Blender executable |
| Use case | Interactive asset creation | Batch texture generation |

**Constitutional Guidance**: For portable asset generation workflows, use `blender_scripts/` automation instead of Blender MCP server.

### "Godot executable not found"

```powershell
# Check if Godot is in ./bin/
ls ./bin/Godot*.exe

# If missing, download from https://godotengine.org/download/
# Place directly in ./bin/
```

### "Blender executable not found"

```powershell
# Check if Blender is in ./bin/
ls ./bin/blender*/blender.exe

# If missing, download portable from https://www.blender.org/download/
# Extract entire folder to ./bin/
```

### "Cannot find path"

All scripts use relative paths. Make sure you run them from the **project root**:

```powershell
# ✅ CORRECT: From project root
cd cave-crawler
.\scripts\run_blender.ps1 create_pixel_textures.py

# ❌ WRONG: From subdirectory
cd cave-crawler/scripts
.\run_blender.ps1 create_pixel_textures.py  # Will fail!
```

## 📜 Constitutional Requirement

This portable tooling setup is part of the **Project Constitution** (see `PROJECT_CONSTITUTION.md`).

All contributors MUST follow these guidelines to ensure uniform development experience across workstations.

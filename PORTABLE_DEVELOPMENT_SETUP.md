# 100% Portable Development Setup

**Goal**: Clone repo → Install tools → Start working (no AI assistant required)

## 🎯 Core Philosophy

**MCP servers are NOT required for development.** They're optional AI assistance tools.

### What You Need (100% Portable)

1. **Godot 4.5.1** in `./bin/`
2. **Blender 4.5+** in `./bin/` (optional, for asset generation)
3. **Git** (already installed)

That's it. No MCP servers needed.

## 🚀 Fresh Workstation Setup (5 Minutes)

### Step 1: Clone Repository
```powershell
git clone https://github.com/willowduster/cave-crawler.git
cd cave-crawler
```

### Step 2: Install Godot (Required)
```powershell
# Download from https://godotengine.org/download/
# Get: Godot 4.5.1 Standard (NOT .NET version)
# Save to: ./bin/Godot_v4.5.1-stable_win64.exe
```

**Verify**:
```powershell
Test-Path ./bin/Godot_v4.5.1-stable_win64.exe  # Should return True
```

### Step 3: Install Blender (Optional - Only for Asset Generation)
```powershell
# Download from https://www.blender.org/download/
# Get: Blender 4.5+ Portable ZIP
# Extract to: ./bin/blender-4.5.0-windows-x64/
```

**Verify**:
```powershell
Test-Path ./bin/blender-4.5.0-windows-x64/blender.exe  # Should return True
```

### Step 4: You're Done! 🎉

```powershell
# Run the game
.\bin\Godot_v4.5.1-stable_win64.exe --path . scenes/levels/procedural_cave.tscn

# Generate textures (if you installed Blender)
.\scripts\run_blender.ps1 create_pixel_textures.py
```

## 📋 What About MCP Servers?

**MCP servers are OPTIONAL** - they enable AI assistants (like me) to help you, but **you don't need them to develop**.

### Development Without MCP

You can do everything manually:

| Task | Without MCP | With MCP (AI Assisted) |
|------|-------------|----------------------|
| Edit code | Use your code editor | AI suggests changes |
| Create scenes | Godot Editor | AI creates scenes via Godot MCP |
| Generate textures | `run_blender.ps1` script | AI creates via Blender MCP |
| Commit code | `git commit -m "message"` | AI commits via Git MCP |
| Debug | Godot debugger | AI analyzes output via Godot MCP |

**Bottom line**: MCP = AI assistance. You don't need it to code.

### If You Want AI Assistance (Optional)

See these guides (for **each workstation** where you want AI help):
- [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md) - Full setup instructions
- [MCP_PORTABILITY_ANALYSIS.md](MCP_PORTABILITY_ANALYSIS.md) - What's portable vs not

**Accept**:
- Godot MCP: Needs `npm install` (5 min setup per workstation)
- Blender MCP: Needs manual addon install (10 min setup per workstation)
- Both are **per-workstation setup**, not portable

## 🎮 Development Workflows

### 1. Game Development (No MCP Needed)

```powershell
# Open project in Godot
.\bin\Godot_v4.5.1-stable_win64.exe --editor --path .

# Edit scenes/scripts in Godot Editor
# Run game with F5 or:
.\bin\Godot_v4.5.1-stable_win64.exe --path . scenes/generation/procedural_cave.tscn

# Commit your work
git add .
git commit -m "Your changes"
git push
```

### 2. Asset Generation (No MCP Needed)

```powershell
# Generate all 16 SNES textures
.\scripts\run_blender.ps1 create_pixel_textures.py

# Generate isometric tiles
.\scripts\run_blender.ps1 create_iso_tiles.py

# Output appears in ./assets/textures/
```

### 3. With AI Assistance (MCP Setup Required)

If you've set up MCP servers on this workstation:
- Ask AI to create scenes
- Ask AI to generate custom assets
- Ask AI to debug issues
- Ask AI to commit changes

**But this is a bonus, not required.**

## 🔧 Troubleshooting

### "Godot won't run"

Check Godot version:
```powershell
.\bin\Godot_v4.5.1-stable_win64.exe --version
# Should show: 4.5.1.stable.official
```

If missing, download from https://godotengine.org/download/

### "Blender script fails"

Check Blender is in `./bin/`:
```powershell
.\bin\blender-4.5.0-windows-x64\blender.exe --version
# Should show: Blender 4.5.0
```

If missing, download portable ZIP from https://www.blender.org/download/

### "I want AI assistance"

That's optional! See:
1. [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md) - Setup instructions
2. [MCP_PORTABILITY_ANALYSIS.md](MCP_PORTABILITY_ANALYSIS.md) - What to expect

## 📊 Portability Matrix

| Component | Portable? | Required? | Setup Time |
|-----------|-----------|-----------|------------|
| Godot executable | ✅ Yes | ✅ Yes | 2 min (download) |
| Blender executable | ✅ Yes | ⚠️ Optional | 3 min (download) |
| Game code | ✅ Yes (Git) | ✅ Yes | 0 min (clone) |
| Blender scripts | ✅ Yes (Git) | ✅ Yes | 0 min (clone) |
| Godot MCP | ⚠️ Semi | ❌ No | 5 min (per workstation) |
| Blender MCP | ❌ No | ❌ No | 10 min (per workstation) |
| **Total for core dev** | ✅ | - | **5 min** |
| **Total with AI** | ⚠️ | - | **20 min** |

## ✅ Constitutional Compliance

This setup follows the project constitution:

> **All development tools MUST be portable across workstations.**

✅ Godot in `./bin/` - portable  
✅ Blender in `./bin/` - portable  
✅ Scripts use relative paths - portable  
✅ No hardcoded paths - portable  
⚠️ MCP servers - **optional, not required**

## 🎯 The Real Answer

**You can't make MCP 100% portable** because:
1. MCP clients (Claude Desktop, Cursor) are installed globally
2. They need per-user configuration files
3. Some MCP servers (Blender) require UI interaction
4. This is by design for security

**But you don't need MCP to develop!**

Core development is 100% portable:
- Clone → Install Godot/Blender to `./bin/` → Code

MCP is just AI assistance on top of that.

## 🚀 Quick Start Commands

```powershell
# Fresh workstation setup
git clone https://github.com/willowduster/cave-crawler.git
cd cave-crawler

# Download Godot 4.5.1 to ./bin/ from https://godotengine.org
# Download Blender 4.5+ to ./bin/ from https://blender.org (optional)

# Run game
.\bin\Godot_v4.5.1-stable_win64.exe --path . scenes/generation/procedural_cave.tscn

# Generate textures
.\scripts\run_blender.ps1 create_pixel_textures.py

# Done! Start coding.
```

**AI assistance (MCP) is optional.**

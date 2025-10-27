# Cave Crawler - AI-Assisted Game Development

**An isometric dungeon crawler built with Godot 4.5.1, featuring procedural cave generation and AI-assisted development via Model Context Protocol (MCP).**

## 🎮 Current Status

- ✅ Procedural cave generation (cellular automata, 150x120 grid)
- ✅ Isometric click-to-move player controls
- ✅ SNES-style pixel art textures (16 unique sprites with detailed gradients)
- ✅ Natural cave floors with depressions, cracks, and scattered details
- ✅ Debug console system (toggleable with Backspace)
- ✅ Randomized obstacle sizes (0.7x-1.3x variation)
- ✅ Z-index depth sorting fixed
- ✅ 100% portable tooling (executables in `./bin/`)
- ⏳ A* pathfinding (next)
- ⏳ Enemy AI
- ⏳ Combat system

## 🚀 Quick Start

### Prerequisites

**This project uses portable tooling** - all executables in `./bin/` for cross-workstation compatibility. See [PORTABLE_TOOLING.md](PORTABLE_TOOLING.md) for details.

1. **Clone the repository**
   ```powershell
   git clone https://github.com/willowduster/cave-crawler.git
   cd cave-crawler
   ```

2. **Install Godot (Portable)**
   - Download [Godot 4.5.1+](https://godotengine.org/download/) (Standard version)
   - Place in `./bin/Godot_v4.5.1-stable_win64.exe`

3. **Install Blender (Portable)** _(optional, for asset generation)_
   - Download [Blender 4.5+ Portable](https://www.blender.org/download/)
   - Extract to `./bin/blender-4.5.0-windows-x64/`

4. **Run the game**
   ```powershell
   .\bin\Godot_v4.5.1-stable_win64.exe --path . scenes/levels/procedural_cave.tscn
   ```

### Controls

- **Click or Hold**: Move player to mouse position
- **Q**: Quit game
- **Backspace**: Toggle debug console

## 🎨 Asset Generation

Generate textures using the portable Blender script:

```powershell
# Generate all 16 SNES-style textures
.\scripts\run_blender.ps1 create_pixel_textures.py

# Generate isometric tiles
.\scripts\run_blender.ps1 create_iso_tiles.py
```

## 🛠️ Development Tools

### Core Tools (Required, Fully Portable ✅)

1. **Godot 4.5.1** - In `./bin/` directory
   - Run game, edit scenes, debug
   - Fully portable executable

2. **Blender 4.5+** - In `./bin/` directory  
   - Asset generation via automation scripts
   - Fully portable via `run_blender.ps1`

### MCP Servers (Optional, NOT Required ⚠️)

**You don't need MCP to develop this game.** MCP enables AI assistance but is entirely optional.

**Want 100% portable setup?** See [PORTABLE_DEVELOPMENT_SETUP.md](PORTABLE_DEVELOPMENT_SETUP.md) - Just Godot + Blender in `./bin/`, no MCP needed.

**Want AI assistance?** (Requires per-workstation setup):

1. **Godot MCP** - AI creates scenes, runs game
   - Setup: 5 min per workstation ([MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md))
   
2. **Blender MCP** - AI creates custom 3D models
   - Setup: 10 min per workstation, **NOT portable**
   - Alternative: Use portable `blender_scripts/` for asset generation

3. **Filesystem/Git MCP** - AI manages files/commits
   - Built into Claude Desktop/Cursor

**Bottom line**: Core development uses portable tools. MCP is bonus AI help.

See [MCP_PORTABILITY_ANALYSIS.md](MCP_PORTABILITY_ANALYSIS.md) for why MCP isn't fully portable.

## 📜 Portable Tooling Philosophy

**Constitutional Requirement**: All development tools MUST be portable across workstations.

✅ **What This Means**:
- All executables in `./bin/` (gitignored)
- Scripts use relative paths from project root
- Works on any machine without hardcoded paths
- No `C:\Users\Ben\...` or `C:\Program Files\...` paths

✅ **Benefits**:
- Clone repo → install tools to `./bin/` → start working
- Same experience on all workstations
- No path configuration needed
- Easy onboarding for new developers

See [PORTABLE_TOOLING.md](PORTABLE_TOOLING.md) for complete guidelines and setup instructions.

## 📚 Documentation

### Core Documentation
- **[PORTABLE_DEVELOPMENT_SETUP.md](PORTABLE_DEVELOPMENT_SETUP.md)** - 100% portable setup (no MCP needed!) **← START HERE**
- **[PORTABLE_TOOLING.md](PORTABLE_TOOLING.md)** - Portable tooling philosophy and guidelines
- **[PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md)** - Development standards and requirements
- **[MCP_PORTABILITY_ANALYSIS.md](MCP_PORTABILITY_ANALYSIS.md)** - Why MCP isn't fully portable
- **[MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)** - Optional AI assistant setup (if you want it)

### Technical Guides
- **[TILEMAP_GUIDE.md](TILEMAP_GUIDE.md)** - Tilemap and collision setup
- **[GODOT_TILESET_SETUP.md](GODOT_TILESET_SETUP.md)** - Tileset configuration
- **[MIGRATION_TO_COMMUNITY_MCP.md](MIGRATION_TO_COMMUNITY_MCP.md)** - Why we use community MCP servers

### Development History
- **[PHASE_2_COMPLETE.md](PHASE_2_COMPLETE.md)** - Platformer POC completion
- **[PLATFORMER_TO_ISOMETRIC_MIGRATION.md](PLATFORMER_TO_ISOMETRIC_MIGRATION.md)** - Isometric pivot
- **[specs/001-mcp-dev-tools/](./specs/001-mcp-dev-tools/)** - Original project specifications

## 🎯 Development Workflow

With MCP servers configured, you can ask your AI assistant to:

### 🎮 Godot Operations
```
"Create a new 2D scene for the player character"
"Add a CharacterBody2D node with collision shape"
"Write a movement script with WASD controls"
"Launch the Godot editor"
"Run the project and show me the debug output"
```

### 📁 File Management
```
"Show me all GDScript files in the project"
"Read the player.gd script"
"Create a new folder called 'enemies'"
```

### 🔧 Version Control
```
"What files have I changed?"
"Show me the diff for player.gd"
"Commit these changes with message 'Add player movement'"
```

### 🎨 Asset Creation (with Blender)
```
"Create a low-poly rock model"
"Apply a stone material"
"Export as GLTF for Godot"
```

## 🏆 What We Learned

This project includes a **fully functional custom MCP implementation** (archived in `_archived/`) that we built as a learning exercise. It includes:

- ✅ Complete Godot integration (8 operations)
- ✅ 47+ passing tests
- ✅ PowerShell automation scripts
- ✅ Configuration management
- ✅ Successfully tested with Godot 4.5.1

**Value**: We now deeply understand MCP architecture and can customize/extend community servers if needed.

**Why switch?** Community servers are actively maintained, have more features, and let us focus on game development instead of infrastructure.

## 🎮 About Cave Crawler

[Add your game description here]

## 🤝 Contributing

This is a personal learning project, but feedback and suggestions are welcome!

## 📝 License

[Add your license here]

## 🔗 Resources

- **Godot Engine**: https://godotengine.org/
- **Model Context Protocol**: https://modelcontextprotocol.io/
- **Godot MCP Server**: https://github.com/Coding-Solo/godot-mcp
- **Blender MCP Server**: https://github.com/ahujasid/blender-mcp

---

**Status**: 🚀 Ready for Development  
**Godot Version**: 4.5.1  
**MCP Servers**: Configured  
**Last Updated**: October 27, 2025

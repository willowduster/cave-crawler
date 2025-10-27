# Cave Crawler - AI-Assisted Game Development

A game development project using **Godot Engine 4.5.1** with AI-powered development tools via the **Model Context Protocol (MCP)**.

## 🎮 Project Structure

```
cave-crawler/
├── bin/                        # Godot Engine 4.5.1 executables
├── cave-crawler/               # Main Godot game project
├── specs/                      # Project specifications
├── godot-mcp/                  # Godot MCP Server (community)
├── blender-mcp/                # Blender MCP Server (community)
├── _archived/                  # Archived custom implementations
│   └── custom-mcp-implementation/  # Our learning project (fully functional)
├── MCP_SETUP_GUIDE.md         # Complete setup instructions
├── MIGRATION_TO_COMMUNITY_MCP.md  # Migration documentation
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Node.js** - For Godot MCP server
2. **Python 3.10+** - Already installed ✅
3. **uv** - Python package manager
4. **Godot Engine 4.5.1** - Already in `bin/` ✅

### Setup MCP Servers

**See complete instructions in**: [`MCP_SETUP_GUIDE.md`](./MCP_SETUP_GUIDE.md)

**Quick version**:
```powershell
# 1. Install Node.js from https://nodejs.org/

# 2. Install uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. Build Godot MCP
cd godot-mcp
npm install
npm run build

# 4. Configure Claude Desktop / Cursor
# See MCP_SETUP_GUIDE.md for configuration
```

## 🛠️ MCP Servers in Use

### ✅ Active MCP Servers

1. **Godot MCP** ([Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp))
   - Launch Godot editor
   - Run projects in debug mode
   - Manage scenes and nodes
   - Capture debug output

2. **Filesystem MCP** (Official Anthropic)
   - Secure file operations
   - Read/write game files
   - Directory management

3. **Git MCP** (Official Anthropic)
   - Version control operations
   - Commit, diff, log
   - Branch management

4. **Blender MCP** (Optional - [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp))
   - Create 3D assets
   - Material and texture work
   - Export GLTF for Godot

## 📚 Documentation

- **[MCP_SETUP_GUIDE.md](./MCP_SETUP_GUIDE.md)** - Complete installation and configuration guide
- **[MIGRATION_TO_COMMUNITY_MCP.md](./MIGRATION_TO_COMMUNITY_MCP.md)** - Why we switched to community servers
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

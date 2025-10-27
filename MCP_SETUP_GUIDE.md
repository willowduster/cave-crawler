# MCP Setup Guide for Cave Crawler Development

## Quick Start - Installation Checklist

### Prerequisites to Install

- [ ] **Node.js** (for Godot MCP) - [Download](https://nodejs.org/)
- [ ] **Python 3.10+** (for Git/Blender MCP) - Already have 3.14 ✅
- [ ] **uv** (Python package manager) - [Install Guide](https://docs.astral.sh/uv/getting-started/installation/)
- [ ] **Godot Engine 4.5.1** - Already in `bin/` ✅
- [ ] **Blender 3.0+** (optional) - [Download](https://www.blender.org/download/)

---

## Step-by-Step Installation

### 1️⃣ Install Node.js (Required for Godot MCP)

**Download**: https://nodejs.org/en/download/

**Recommended**: LTS version (v20.x or v22.x)

**Verify Installation**:
```powershell
node --version
npm --version
```

### 2️⃣ Install uv Package Manager (Required for Python MCP servers)

**Windows Installation**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Add to PATH** (may be required):
```powershell
$env:Path += ";$env:USERPROFILE\.local\bin"
```

**Verify Installation**:
```powershell
uv --version
```

### 3️⃣ Build Godot MCP Server

```powershell
cd C:\Users\Ben\code\cave-crawler\godot-mcp
npm install
npm run build
```

**Expected Output**: `build/index.js` created successfully

### 4️⃣ Setup Blender MCP Server (Optional)

**If you plan to create 3D assets**:

```powershell
cd C:\Users\Ben\code\cave-crawler\blender-mcp
```

**Install Blender Addon**:
1. Open Blender
2. Edit → Preferences → Add-ons → Install
3. Select `addon.py` from the `blender-mcp` folder
4. Enable "Blender MCP Socket Server"
5. Click "Start Server" (runs on port 9876)

---

## MCP Client Configuration

### Option A: Claude Desktop

**Config File Location**:
```
C:\Users\Ben\AppData\Roaming\Claude\claude_desktop_config.json
```

**Complete Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\Ben\\code\\cave-crawler"
      ]
    },
    "git": {
      "command": "uvx",
      "args": [
        "mcp-server-git",
        "--repository",
        "C:\\Users\\Ben\\code\\cave-crawler"
      ]
    },
    "godot": {
      "command": "node",
      "args": [
        "C:\\Users\\Ben\\code\\cave-crawler\\godot-mcp\\build\\index.js"
      ],
      "env": {
        "DEBUG": "true"
      }
    },
    "blender": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\Ben\\code\\cave-crawler\\blender-mcp",
        "run",
        "blender-mcp"
      ],
      "env": {
        "BLENDER_HOST": "localhost",
        "BLENDER_PORT": "9876"
      }
    }
  }
}
```

**After editing**: Restart Claude Desktop

### Option B: Cursor

1. **Cursor Settings** → **Features** → **MCP**
2. **Add each server**:

**Filesystem Server**:
- Name: `filesystem`
- Type: `command`
- Command: `npx -y @modelcontextprotocol/server-filesystem C:\Users\Ben\code\cave-crawler`

**Git Server**:
- Name: `git`
- Type: `command`
- Command: `uvx mcp-server-git --repository C:\Users\Ben\code\cave-crawler`

**Godot Server**:
- Name: `godot`
- Type: `command`
- Command: `node C:\Users\Ben\code\cave-crawler\godot-mcp\build\index.js`

**Blender Server** (optional):
- Name: `blender`
- Type: `command`
- Command: `uv --directory C:\Users\Ben\code\cave-crawler\blender-mcp run blender-mcp`
- Environment: `BLENDER_HOST=localhost`, `BLENDER_PORT=9876`

### Option C: Cline (VS Code Extension)

**Config File**: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

(Same JSON structure as Claude Desktop)

---

## Testing Your Setup

### Test Godot MCP

**In your AI assistant**, try:
```
Can you get the Godot version?
```

**Expected**: Should return Godot version info

### Test Filesystem MCP

```
List all .gd files in the cave-crawler project
```

**Expected**: Should list GDScript files

### Test Git MCP

```
What's the current git status?
```

**Expected**: Should show branch and uncommitted changes

### Test Blender MCP

```
Create a simple cube in Blender
```

**Expected**: Cube appears in Blender viewport

---

## Available Tools

### 🎮 Godot MCP Tools

- `get_godot_version` - Get installed Godot version
- `list_projects` - Find Godot projects in a directory
- `get_project_info` - Get detailed project structure
- `launch_editor` - Open Godot editor for a project
- `run_project` - Execute project in debug mode
- `stop_project` - Stop running project
- `get_debug_output` - Capture console output
- `create_scene` - Create new scene files
- `add_node` - Add nodes to scenes
- `load_sprite` - Load sprites/textures
- `export_mesh_library` - Export 3D scenes
- `save_scene` - Save scene files
- `get_uid` - Get file UID (Godot 4.4+)
- `update_project_uids` - Update UID references

### 📁 Filesystem MCP Tools

- `read_file` - Read file contents
- `write_file` - Write to files
- `list_directory` - List directory contents
- `create_directory` - Create directories
- `move_file` - Move/rename files
- `delete_file` - Delete files

### 🔧 Git MCP Tools

- `git_status` - Check repository status
- `git_log` - View commit history
- `git_diff` - Show changes
- `git_commit` - Commit changes
- `git_add` - Stage files
- `git_show` - Show commit details

### 🎨 Blender MCP Tools

- `create_object` - Create 3D objects
- `modify_object` - Transform objects
- `apply_material` - Add materials/colors
- `get_scene_info` - Inspect current scene
- `execute_code` - Run Python in Blender
- `search_sketchfab` - Download Sketchfab models
- `download_poly_haven` - Get Poly Haven assets
- `capture_viewport` - Take screenshots
- `generate_3d_model` - AI-generated models (Hyper3D)

---

## Common Issues & Solutions

### ❌ "npm is not recognized"

**Solution**: Install Node.js from https://nodejs.org/

### ❌ "uvx is not recognized"

**Solution**: 
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
$env:Path += ";$env:USERPROFILE\.local\bin"
```

### ❌ Godot MCP can't find Godot

**Solution**: Ensure Godot is in PATH or specify full path in your project

### ❌ Blender MCP connection refused

**Solution**: 
1. Make sure Blender is open
2. Enable "Blender MCP Socket Server" addon
3. Click "Start Server" in addon preferences

### ❌ MCP servers not appearing in Claude/Cursor

**Solution**:
1. Check JSON syntax in config file
2. Restart the application
3. Check MCP server logs for errors

---

## Workflow Examples

### 🎮 Game Development Workflow

**Create a new Godot scene**:
```
Create a new 2D scene called "PlayerCharacter" with a CharacterBody2D root node
```

**Add GDScript**:
```
Create a player movement script with WASD controls and basic physics
```

**Test in Godot**:
```
Launch the Godot editor for this project
```

### 🎨 Asset Creation Workflow

**In Blender**:
```
Create a low-poly rock model suitable for a cave environment
```

**Export for Godot**:
```
Export the rock as GLTF to the cave-crawler assets folder
```

**Import to Godot**:
```
Create a Godot scene that uses the rock GLTF model
```

### 🔧 Code Management Workflow

**Check changes**:
```
Show me what files have been modified
```

**Commit work**:
```
Stage all modified .gd files and commit with message "Add player movement"
```

---

## Next Steps

1. ✅ **Complete prerequisites installation**
2. ✅ **Build Godot MCP server** (`npm run build`)
3. ✅ **Configure your AI assistant** (Claude/Cursor/Cline)
4. ✅ **Test each MCP server** with simple commands
5. 🚀 **Start building your cave-crawler game!**

---

## Resources

- **Godot MCP**: https://github.com/Coding-Solo/godot-mcp
- **Blender MCP**: https://github.com/ahujasid/blender-mcp
- **MCP Specification**: https://modelcontextprotocol.io/
- **Godot Docs**: https://docs.godotengine.org/
- **Blender Python API**: https://docs.blender.org/api/current/

---

## Support

- **Godot MCP Issues**: https://github.com/Coding-Solo/godot-mcp/issues
- **Blender MCP Discord**: https://discord.gg/z5apgR8TFU
- **MCP Community**: https://github.com/modelcontextprotocol

---

**Status**: 🔧 Setup in Progress  
**Date**: October 27, 2025  
**Ready for**: Cave Crawler Development 🎮

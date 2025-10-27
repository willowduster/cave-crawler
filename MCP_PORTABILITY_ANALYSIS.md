# MCP Server Portability Analysis

**Date**: October 27, 2025  
**Issue**: Blender MCP Server is NOT portable across workstations  
**Solution**: Use Blender automation scripts instead

## 🔍 The Problem

MCP (Model Context Protocol) servers enable AI assistants to control tools, but they have **different portability characteristics** than the tools themselves.

### What IS Portable ✅

| Component | Location | Setup | Cross-Workstation |
|-----------|----------|-------|-------------------|
| Godot Executable | `./bin/` | Copy file | ✅ Fully portable |
| Blender Executable | `./bin/` | Extract folder | ✅ Fully portable |
| Blender Scripts | `./blender_scripts/` | No setup needed | ✅ Fully portable |
| Helper Scripts | `./scripts/` | No setup needed | ✅ Fully portable |
| Game Code | `./scripts/`, `./scenes/` | No setup needed | ✅ Fully portable |

### What is NOT Portable ❌

| Component | Setup Required | Why Not Portable |
|-----------|----------------|------------------|
| **Blender MCP Server** | Manual UI steps | Requires addon installation via Blender UI, clicking "Start Server" button |
| **Godot MCP Server** | npm install + build | Requires Node.js globally, build step per machine |
| **MCP Client Config** | Per-workstation paths | Claude Desktop/Cursor config with absolute paths |

## 🎯 Your Concern: Blender MCP Setup

You're right to be worried! The Blender MCP setup is **NOT portable** because it requires:

### Manual Steps (Every Workstation)

1. **Install Blender addon**:
   ```
   - Open Blender
   - Edit → Preferences → Add-ons
   - Install → Select blender-mcp/addon.py
   - Enable "Blender MCP Socket Server"
   ```

2. **Start server** (every session):
   ```
   - Open Blender
   - Click "Start Server" button in addon
   - Keep Blender running in background
   ```

3. **Configure MCP client** with absolute paths:
   ```json
   "blender": {
     "command": "uv",
     "args": [
       "--directory",
       "C:\\Users\\Ben\\code\\cave-crawler\\blender-mcp",  // ❌ NOT portable
       "run",
       "blender-mcp"
     ]
   }
   ```

### Why This Is a Problem

- ❌ Can't just "clone and run" on a new workstation
- ❌ Requires manual clicking in Blender UI (can't script)
- ❌ Needs Blender running in background (uses ~500MB RAM)
- ❌ Config has hardcoded absolute paths
- ❌ Requires Python environment setup with `uv`
- ❌ Not documented in a "setup script"

## ✅ The Solution: Two Approaches

### Approach 1: Blender Scripts (RECOMMENDED for Portability)

Use the automated Blender scripts for **repeatable, portable asset generation**:

```powershell
# This is FULLY PORTABLE
.\scripts\run_blender.ps1 create_pixel_textures.py
```

**Advantages**:
- ✅ No manual setup required
- ✅ Same output every time
- ✅ Scripts versioned in Git
- ✅ Works on any machine with Blender in `./bin/`
- ✅ No background processes needed
- ✅ Can run in CI/CD pipelines

**Use for**:
- Texture generation (SNES sprites, tiles)
- Batch processing
- Automated builds
- Repeatable asset pipelines

### Approach 2: Blender MCP (for Interactive Workflows)

Keep Blender MCP for **interactive AI-assisted asset creation**:

**Advantages**:
- ✅ AI can create custom 3D models on demand
- ✅ Interactive material editing
- ✅ Real-time feedback

**Use for**:
- One-off custom assets
- Experimenting with designs
- AI-guided modeling sessions

**Accept**:
- ⚠️ NOT portable - requires per-workstation setup
- ⚠️ Setup documentation needed (see MCP_SETUP_GUIDE.md)
- ⚠️ Not versioned (external dependency)

## 📋 Updated Constitutional Requirements

### For Portable Workflows (MUST)

✅ **Use Blender Scripts** for:
- Texture generation
- Tile creation
- Batch processing
- Any repeatable asset generation

```powershell
# Always portable across workstations
.\scripts\run_blender.ps1 <script_name>.py
```

### For Interactive AI Workflows (OPTIONAL)

⚠️ **Use Blender MCP** for:
- One-off custom assets
- AI-assisted modeling
- Experimental designs

⚠️ **Accept**:
- Requires per-workstation manual setup
- Documented in MCP_SETUP_GUIDE.md
- Not required for core development

## 🔧 Practical Workflow

### New Workstation Setup

1. **Clone repository**:
   ```powershell
   git clone https://github.com/willowduster/cave-crawler.git
   cd cave-crawler
   ```

2. **Install portable tools**:
   ```powershell
   # Download Godot 4.5.1+ to ./bin/
   # Download Blender 4.5+ to ./bin/blender-4.5.0-windows-x64/
   ```

3. **You're ready!** (for core development)
   ```powershell
   # Run game
   .\bin\Godot_v4.5.1-stable_win64.exe --path . scenes/generation/procedural_cave.tscn
   
   # Generate textures
   .\scripts\run_blender.ps1 create_pixel_textures.py
   ```

4. **OPTIONAL: Setup Blender MCP** (if you want AI asset creation):
   ```powershell
   # See MCP_SETUP_GUIDE.md for manual setup steps
   # Only needed if you want AI to create custom models
   ```

## 📊 Portability Matrix

| Task | Portable Method | AI-Assisted Method |
|------|----------------|-------------------|
| **Generate SNES textures** | `.\scripts\run_blender.ps1 create_pixel_textures.py` | ❌ Not needed |
| **Generate isometric tiles** | `.\scripts\run_blender.ps1 create_iso_tiles.py` | ❌ Not needed |
| **Run game** | `.\bin\Godot_v4.5.1-stable_win64.exe --path .` | Godot MCP (semi-portable) |
| **Edit scenes** | Open in Godot Editor | Godot MCP (semi-portable) |
| **Create custom 3D model** | Write Blender script | Blender MCP (not portable) ⚠️ |
| **Batch asset generation** | Blender scripts | ❌ Not recommended |

## ✅ Recommendation

**For this project**:

1. **Core asset generation**: Use Blender scripts (portable)
2. **Game development**: Use portable Godot executable
3. **AI assistance**: Optional MCP setup for interactive workflows
4. **Commit to Git**: Scripts, scenes, textures (NOT MCP configs)

**Constitution Update**:
- Blender MCP is **optional** and **not required** for development
- All **repeatable workflows** must use portable scripts
- MCP servers are **development conveniences**, not core dependencies

## 📝 Documentation Updates

Updated the following files to reflect this:

- ✅ `PROJECT_CONSTITUTION.md` - Added MCP portability section
- ✅ `PORTABLE_TOOLING.md` - Added MCP server analysis
- ✅ `MCP_PORTABILITY_ANALYSIS.md` - This document

## 🎉 Summary

**Your concern was valid!** Blender MCP is NOT portable.

**Solution**: 
- ✅ Core workflows use **portable Blender scripts**
- ⚠️ Blender MCP is **optional** for AI-assisted modeling
- ✅ No portability compromise - scripts handle all repeatable tasks
- ⚠️ MCP setup documented but not required

**Bottom Line**: You can clone the repo and start working with just Godot and Blender in `./bin/`. MCP is a bonus, not a requirement.

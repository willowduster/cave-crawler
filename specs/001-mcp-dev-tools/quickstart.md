# Quick Start Guide: MCP Development Tools

**Feature**: 001-mcp-dev-tools  
**Last Updated**: 2025-10-26  
**Target Audience**: Developers setting up MCP servers for Godot, Blender, and GIMP

---

## Overview

This guide walks you through setting up MCP (Model Context Protocol) servers that enable AI-assisted development with Godot Engine, Blender, and GIMP on Windows. By the end of this guide, you'll be able to use AI to create scenes, generate 3D models, and edit sprites directly from your IDE.

**Time to Complete**: 15-30 minutes

---

## Prerequisites

Before you begin, ensure you have:

### Required Software

- ✅ **Windows 10 or 11** (64-bit)
- ✅ **Python 3.11 or later** ([Download](https://www.python.org/downloads/))
- ✅ **Git** ([Download](https://git-scm.com/downloads))
- ✅ **VS Code** with MCP support ([Download](https://code.visualstudio.com/))

### Development Tools (at least one)

- ⬜ **Godot Engine 4.x** ([Download](https://godotengine.org/download))
- ⬜ **Blender 3.x+** ([Download](https://www.blender.org/download/))
- ⬜ **GIMP 2.10+** ([Download](https://www.gimp.org/downloads/))

**Note**: You don't need all three tools installed. MCP servers will only activate for tools you have installed.

### Permissions

- Administrator rights (for Python package installation)
- Write access to the repository directory

---

## Step 1: Clone the Repository

If you haven't already:

```powershell
cd C:\Users\<YourUsername>\code
git clone https://github.com/willowduster/cave-crawler.git
cd cave-crawler
```

---

## Step 2: Install Python Dependencies

Navigate to the MCP servers directory and install required packages:

```powershell
cd mcp-servers
pip install -r requirements.txt
```

**Expected Output**:
```
Successfully installed mcp-0.9.0 pydantic-2.x psutil-5.x ...
```

**Troubleshooting**:
- If `pip` is not found, ensure Python is in your PATH
- Use `python -m pip install -r requirements.txt` as alternative
- Consider using a virtual environment: `python -m venv venv` then `venv\Scripts\activate`

---

## Step 3: Detect Installed Tools

Run the tool detection script to find Godot, Blender, and GIMP:

```powershell
.\scripts\detect-tools.ps1
```

**Expected Output**:
```
Scanning for development tools...

✓ Godot Engine 4.2.1
  Path: C:\Program Files\Godot\godot.exe
  Method: Registry

✓ Blender 3.6.5
  Path: C:\Program Files\Blender Foundation\Blender 3.6\blender.exe
  Method: Common Path

✗ GIMP not found
  Suggestion: Install GIMP or manually specify path in config

Detection results saved to: config\detected-tools.json
```

**If a tool isn't detected**:
1. Verify it's installed correctly
2. Note the installation path
3. You'll manually configure it in the next step

---

## Step 4: Configure MCP Servers

### Option A: Use Auto-Generated Config (Recommended)

If detection found all your tools:

```powershell
copy config\mcp-config.example.json config\mcp-config.json
```

The script automatically updates `mcp-config.json` with detected paths.

### Option B: Manual Configuration

If you need to manually specify tool paths, edit `config\mcp-config.json`:

```json
{
  "version": "1.0.0",
  "servers": [
    {
      "name": "godot",
      "enabled": true,
      "tool_path": "C:\\Path\\To\\godot.exe",  // Update this
      "operations": [],
      "timeout": 30,
      "max_concurrent": 3
    },
    {
      "name": "blender",
      "enabled": true,
      "tool_path": "auto",  // or specify path
      "timeout": 60,
      "max_concurrent": 2
    },
    {
      "name": "gimp",
      "enabled": false,  // Disable if not installed
      "tool_path": "auto",
      "timeout": 20,
      "max_concurrent": 3
    }
  ],
  "logging": {
    "level": "INFO",
    "file_path": "logs/mcp-servers.log",
    "max_file_size": 10485760,
    "rotation_count": 5
  }
}
```

**Configuration Tips**:
- Set `enabled: false` for tools you don't have installed
- Use double backslashes (`\\`) in Windows paths
- `tool_path: "auto"` triggers automatic detection
- Adjust `timeout` if operations frequently timeout
- `max_concurrent` controls how many operations run simultaneously

---

## Step 5: Validate Configuration

Verify your configuration is valid:

```powershell
.\scripts\validate-config.ps1
```

**Expected Output**:
```
Validating MCP configuration...

✓ Configuration schema valid
✓ All tool paths accessible
✓ Logging directory writable
✓ No conflicts detected

Configuration is ready!
```

**If validation fails**:
- Check error message for specific issue
- Verify file paths use correct format
- Ensure directories exist and are writable

---

## Step 6: Start MCP Servers

Start all enabled MCP servers:

```powershell
.\scripts\start-all-servers.ps1
```

**Expected Output**:
```
Starting MCP servers...

[Godot] Starting server...
[Godot] ✓ Server running (PID: 12345)

[Blender] Starting server...
[Blender] ✓ Server running (PID: 12346)

[GIMP] Skipped (disabled in config)

All servers started successfully!
Log file: logs\mcp-servers.log
```

**Servers run in the background**. They'll continue running until you stop them or restart your computer.

---

## Step 7: Verify MCP Integration

### Test Godot Operations

From VS Code, try asking AI:

```
List all scenes in the Godot project
```

**Expected**: AI should return a list of `.tscn` files from your `cave-crawler` project.

### Test Blender Operations

```
Create a simple cube in Blender and export it as GLTF
```

**Expected**: AI should create a cube and save it to your specified location.

### Test GIMP Operations

```
Create a 256x256 sprite with transparent background in GIMP
```

**Expected**: AI should create an image and save it as PNG.

---

## Step 8: Stop MCP Servers (When Done)

When you're finished working:

```powershell
.\scripts\stop-all-servers.ps1
```

**Expected Output**:
```
Stopping MCP servers...

[Godot] Stopping server (PID: 12345)...
[Godot] ✓ Server stopped

[Blender] Stopping server (PID: 12346)...
[Blender] ✓ Server stopped

All servers stopped.
```

---

## Common Issues & Solutions

### Issue: "Python not found"

**Solution**: 
1. Install Python 3.11+ from python.org
2. During installation, check "Add Python to PATH"
3. Restart PowerShell

### Issue: "Tool not detected"

**Solution**:
1. Verify tool is installed and runs
2. Find installation path (e.g., `C:\Program Files\Godot\godot.exe`)
3. Manually set `tool_path` in `mcp-config.json`
4. Run `.\scripts\validate-config.ps1` again

### Issue: "Permission denied" when starting servers

**Solution**:
1. Run PowerShell as Administrator
2. Or change logging directory to a user-writable location in config

### Issue: Operations timeout frequently

**Solution**:
1. Increase `timeout` value in `mcp-config.json`
2. For Blender specifically, increase to 90-120 seconds for complex models
3. Restart servers after config changes

### Issue: "Server already running"

**Solution**:
```powershell
.\scripts\stop-all-servers.ps1
.\scripts\start-all-servers.ps1
```

### Issue: Can't find log files

**Logs Location**: `mcp-servers\logs\mcp-servers.log`

**View recent logs**:
```powershell
Get-Content logs\mcp-servers.log -Tail 50
```

---

## Next Steps

### Explore Operations

Check the operation reference docs:
- `docs/operation-reference.md` - Complete list of available operations
- `specs/001-mcp-dev-tools/contracts/` - Detailed operation schemas

### Advanced Configuration

- **Enable/disable specific operations**: Edit `operations` array in config
- **Performance tuning**: Adjust `max_concurrent` and `timeout`
- **Custom logging**: Change log level to `DEBUG` for detailed output

### Development Workflow

1. Start MCP servers at beginning of work session
2. Use AI to create/modify game assets
3. Verify changes in tools (Godot, Blender, GIMP)
4. Stop servers when done to free resources

### Integration with VS Code

- Install MCP extension for VS Code (if available)
- Configure workspace settings to auto-start servers
- Set up keyboard shortcuts for common operations

---

## Getting Help

### Check Logs

Always check logs first when something goes wrong:

```powershell
Get-Content logs\mcp-servers.log -Tail 100
```

### Documentation

- **Full Documentation**: `mcp-servers/docs/`
- **Troubleshooting Guide**: `mcp-servers/docs/troubleshooting.md`
- **Operation Reference**: `mcp-servers/docs/operation-reference.md`

### Report Issues

If you encounter bugs:
1. Check logs for error messages
2. Try reproducing with minimal example
3. Report in GitHub Issues with:
   - Error message
   - Log excerpt
   - Tool versions
   - Steps to reproduce

---

## Summary

You've successfully set up MCP servers for AI-assisted game development! You can now:

✅ Let AI create and modify Godot scenes and scripts  
✅ Generate 3D models in Blender via AI commands  
✅ Create and edit sprites in GIMP through AI  
✅ Manage all servers from a single configuration  

**Start developing** with AI assistance and enjoy the productivity boost! 🚀

---

**Quick Reference Card**

```powershell
# Start servers
.\scripts\start-all-servers.ps1

# Stop servers
.\scripts\stop-all-servers.ps1

# Validate config
.\scripts\validate-config.ps1

# Detect tools
.\scripts\detect-tools.ps1

# View logs
Get-Content logs\mcp-servers.log -Tail 50
```

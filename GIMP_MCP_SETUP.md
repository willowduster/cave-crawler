# GIMP MCP Setup Guide

## Status
✅ GIMP 3 found at: `C:\Users\Ben\AppData\Local\Programs\GIMP 3\bin\gimp-3.exe`
✅ GIMP MCP server cloned from: https://github.com/libreearth/gimp-mcp
✅ GIMP MCP plugin copied to: `C:\Users\Ben\AppData\Roaming\GIMP\3.0\plug-ins\gimp_mcp_server.py`
⚠️ GIMP MCP client needs dependency fixes

## Architecture

The GIMP MCP server works similarly to Blender MCP:
1. **GIMP Plugin** (`gimp_mcp_server.py`) - Runs inside GIMP, listens on localhost:9876
2. **MCP Client** (`gimp_mcp_client.py`) - Connects to GIMP plugin via socket, exposes MCP tools

## Installation Steps

### Step 1: Install the GIMP Plugin

The plugin has already been copied to GIMP's plugin directory:
- Location: `C:\Users\Ben\AppData\Roaming\GIMP\3.0\plug-ins\gimp_mcp_server.py`

To activate it in GIMP:

1. **Launch GIMP 3** (should be running now)
2. Go to **Filters > Development > Start MCP Server**
3. The server will start listening on `localhost:9876`
4. Check the terminal/console for confirmation: "Server listening on localhost:9876"

### Step 2: Fix MCP Client Dependencies

The MCP client (`gimp_mcp_client.py`) needs to be updated to work with the current FastMCP API.

**Current Issues:**
- FastMCP initialization doesn't accept `description` parameter
- Need to install correct `mcp` package version

**Temporary Workaround:**
Since the GIMP MCP is still in development, you can:
1. Run the plugin inside GIMP (Step 1)
2. Manually test the connection with Python scripts
3. Wait for the GIMP MCP project to mature

### Step 3: Configure in Claude/Cursor (When Fixed)

Once the client is working, add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gimp": {
      "command": "uvx",
      "args": ["gimp-mcp"]
    }
  }
}
```

For Cursor (Windows):
```json
{
  "mcpServers": {
    "gimp": {
      "command": "cmd",
      "args": ["/c", "uvx", "gimp-mcp"]
    }
  }
}
```

## Available Features (When Working)

The GIMP MCP server will provide:
- **List images**: Get all open images in GIMP
- **Get image info**: Retrieve image dimensions, layers, etc.
- **Apply effects**: Gaussian blur, filters, etc.
- **Call any GIMP API**: Dynamic access to GIMP's Python-Fu API
- **Layer manipulation**: Create, modify, delete layers
- **File operations**: Load/save images

## Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| GIMP 3 | ✅ Installed | C:\Users\Ben\AppData\Local\Programs\GIMP 3\ |
| GIMP Plugin | ✅ Copied | Needs manual activation in GIMP |
| MCP Client | ⚠️ Needs Fix | FastMCP API compatibility issues |
| Integration | ⏳ Pending | Waiting for client fixes |

## Alternative: Direct GIMP Python-Fu

While waiting for GIMP MCP to mature, you can:
1. Use GIMP's built-in Python-Fu console: **Filters > Python-Fu > Console**
2. Write standalone Python scripts that use `gimp` module
3. Create GIMP plugins directly in Python

## Recommendation

**For now, focus on:**
- ✅ Godot MCP (fully working and tested)
- ✅ Blender MCP (fully working and tested)
- ⏭️ GIMP MCP (plugin installed, but client needs development)

The GIMP MCP project is newer and still maturing. The plugin is installed and ready, but the MCP client needs updates to work with current MCP libraries.

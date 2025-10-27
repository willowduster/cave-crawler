# Blender MCP Setup Guide

## Status
✅ Blender 4.5 found at: `C:\Program Files\Blender Foundation\Blender 4.5\blender.exe`
✅ Blender MCP server installed and running via `uvx blender-mcp`
✅ Configuration added to `claude_desktop_config.json`

## Install Blender Addon (Required)

The Blender MCP server communicates with Blender through a socket-based addon. You need to install this addon in Blender:

### Step 1: Install the Addon

1. **Open Blender** (should already be running)
2. Go to **Edit > Preferences**
3. Select **Add-ons** from the left panel
4. Click **Install...** button at the top
5. Navigate to: `C:\Users\Ben\code\cave-crawler\blender-mcp\addon.py`
6. Select the file and click **Install Add-on**

### Step 2: Enable the Addon

1. In the Add-ons preferences, search for "**Blender MCP**"
2. Check the box next to "Interface: Blender MCP" to enable it
3. The addon should now appear in the 3D Viewport sidebar

### Step 3: Start the MCP Server in Blender

1. In Blender, press **N** to open the sidebar (if not already open)
2. Click the **BlenderMCP** tab
3. You should see:
   - Host: localhost
   - Port: 9876
   - Status: Server Stopped
4. Click **Start Server** button
5. Status should change to "Server Running"

### Step 4: Test the Connection

The Blender MCP server (running via `uvx blender-mcp`) should now be able to communicate with Blender through the socket connection.

## Available Features

Once configured in Claude Desktop or Cursor, the AI assistant can:

- **Create and manipulate 3D objects** in Blender
- **Apply materials and colors**
- **Inspect scene information**
- **Execute Python code** in Blender
- **Download Poly Haven assets**
- **Generate 3D models** using Hyper3D Rodin
- **View screenshots** of the Blender viewport
- **Search and download Sketchfab models**

## Troubleshooting

### Server Won't Connect
- Make sure the addon is enabled in Blender
- Verify the server is running in the BlenderMCP sidebar tab
- Check that the port 9876 is not blocked by firewall
- Restart Blender if needed

### Addon Not Showing
- Make sure you installed `addon.py` from the correct location
- Check that the addon is enabled (checkbox is checked)
- Restart Blender

## Configuration Files

### Claude Desktop Config
Location: `C:\Users\Ben\AppData\Roaming\Claude\claude_desktop_config.json`

The configuration has been prepared in: `claude_desktop_config.json`

### Cursor Config
Follow the instructions in: `CURSOR_MCP_CONFIG.md`

For Windows, add this server:
```json
{
  "mcpServers": {
    "blender": {
      "command": "cmd",
      "args": [
        "/c",
        "uvx",
        "blender-mcp"
      ]
    }
  }
}
```

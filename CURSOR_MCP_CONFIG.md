# Cursor MCP Configuration

## How to Configure in Cursor

1. Open **Cursor Settings** → **Features** → **MCP**
2. Add each server below using the **+ Add New MCP Server** button

---

## Server 1: Filesystem

- **Name**: `filesystem`
- **Type**: `command`
- **Command**: `npx -y @modelcontextprotocol/server-filesystem C:\Users\Ben\code\cave-crawler`

---

## Server 2: Git

- **Name**: `git`
- **Type**: `command`
- **Command**: `uvx mcp-server-git --repository C:\Users\Ben\code\cave-crawler`

---

## Server 3: Godot

- **Name**: `godot`
- **Type**: `command`
- **Command**: `GODOT_PATH=C:\Users\Ben\code\cave-crawler\bin\Godot_v4.5.1-stable_win64.exe node C:\Users\Ben\code\cave-crawler\godot-mcp\build\index.js`
- **Environment Variables** (optional):
  - `DEBUG=true`

---

## Server 4: Blender

- **Name**: `blender`
- **Type**: `command`
- **Command**: `cmd /c uvx blender-mcp`

**Note**: Before using Blender MCP, you must:
1. Install the Blender addon from `blender-mcp\addon.py`
2. Enable it in Blender preferences
3. Start the MCP server in Blender's sidebar (press N → BlenderMCP tab)

See `BLENDER_MCP_SETUP.md` for detailed instructions.

---

## Alternative: JSON Configuration

If Cursor supports direct JSON config, use:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Ben\\code\\cave-crawler"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "C:\\Users\\Ben\\code\\cave-crawler"]
    },
    "godot": {
      "command": "node",
      "args": ["C:\\Users\\Ben\\code\\cave-crawler\\godot-mcp\\build\\index.js"],
      "env": {
        "GODOT_PATH": "C:\\Users\\Ben\\code\\cave-crawler\\bin\\Godot_v4.5.1-stable_win64.exe",
        "DEBUG": "true"
      }
    },
    "blender": {
      "command": "cmd",
      "args": ["/c", "uvx", "blender-mcp"]
    }
  }
}
```

---

## After Configuration

1. **Restart Cursor**
2. **Verify** MCP servers appear in the tools list
3. **Test** with: "Get Godot version" or "List project files"

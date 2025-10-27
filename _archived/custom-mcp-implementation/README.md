# MCP Development Tools Integration

AI-powered development tool servers for Godot Engine, Blender, and GIMP, enabling seamless AI-assisted game development through the Model Context Protocol (MCP).

## Overview

This project provides MCP servers that allow AI assistants to interact with game development tools:

- **Godot Server**: Create and modify scenes, scripts, and resources
- **Blender Server**: Generate 3D models, apply materials, export GLTF assets
- **GIMP Server**: Create sprites, edit textures, manage layers

## Features

✅ **Unified Configuration**: Manage all MCP servers from a single JSON file  
✅ **Auto-Detection**: Automatically finds installed tools on Windows  
✅ **Safe Operations**: File locking and atomic writes prevent corruption  
✅ **Comprehensive Logging**: Detailed logs for debugging and monitoring  
✅ **Independent Servers**: Each tool runs as a separate MCP server  
✅ **Windows Optimized**: Native support for Windows 10/11  

## Quick Start

### Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Windows 10/11** (64-bit)
- At least one of:
  - **Godot Engine 4.x** - [Download](https://godotengine.org/download)
  - **Blender 3.x+** - [Download](https://www.blender.org/download/)
  - **GIMP 2.10+** - [Download](https://www.gimp.org/downloads/)

### Installation

1. **Install dependencies**:
   ```powershell
   cd mcp-servers
   pip install -r requirements.txt
   ```

2. **Detect installed tools**:
   ```powershell
   .\scripts\detect-tools.ps1
   ```

3. **Configure servers**:
   ```powershell
   copy config\mcp-config.example.json config\mcp-config.json
   # Edit config\mcp-config.json if needed
   ```

4. **Start servers**:
   ```powershell
   .\scripts\start-all-servers.ps1
   ```

For detailed setup instructions, see [Quick Start Guide](../specs/001-mcp-dev-tools/quickstart.md).

## Project Structure

```
mcp-servers/
├── config/              # Configuration files
│   ├── mcp-config.json        # Main configuration (user-editable)
│   ├── mcp-config.schema.json # JSON schema for validation
│   └── detected-tools.json    # Cached tool detection results
├── servers/             # MCP server implementations
│   ├── common/          # Shared utilities
│   ├── godot/           # Godot MCP server
│   ├── blender/         # Blender MCP server
│   └── gimp/            # GIMP MCP server
├── tests/               # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── fixtures/        # Test fixtures
├── docs/                # Documentation
├── scripts/             # Management scripts
└── logs/                # Log files
```

## Usage Examples

### Godot Operations

```python
# AI can now:
- List all scenes in project
- Create new scene files
- Read and modify GDScript files
- Validate script syntax
```

### Blender Operations

```python
# AI can now:
- Create primitive 3D objects
- Apply materials and textures
- Export models as GLTF for Godot
- Generate preview renders
```

### GIMP Operations

```python
# AI can now:
- Create new images with layers
- Apply filters and effects
- Export sprites as PNG with transparency
- Batch process images
```

## Configuration

Edit `config/mcp-config.json` to customize:

- Enable/disable specific servers
- Set tool executable paths
- Adjust operation timeouts
- Configure logging levels
- Set concurrent operation limits

See [Configuration Guide](docs/setup.md) for details.

## Documentation

- **[Quick Start Guide](../specs/001-mcp-dev-tools/quickstart.md)** - Get up and running
- **[Implementation Plan](../specs/001-mcp-dev-tools/plan.md)** - Technical architecture
- **[Operation Reference](docs/operation-reference.md)** - Complete API documentation
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## Development

### Running Tests

```powershell
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=servers --cov-report=html

# Run specific test file
pytest tests/unit/test_config.py
```

### Code Quality

```powershell
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy servers/
```

## Contributing

1. Follow the constitution principles defined in `.specify/memory/constitution.md`
2. Write tests first (TDD approach)
3. Ensure all tests pass before submitting
4. Follow code style (black formatting, type hints)
5. Update documentation as needed

## Architecture

- **MCP Protocol**: Uses official `mcp` Python SDK
- **Server Design**: Independent server per tool (Godot, Blender, GIMP)
- **Tool Integration**: 
  - Godot: Direct file parsing + CLI validation
  - Blender: `bpy` API via headless subprocess
  - GIMP: Python-Fu batch mode execution
- **Safety**: File locking + atomic writes prevent corruption
- **Configuration**: JSON-based with pydantic validation

## Roadmap

- [x] Phase 1: Project setup and structure
- [ ] Phase 2: Core infrastructure and utilities
- [ ] Phase 3: Godot MCP server (MVP)
- [ ] Phase 4: Configuration management (MVP)
- [ ] Phase 5: Blender MCP server
- [ ] Phase 6: GIMP MCP server
- [ ] Phase 7: Polish and optimization

## License

MIT License - See LICENSE file for details

## Support

- **Documentation**: See `docs/` directory
- **Issues**: [GitHub Issues](https://github.com/willowduster/cave-crawler/issues)
- **Logs**: Check `logs/mcp-servers.log` for debugging

---

**Status**: 🚧 In Development (Phase 1 Complete)

Built for the Cave Crawler multiplayer RPG project.

# Implementation Plan: MCP Development Tools Integration

**Branch**: `001-mcp-dev-tools` | **Date**: 2025-10-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-mcp-dev-tools/spec.md`

## Summary

This feature establishes MCP (Model Context Protocol) server infrastructure to enable AI-assisted development with Godot Engine, Blender, and GIMP on Windows. The primary requirement is to provide seamless AI access to game development tools for scene creation, 3D modeling, and 2D art production. The technical approach uses existing MCP server implementations where available, with custom adapters for tool-specific operations, managed through a unified JSON configuration file.

## Technical Context

**Language/Version**: Python 3.11+ (for MCP server scripts and tool adapters)  
**Primary Dependencies**: 
- `mcp` Python package (Model Context Protocol SDK)
- `pydantic` for configuration validation
- `psutil` for process management
- `winreg` for Windows registry access (tool detection)

**Storage**: JSON configuration file for MCP server settings; file-based for tool project files  
**Testing**: `pytest` for unit tests, integration tests with actual tool installations  
**Target Platform**: Windows 10/11 (64-bit)  
**Project Type**: Development tooling infrastructure (not game code)  
**Performance Goals**: 
- Tool detection: <3 seconds on startup
- MCP operation response: <2 seconds for file operations
- Server startup: <5 seconds per tool server

**Constraints**: 
- Must not interfere with manual tool usage
- File operations must be atomic (no partial writes)
- Concurrent request handling without file corruption
- Graceful degradation when tools not installed

**Scale/Scope**: 
- 3 MCP servers (Godot, Blender, GIMP)
- 20+ tool operations across all servers
- Single-user development environment
- Concurrent operation support (up to 5 simultaneous requests)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Scene-Component Architecture ✅ N/A
**Status**: Not applicable - this is tooling infrastructure, not game code.

### II. Network Authority First ✅ N/A
**Status**: Not applicable - MCP servers are local-only (no multiplayer component).

### III. Separation of Game Logic and Presentation ✅ PASS
**Status**: MCP servers are separate from game logic. Tool adapters isolated from configuration management.
**Evidence**: Server architecture separates tool interaction (presentation) from configuration/orchestration (logic).

### IV. Test-Driven Development ✅ PASS
**Status**: TDD required for critical path: tool detection, file operations, error handling.
**Plan**: Write tests first for:
- Tool installation detection
- Configuration validation
- File operation safety (atomic writes, concurrent access)
- Error handling and logging

### V. Performance Budget Compliance ✅ PASS
**Status**: Performance targets defined in Technical Context.
**Metrics**: Tool detection <3s, operations <2s, startup <5s per server.

### VI. Data-Driven Design ✅ PASS
**Status**: MCP server configuration is JSON-based, external to code.
**Evidence**: Tool paths, enabled servers, operation settings all configurable via JSON.

### VII. Graceful Degradation ✅ PASS
**Status**: System handles missing tools, connection failures, and crashes gracefully.
**Evidence**: 
- Clear error messages when tools not found (FR-017)
- Tool detection validates executables before starting servers (FR-020)
- Operation logs for troubleshooting (FR-015)

### VIII-XV. RPG-Specific Principles ✅ N/A
**Status**: Not applicable - this is development infrastructure, not gameplay features.

**Overall Assessment**: ✅ **GATE PASSED** - All applicable constitution principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-dev-tools/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0: Tool detection methods, MCP SDK research
├── data-model.md        # Phase 1: Configuration schema, server state model
├── quickstart.md        # Phase 1: Setup guide for team members
├── contracts/           # Phase 1: MCP operation schemas
│   ├── godot-operations.json
│   ├── blender-operations.json
│   └── gimp-operations.json
├── checklists/
│   └── requirements.md  # Already created
└── spec.md              # Already created
```

### Source Code (repository root)

```text
mcp-servers/                     # NEW: MCP server infrastructure (outside cave-crawler/)
├── config/
│   ├── mcp-config.json          # Unified MCP server configuration
│   ├── mcp-config.schema.json   # JSON schema for validation
│   └── mcp-config.example.json  # Example config with comments
├── servers/
│   ├── godot/
│   │   ├── server.py            # Godot MCP server entry point
│   │   ├── operations.py        # Godot-specific operations
│   │   ├── detector.py          # Godot installation detection
│   │   └── __init__.py
│   ├── blender/
│   │   ├── server.py            # Blender MCP server entry point
│   │   ├── operations.py        # Blender-specific operations (bpy wrapper)
│   │   ├── detector.py          # Blender installation detection
│   │   └── __init__.py
│   ├── gimp/
│   │   ├── server.py            # GIMP MCP server entry point
│   │   ├── operations.py        # GIMP-specific operations (script-fu/python-fu)
│   │   ├── detector.py          # GIMP installation detection
│   │   └── __init__.py
│   └── common/
│       ├── base_server.py       # Shared MCP server base class
│       ├── detector_base.py     # Base tool detection logic
│       ├── logger.py            # Unified logging
│       └── __init__.py
├── tests/
│   ├── unit/
│   │   ├── test_config.py
│   │   ├── test_godot_detector.py
│   │   ├── test_blender_detector.py
│   │   └── test_gimp_detector.py
│   ├── integration/
│   │   ├── test_godot_operations.py
│   │   ├── test_blender_operations.py
│   │   └── test_gimp_operations.py
│   └── fixtures/
│       ├── mock_godot_project/
│       ├── mock_blender_files/
│       └── mock_gimp_files/
├── docs/
│   ├── setup.md                 # Installation and setup guide
│   ├── troubleshooting.md       # Common issues and solutions
│   └── operation-reference.md   # Full operation catalog
├── scripts/
│   ├── start-all-servers.ps1    # Start all MCP servers
│   ├── stop-all-servers.ps1     # Stop all MCP servers
│   ├── validate-config.ps1      # Validate configuration file
│   └── detect-tools.ps1         # Standalone tool detection
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project metadata and dependencies
└── README.md                   # Overview and quick start

cave-crawler/                    # Existing game project (unchanged)
└── [existing structure]         # Game code remains separate
```

**Structure Decision**: MCP servers are infrastructure supporting game development, not part of the game itself. They live in a sibling directory (`mcp-servers/`) alongside `cave-crawler/` at the repository root. This separation:
- Keeps game code clean (no dev tooling mixed in)
- Allows independent versioning of MCP infrastructure
- Enables reuse across multiple game projects if needed
- Follows "separation of concerns" principle from constitution

## Complexity Tracking

> **No constitution violations requiring justification.**

All applicable constitution principles are satisfied without complexity trade-offs.

---

# Phase 0: Outline & Research

## Research Tasks

### R1: MCP Protocol Implementation Options
**Question**: Which MCP SDK/framework should we use for Python-based servers?

**Research Areas**:
- Official MCP Python SDK availability and maturity
- Alternative MCP implementations (if official SDK limited)
- Server lifecycle management patterns
- Client-server communication mechanisms (stdio, HTTP, WebSocket)
- Error handling and logging best practices in MCP

**Decision Criteria**:
- Active maintenance and documentation
- Windows compatibility
- Python 3.11+ support
- Ease of defining custom operations

### R2: Godot Project File Interaction
**Question**: How can Python scripts read/write Godot project files safely?

**Research Areas**:
- Godot project file formats (.tscn, .tres, .gd)
- Safe file parsing libraries (avoiding full Godot engine dependency)
- Scene file modification without corruption
- GDScript syntax parsing (for script operations)
- Godot CLI capabilities for file generation

**Decision Criteria**:
- No Godot engine runtime required
- Atomic file operations
- Maintains file format integrity
- Handles Godot 4.x format changes

### R3: Blender Headless Automation on Windows
**Question**: How to run Blender operations in background without GUI?

**Research Areas**:
- Blender Python API (`bpy`) usage patterns
- Headless Blender execution on Windows (`--background` flag)
- Blender script execution via command-line
- GLTF export from Python scripts
- Process management for long-running Blender instances

**Decision Criteria**:
- Reliable headless operation on Windows
- Clean process cleanup (no zombie processes)
- Export quality matches GUI exports
- Performance acceptable for small-to-medium models

### R4: GIMP Scripting for Automation
**Question**: What's the best approach for automating GIMP operations?

**Research Areas**:
- GIMP Python-Fu vs. Script-Fu
- Batch mode operation (`gimp -i -b`)
- PDB (Procedural Database) function catalog
- Layer manipulation and export operations
- GIMP 2.10 vs 3.0 scripting differences (if relevant)

**Decision Criteria**:
- Windows compatibility
- PNG export with transparency support
- Layer manipulation capabilities
- Batch execution reliability

### R5: Windows Tool Detection Strategies
**Question**: How to reliably detect tool installations on Windows?

**Research Areas**:
- Windows Registry keys for application detection
- Common installation paths (Program Files, AppData)
- PATH environment variable scanning
- Version detection from executable metadata
- Handling multiple installations (e.g., Steam vs. standalone Godot)

**Decision Criteria**:
- Reliability across Windows 10/11
- Handles non-standard installation paths
- Detects tool versions accurately
- Minimal false positives/negatives

### R6: Concurrent File Access Patterns
**Question**: How to prevent file corruption when multiple MCP operations run simultaneously?

**Research Areas**:
- File locking mechanisms in Python (Windows-compatible)
- Atomic write patterns (write-to-temp, rename)
- Queue-based operation serialization
- Read-write lock implementations
- Race condition prevention strategies

**Decision Criteria**:
- No file corruption risk
- Minimal performance overhead
- Clear error messages on lock contention
- Compatible with external tool file watchers (Godot's auto-reload)

**Output File**: research.md (will contain findings and decisions for all R1-R6)

---

# Phase 1: Design & Contracts

## Prerequisites
- `research.md` complete with all technology decisions documented
- All NEEDS CLARIFICATION items resolved

## Data Model (`data-model.md`)

### Entity 1: MCP Server Configuration
**Purpose**: Defines settings for all MCP servers in unified JSON file.

**Schema**:
```
MCPConfiguration:
  - version: string (config schema version, e.g., "1.0.0")
  - servers: ServerConfig[]
  - logging: LoggingConfig
  
ServerConfig:
  - name: string (godot|blender|gimp)
  - enabled: boolean
  - tool_path: string (path to executable, or "auto" for detection)
  - operations: string[] (list of enabled operation names)
  - timeout: integer (operation timeout in seconds)
  - max_concurrent: integer (max simultaneous operations)
  
LoggingConfig:
  - level: string (DEBUG|INFO|WARN|ERROR)
  - file_path: string (log file location)
  - max_file_size: integer (bytes)
  - rotation_count: integer (number of backup logs)
```

**Validation Rules**:
- `version` must be valid semver string
- `servers` array must contain at least one entry
- `server.name` must be unique within array
- `tool_path` must be valid Windows path or "auto"
- `timeout` must be 5-300 seconds
- `max_concurrent` must be 1-10

**Relationships**: Configuration → N ServerConfigs

### Entity 2: Tool Installation
**Purpose**: Represents detected tool installation with metadata.

**Schema**:
```
ToolInstallation:
  - tool_name: string (godot|blender|gimp)
  - executable_path: string (full path to .exe)
  - version: string (detected version, e.g., "4.2.1")
  - install_directory: string (base installation folder)
  - detection_method: string (registry|path|manual)
  - is_valid: boolean (executable exists and runs)
  - detected_at: timestamp
```

**State Transitions**: 
- Unknown → Detected (tool found)
- Detected → Validated (executable confirmed working)
- Validated → Invalid (executable stops working)

### Entity 3: MCP Operation Request
**Purpose**: Represents a single operation requested through MCP protocol.

**Schema**:
```
MCPOperationRequest:
  - operation_id: uuid
  - server_name: string (godot|blender|gimp)
  - operation_type: string (read_file|create_scene|export_model|etc)
  - parameters: dict (operation-specific params)
  - requested_at: timestamp
  - timeout: integer (seconds)
  - priority: integer (0-10, higher = more urgent)
```

**Relationships**: Request → 1 ServerConfig

### Entity 4: Operation Log Entry
**Purpose**: Records MCP operation execution for debugging and auditing.

**Schema**:
```
OperationLogEntry:
  - log_id: uuid
  - operation_id: uuid (links to MCPOperationRequest)
  - server_name: string
  - operation_type: string
  - status: string (queued|running|success|error|timeout)
  - started_at: timestamp
  - completed_at: timestamp (null if still running)
  - duration_ms: integer
  - error_message: string (null if success)
  - stack_trace: string (null if success)
```

**State Transitions**:
- Queued → Running (operation starts)
- Running → Success (operation completes)
- Running → Error (operation fails)
- Running → Timeout (operation exceeds time limit)

## API Contracts (`/contracts/`)

### Godot Operations Contract (`godot-operations.json`)

Defines MCP operations for Godot Engine interaction:

**Operations**:
1. `list_project_files`: Returns project structure (scenes, scripts, resources)
2. `read_scene`: Reads .tscn file content
3. `read_script`: Reads .gd file content
4. `create_scene`: Creates new .tscn file from template
5. `create_script`: Creates new .gd file with boilerplate
6. `update_script`: Modifies existing GDScript file
7. `validate_syntax`: Checks GDScript syntax without running
8. `list_resources`: Lists .tres resource files

**Contract Schema** (OpenAPI-style):
```json
{
  "operation": "read_scene",
  "parameters": {
    "scene_path": {
      "type": "string",
      "description": "Relative path from project root to .tscn file",
      "required": true,
      "example": "scenes/player/player.tscn"
    }
  },
  "returns": {
    "scene_content": {
      "type": "string",
      "description": "Raw .tscn file content"
    },
    "node_tree": {
      "type": "object",
      "description": "Parsed scene node hierarchy"
    }
  },
  "errors": [
    "FileNotFound: scene_path does not exist",
    "InvalidFormat: file is not valid .tscn",
    "PermissionDenied: cannot read file"
  ]
}
```

### Blender Operations Contract (`blender-operations.json`)

Defines MCP operations for Blender 3D modeling:

**Operations**:
1. `create_primitive`: Creates basic 3D shape (cube, sphere, cylinder, etc.)
2. `modify_object`: Changes object properties (location, rotation, scale)
3. `apply_material`: Adds/modifies material properties
4. `export_gltf`: Exports scene/object as GLTF 2.0
5. `import_reference`: Imports reference image/model
6. `list_objects`: Returns all objects in current scene
7. `execute_script`: Runs custom bpy Python script
8. `render_preview`: Generates preview render (for thumbnails)

**Contract Schema Example**:
```json
{
  "operation": "export_gltf",
  "parameters": {
    "output_path": {
      "type": "string",
      "description": "Full path for .gltf/.glb file",
      "required": true
    },
    "format": {
      "type": "string",
      "enum": ["gltf", "glb"],
      "default": "glb"
    },
    "include_animations": {
      "type": "boolean",
      "default": true
    },
    "selection_only": {
      "type": "boolean",
      "default": false,
      "description": "Export only selected objects"
    }
  },
  "returns": {
    "file_path": "string",
    "file_size_bytes": "integer",
    "export_warnings": "string[]"
  },
  "errors": [
    "InvalidPath: output_path not writable",
    "ExportFailed: GLTF exporter error",
    "NoObjects: nothing to export"
  ]
}
```

### GIMP Operations Contract (`gimp-operations.json`)

Defines MCP operations for GIMP image editing:

**Operations**:
1. `create_image`: Creates new image with dimensions
2. `open_image`: Opens existing image file
3. `add_layer`: Adds new layer to image
4. `apply_filter`: Applies filter/effect to layer
5. `export_png`: Exports image as PNG with transparency
6. `resize_image`: Resizes canvas or layer
7. `merge_layers`: Flattens visible layers
8. `get_image_info`: Returns dimensions, layers, format

**Contract Schema Example**:
```json
{
  "operation": "create_image",
  "parameters": {
    "width": {
      "type": "integer",
      "min": 1,
      "max": 8192,
      "required": true
    },
    "height": {
      "type": "integer",
      "min": 1,
      "max": 8192,
      "required": true
    },
    "background_color": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$",
      "default": "#FFFFFF"
    },
    "has_alpha": {
      "type": "boolean",
      "default": true,
      "description": "Include alpha channel for transparency"
    }
  },
  "returns": {
    "image_id": "integer",
    "dimensions": {"width": "integer", "height": "integer"}
  },
  "errors": [
    "InvalidDimensions: width or height out of range",
    "MemoryError: image too large to create"
  ]
}
```

## Quick Start Guide (`quickstart.md`)

**Content Outline**:
1. **Prerequisites**: Windows version, Python version, tool installations
2. **Installation Steps**:
   - Clone repository
   - Install Python dependencies (`pip install -r mcp-servers/requirements.txt`)
   - Run tool detection script
   - Configure `mcp-config.json`
3. **Verification**:
   - Start individual server (test mode)
   - Execute sample operation
   - Check logs
4. **Common Issues**: Tool not found, permission errors, port conflicts
5. **Next Steps**: Integration with VS Code, advanced configuration

## Agent Context Update

**Action**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType copilot`

**Expected Changes**:
- Add MCP server technologies to context (Python, MCP SDK, tool APIs)
- Document new directory structure (`mcp-servers/`)
- Preserve existing game development context

---

# Phase 2: Task Breakdown

**Status**: NOT EXECUTED BY `/speckit.plan`

Task breakdown is handled by the separate `/speckit.tasks` command, which will:
- Generate task list from this plan
- Create development checklist
- Define test coverage requirements
- Output to `specs/001-mcp-dev-tools/tasks.md`

**Note**: Run `/speckit.tasks` after this plan is reviewed and approved.

---

# Implementation Notes

## Tool-Specific Considerations

### Godot
- `.tscn` files are text-based (easy to parse/modify)
- `.tres` files are also text-based (resources)
- GDScript syntax is Python-like (can use Python parsers with adaptations)
- Godot CLI supports `--headless` mode (no editor GUI)
- File watching: Godot auto-reloads changed files

### Blender
- `bpy` API is comprehensive but requires Blender runtime
- Headless mode: `blender --background --python script.py`
- GLTF exporter: built-in addon, reliable
- Process management: use subprocess with timeout
- Windows-specific: handle path spaces, use `shell=False`

### GIMP
- Python-Fu available in GIMP 2.10 (may change in 3.0)
- Batch mode: `gimp -i -b '(python-fu-...)'`
- PDB functions: well-documented but verbose syntax
- File locking: GIMP creates lock files (.xcf.lock)
- Export: use `pdb.file_png_save_defaults` for PNG

## Testing Strategy

### Unit Tests (TDD Required)
1. **Configuration Validation**: Test JSON schema validation, required fields, value ranges
2. **Tool Detection**: Mock registry, file system, PATH to test detection logic
3. **Error Handling**: Test each error scenario (tool not found, invalid paths, etc.)
4. **Logging**: Verify log entries created correctly

### Integration Tests
1. **Godot Operations**: Require Godot installed; test real file operations
2. **Blender Operations**: Require Blender installed; test headless execution
3. **GIMP Operations**: Require GIMP installed; test batch mode
4. **Concurrent Operations**: Test file locking and queue management

### Manual Testing
1. **End-to-End Workflows**: AI creates scene → modifies script → exports model
2. **Error Recovery**: Kill server mid-operation, verify graceful restart
3. **Tool Updates**: Verify detection still works after tool version upgrade

## Security Considerations

- **Path Validation**: Prevent directory traversal attacks in file paths
- **Command Injection**: Sanitize all inputs to tool executables
- **Resource Limits**: Timeout and memory limits on tool operations
- **Logging**: Don't log sensitive data (file contents, user paths beyond necessary)

## Future Enhancements (Out of Scope for v1)

- Real-time sync: Watch tool GUI changes and sync to MCP state
- Multi-project support: Manage multiple Godot projects simultaneously
- Advanced Blender: Rigging, complex animations, shader editing
- Advanced GIMP: Batch processing, plugin execution, advanced filters
- macOS/Linux support: Extend tool detection and operations
- Performance optimization: Persistent tool processes (avoid startup overhead)

---

# Next Steps

1. ✅ Review and approve this implementation plan
2. ⏭️ Execute Phase 0: Run research tasks, document findings in `research.md`
3. ⏭️ Execute Phase 1: Create `data-model.md`, contracts, `quickstart.md`
4. ⏭️ Run `/speckit.tasks` to generate task breakdown and checklist
5. ⏭️ Begin TDD implementation following task order

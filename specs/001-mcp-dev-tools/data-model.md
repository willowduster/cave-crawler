# Data Model: MCP Development Tools Integration

**Date**: 2025-10-26  
**Feature**: 001-mcp-dev-tools  
**Status**: Complete

This document defines the data structures, schemas, and relationships for the MCP development tools integration system.

---

## Configuration Data Model

### MCP Configuration Schema

**Purpose**: Central configuration for all MCP servers, tool detection, and operational settings.

**File**: `mcp-servers/config/mcp-config.json`

**JSON Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["version", "servers", "logging"],
  "properties": {
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Configuration schema version (semver)"
    },
    "servers": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/definitions/ServerConfig"
      }
    },
    "logging": {
      "$ref": "#/definitions/LoggingConfig"
    }
  },
  "definitions": {
    "ServerConfig": {
      "type": "object",
      "required": ["name", "enabled", "tool_path"],
      "properties": {
        "name": {
          "type": "string",
          "enum": ["godot", "blender", "gimp"]
        },
        "enabled": {
          "type": "boolean",
          "description": "Whether this server should start"
        },
        "tool_path": {
          "type": "string",
          "description": "Path to tool executable or 'auto' for detection"
        },
        "operations": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Enabled operation names (empty = all)"
        },
        "timeout": {
          "type": "integer",
          "minimum": 5,
          "maximum": 300,
          "default": 30,
          "description": "Operation timeout in seconds"
        },
        "max_concurrent": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10,
          "default": 3,
          "description": "Max simultaneous operations"
        }
      }
    },
    "LoggingConfig": {
      "type": "object",
      "required": ["level", "file_path"],
      "properties": {
        "level": {
          "type": "string",
          "enum": ["DEBUG", "INFO", "WARN", "ERROR"]
        },
        "file_path": {
          "type": "string",
          "description": "Log file path (absolute or relative)"
        },
        "max_file_size": {
          "type": "integer",
          "minimum": 1024,
          "default": 10485760,
          "description": "Max log file size in bytes (10MB default)"
        },
        "rotation_count": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10,
          "default": 5,
          "description": "Number of rotated log files to keep"
        }
      }
    }
  }
}
```

**Example Configuration**:
```json
{
  "version": "1.0.0",
  "servers": [
    {
      "name": "godot",
      "enabled": true,
      "tool_path": "auto",
      "operations": [],
      "timeout": 30,
      "max_concurrent": 3
    },
    {
      "name": "blender",
      "enabled": true,
      "tool_path": "C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe",
      "operations": ["create_primitive", "export_gltf"],
      "timeout": 60,
      "max_concurrent": 2
    },
    {
      "name": "gimp",
      "enabled": false,
      "tool_path": "auto",
      "operations": [],
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

---

## Tool Installation Data Model

### ToolInstallation Class

**Purpose**: Represents a detected tool installation with metadata and validation status.

**Python Class Definition**:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class DetectionMethod(Enum):
    REGISTRY = "registry"
    COMMON_PATH = "common_path"
    ENVIRONMENT_PATH = "path"
    MANUAL = "manual"
    CONFIG = "config"

@dataclass
class ToolInstallation:
    tool_name: str              # "godot" | "blender" | "gimp"
    executable_path: str        # Full path to .exe
    version: str                # e.g., "4.2.1"
    install_directory: str      # Base installation folder
    detection_method: DetectionMethod
    is_valid: bool              # Executable exists and runs
    detected_at: datetime
    validation_error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "tool_name": self.tool_name,
            "executable_path": self.executable_path,
            "version": self.version,
            "install_directory": self.install_directory,
            "detection_method": self.detection_method.value,
            "is_valid": self.is_valid,
            "detected_at": self.detected_at.isoformat(),
            "validation_error": self.validation_error
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ToolInstallation':
        """Deserialize from dictionary."""
        return cls(
            tool_name=data["tool_name"],
            executable_path=data["executable_path"],
            version=data["version"],
            install_directory=data["install_directory"],
            detection_method=DetectionMethod(data["detection_method"]),
            is_valid=data["is_valid"],
            detected_at=datetime.fromisoformat(data["detected_at"]),
            validation_error=data.get("validation_error")
        )
```

**State Transitions**:
```
Unknown → Detected: Tool found during detection scan
Detected → Validated: Executable confirmed working (--version succeeds)
Validated → Invalid: Executable no longer works (file moved, permissions changed)
Invalid → Validated: Issue resolved, executable working again
```

**Persistence**:
Tool installations are cached in `mcp-servers/config/detected-tools.json`:
```json
{
  "last_scan": "2025-10-26T10:30:00Z",
  "tools": {
    "godot": {
      "tool_name": "godot",
      "executable_path": "C:\\Program Files\\Godot\\godot.exe",
      "version": "4.2.1.stable",
      "install_directory": "C:\\Program Files\\Godot",
      "detection_method": "registry",
      "is_valid": true,
      "detected_at": "2025-10-26T10:30:00Z",
      "validation_error": null
    }
  }
}
```

---

## MCP Operation Data Model

### MCPOperationRequest Class

**Purpose**: Represents a single operation request through MCP protocol.

**Python Class Definition**:
```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4, UUID
from typing import Any, Dict

@dataclass
class MCPOperationRequest:
    operation_id: UUID = field(default_factory=uuid4)
    server_name: str = ""       # "godot" | "blender" | "gimp"
    operation_type: str = ""    # e.g., "read_file", "create_scene"
    parameters: Dict[str, Any] = field(default_factory=dict)
    requested_at: datetime = field(default_factory=datetime.now)
    timeout: int = 30           # Seconds
    priority: int = 5           # 0-10, higher = more urgent
    
    def to_dict(self) -> dict:
        return {
            "operation_id": str(self.operation_id),
            "server_name": self.server_name,
            "operation_type": self.operation_type,
            "parameters": self.parameters,
            "requested_at": self.requested_at.isoformat(),
            "timeout": self.timeout,
            "priority": self.priority
        }
```

**Validation Rules**:
- `server_name` must be one of: godot, blender, gimp
- `operation_type` must be supported by specified server
- `parameters` must match operation schema (validated against contracts)
- `timeout` must be 5-300 seconds
- `priority` must be 0-10

---

## Operation Log Data Model

### OperationLogEntry Class

**Purpose**: Records execution details of MCP operations for debugging and auditing.

**Python Class Definition**:
```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum

class OperationStatus(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"

@dataclass
class OperationLogEntry:
    log_id: UUID = field(default_factory=uuid4)
    operation_id: UUID = None
    server_name: str = ""
    operation_type: str = ""
    status: OperationStatus = OperationStatus.QUEUED
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    result_data: Optional[dict] = None
    
    def mark_running(self):
        """Transition to running state."""
        self.status = OperationStatus.RUNNING
        self.started_at = datetime.now()
    
    def mark_success(self, result: dict = None):
        """Transition to success state."""
        self.status = OperationStatus.SUCCESS
        self.completed_at = datetime.now()
        self.duration_ms = int((self.completed_at - self.started_at).total_seconds() * 1000)
        self.result_data = result
    
    def mark_error(self, error: Exception):
        """Transition to error state."""
        self.status = OperationStatus.ERROR
        self.completed_at = datetime.now()
        self.duration_ms = int((self.completed_at - self.started_at).total_seconds() * 1000)
        self.error_message = str(error)
        import traceback
        self.stack_trace = traceback.format_exc()
    
    def mark_timeout(self):
        """Transition to timeout state."""
        self.status = OperationStatus.TIMEOUT
        self.completed_at = datetime.now()
        self.duration_ms = int((self.completed_at - self.started_at).total_seconds() * 1000)
        self.error_message = f"Operation exceeded timeout of {self.duration_ms}ms"
    
    def to_dict(self) -> dict:
        return {
            "log_id": str(self.log_id),
            "operation_id": str(self.operation_id),
            "server_name": self.server_name,
            "operation_type": self.operation_type,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": self.duration_ms,
            "error_message": self.error_message,
            "stack_trace": self.stack_trace,
            "result_data": self.result_data
        }
```

**Log Persistence**:
Logs are written to rotating log files (configured in `logging` section):
- Text format: Human-readable for troubleshooting
- JSON format: Structured for analysis
- Rotation: When file exceeds `max_file_size`, rotate to `.1`, `.2`, etc.

**Example Log Entry** (JSON format):
```json
{
  "log_id": "550e8400-e29b-41d4-a716-446655440000",
  "operation_id": "123e4567-e89b-12d3-a456-426614174000",
  "server_name": "godot",
  "operation_type": "create_scene",
  "status": "success",
  "started_at": "2025-10-26T10:35:22.123Z",
  "completed_at": "2025-10-26T10:35:22.456Z",
  "duration_ms": 333,
  "error_message": null,
  "stack_trace": null,
  "result_data": {
    "scene_path": "scenes/enemy/goblin.tscn",
    "file_size_bytes": 1024
  }
}
```

---

## Server State Data Model

### MCPServerState Class

**Purpose**: Tracks runtime state of each MCP server.

**Python Class Definition**:
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class ServerStatus(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"
    STOPPING = "stopping"

@dataclass
class MCPServerState:
    server_name: str
    status: ServerStatus = ServerStatus.STOPPED
    tool_installation: Optional[ToolInstallation] = None
    started_at: Optional[datetime] = None
    error_message: Optional[str] = None
    active_operations: int = 0
    total_operations: int = 0
    failed_operations: int = 0
    
    def can_accept_operation(self, max_concurrent: int) -> bool:
        """Check if server can accept new operation."""
        return (
            self.status == ServerStatus.RUNNING and
            self.active_operations < max_concurrent
        )
    
    def to_dict(self) -> dict:
        return {
            "server_name": self.server_name,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "error_message": self.error_message,
            "active_operations": self.active_operations,
            "total_operations": self.total_operations,
            "failed_operations": self.failed_operations,
            "tool_installation": self.tool_installation.to_dict() if self.tool_installation else None
        }
```

---

## Entity Relationships

```
MCPConfiguration (1)
  ├── ServerConfig (N)
  └── LoggingConfig (1)

ServerConfig (1) ← uses → ToolInstallation (0..1)

MCPOperationRequest (N) → ServerConfig (1)
MCPOperationRequest (1) → OperationLogEntry (1)

MCPServerState (1) ← manages → ServerConfig (1)
MCPServerState (1) ← tracks → ToolInstallation (1)
```

**Cardinality**:
- 1 Configuration : N Servers
- 1 Server : 0 or 1 Tool Installation (may not be detected)
- 1 Operation Request : 1 Log Entry
- N Operation Requests : 1 Server

---

## File Storage Locations

| Data Type | File Path | Format | Purpose |
|-----------|-----------|--------|---------|
| Configuration | `config/mcp-config.json` | JSON | User-editable settings |
| Detected Tools | `config/detected-tools.json` | JSON | Cached tool detection results |
| Operation Logs | `logs/mcp-servers.log` | Text/JSON | Operation history and errors |
| Server State | In-memory only | Python objects | Runtime state (not persisted) |

---

## Validation Rules Summary

### Configuration Validation
- Version must be valid semver (e.g., "1.0.0")
- At least one server must be defined
- Server names must be unique
- Tool paths must be valid Windows paths or "auto"
- Timeouts: 5-300 seconds
- Max concurrent: 1-10 operations

### Tool Installation Validation
- Executable path must exist
- Executable must run successfully (--version check)
- Version string must be parseable

### Operation Request Validation
- Operation type must exist in server's operation list
- Parameters must match operation contract schema
- Server must be enabled and running
- Timeout must be positive integer

### Log Entry Validation
- All required fields must be present
- Timestamps must be valid ISO 8601
- Status must be valid enum value
- Duration must be non-negative

---

## Implementation Notes

### Thread Safety
- `MCPServerState`: Protected by threading.Lock
- `OperationLogEntry`: Append-only (thread-safe with file locking)
- Configuration: Read-only after initial load (no locking needed)

### Performance Considerations
- Tool detection: Cache results for 5 minutes, re-detect on failure
- Log rotation: Async rotation to avoid blocking operations
- State queries: In-memory reads (no I/O)

### Error Handling
- Invalid config: Fail fast on startup with clear error
- Missing tool: Disable server, log warning, continue
- Operation failure: Log error, return error response, don't crash server

---

**Status**: ✅ Data model complete and ready for implementation

# Research Findings: MCP Development Tools Integration

**Date**: 2025-10-26  
**Feature**: 001-mcp-dev-tools  
**Status**: Complete

This document contains research findings and technology decisions for implementing MCP servers for Godot, Blender, and GIMP on Windows.

---

## R1: MCP Protocol Implementation Options

### Decision: Use Official MCP Python SDK

**Chosen Technology**: `mcp` Python package (official Anthropic SDK)

**Rationale**:
- Official implementation ensures protocol compliance
- Active development and documentation
- Native support for stdio and SSE transport (both useful for different scenarios)
- Clean server/tool abstraction model
- Built-in error handling patterns
- Windows-compatible (tested on Python 3.11+)

**Alternatives Considered**:
1. **Custom MCP implementation**
   - Rejected: Reinventing the wheel, high maintenance burden
   - Protocol may evolve, custom impl would lag
   
2. **Language Server Protocol (LSP) adaptation**
   - Rejected: LSP is text-editor focused, not suitable for general tool automation
   - Would require significant protocol extensions

**Implementation Approach**:
- Use `mcp` package's `Server` class as base for each tool server
- Implement tool-specific operations as MCP "tools" (callable functions)
- Use stdio transport for VS Code integration (standard for MCP)
- Leverage built-in request/response schema validation

**Dependencies**:
```
mcp>=0.9.0
```

---

## R2: Godot Project File Interaction

### Decision: Direct Text File Parsing with Validation

**Chosen Approach**: Parse `.tscn` and `.gd` files as text with custom validators

**Rationale**:
- Godot project files are human-readable text (similar to INI/TOML format)
- `.tscn` format: Section-based with `[node ...]`, `[resource ...]` headers
- `.gd` files: Standard text with Python-like syntax
- No Godot engine runtime required (lightweight solution)
- Can use regex and string manipulation for safe modifications
- For complex operations, can invoke Godot CLI (`godot --headless --script ...`)

**Alternatives Considered**:
1. **Full Godot Engine Embed**
   - Rejected: Massive dependency, requires C# or C++ bindings
   - Overkill for file read/write operations
   
2. **Godot CLI for All Operations**
   - Rejected: Too slow (startup time per operation)
   - Considered: Hybrid approach - use CLI for validation only

**Implementation Approach**:
- **Read operations**: Direct file I/O, parse as text
- **Create operations**: Use templates (minimal .tscn/.gd boilerplates)
- **Modify operations**: String replacement with validation
- **Validation**: Invoke `godot --headless --check-only script.gd` for syntax check
- **Atomic writes**: Write to `.tmp` file, validate, then rename

**File Format Examples**:

```gdscript
# .tscn format (simplified)
[gd_scene load_steps=2 format=3 uid="uid://..."]
[ext_resource type="Script" path="res://player.gd" id="1_abc123"]
[node name="Player" type="CharacterBody2D"]
script = ExtResource("1_abc123")
```

```gdscript
# .gd format
extends CharacterBody2D
class_name Player

@export var speed: float = 300.0

func _ready() -> void:
    pass
```

**Safety Measures**:
- Always backup original file before modification
- Validate file format before/after changes
- Fail gracefully with clear error messages
- Never modify files currently open in Godot editor (check lock files)

---

## R3: Blender Headless Automation on Windows

### Decision: Use Blender Python API (bpy) via subprocess

**Chosen Approach**: Execute Blender in background mode with Python scripts

**Rationale**:
- Blender's `--background` flag runs without GUI (headless mode)
- `bpy` (Blender Python API) provides full access to modeling, materials, export
- Script execution: `blender --background --python script.py`
- GLTF exporter is built-in addon (reliable, Godot-compatible)
- Process isolation: each operation runs in separate Blender instance

**Alternatives Considered**:
1. **Persistent Blender instance (background server)**
   - Rejected for v1: More complex (IPC, state management)
   - Future enhancement: Would reduce startup overhead
   
2. **Blender CLI only (no Python)**
   - Rejected: CLI limited, can't script complex operations
   
3. **Third-party 3D library (trimesh, Open3D)**
   - Rejected: Less powerful than Blender, harder GLTF export

**Implementation Approach**:

**Template Script Pattern**:
```python
# blender_script_template.py
import bpy
import sys
import json

# Clear default scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Operation-specific code injected here
# ...

# Export GLTF
bpy.ops.export_scene.gltf(
    filepath=sys.argv[-1],
    export_format='GLB',
    export_animations=True
)

print("SUCCESS")
```

**Execution Pattern**:
```python
import subprocess

def execute_blender_operation(script_path, output_path, timeout=30):
    cmd = [
        "blender",
        "--background",
        "--python", script_path,
        "--", output_path  # Args after -- passed to script
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        creationflags=subprocess.CREATE_NO_WINDOW  # Windows: no console popup
    )
    return result
```

**Windows-Specific Handling**:
- Use `subprocess.CREATE_NO_WINDOW` to prevent console flashing
- Handle path spaces: Pass as list, not string (avoid shell injection)
- Check Blender executable: `blender.exe` vs `blender` in PATH
- Timeout enforcement: Prevent hung processes

**GLTF Export Settings**:
```python
bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',           # Binary format (smaller)
    export_textures=True,
    export_materials='EXPORT',
    export_animations=True,
    export_apply=True              # Apply modifiers
)
```

**Error Handling**:
- Parse stderr for Blender error messages
- Check for "SUCCESS" marker in stdout
- Timeout detection: Raise clear timeout exception
- File validation: Check output file exists and has size > 0

---

## R4: GIMP Scripting for Automation

### Decision: Use GIMP Batch Mode with Python-Fu

**Chosen Approach**: Execute GIMP in batch mode (`-i -b`) with Python-Fu scripts

**Rationale**:
- GIMP 2.10 includes Python-Fu (Python 2.7-based scripting)
- Batch mode (`-i -b`) runs without GUI
- PDB (Procedural Database) provides comprehensive function catalog
- Can execute Python code directly or call PDB functions
- PNG export with transparency well-supported

**Alternatives Considered**:
1. **Script-Fu (Scheme-based)**
   - Rejected: Scheme syntax unfamiliar, Python-Fu more accessible
   
2. **GIMP 3.0 (future)**
   - Noted: GIMP 3.0 uses Python 3, may require migration
   - Current: Focus on GIMP 2.10 (stable, widely installed)

**Implementation Approach**:

**Execution Pattern**:
```python
import subprocess

def execute_gimp_operation(python_code, timeout=20):
    # GIMP batch mode: -i (no interface), -b (batch), -- (run code)
    cmd = [
        "gimp-2.10.exe",
        "-i",
        "-b", python_code,
        "-b", "(gimp-quit 0)"
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    return result
```

**Python-Fu Script Examples**:

**Create Image**:
```python
python_code = f"""
from gimpfu import *
img = gimp.Image({width}, {height}, RGB)
layer = gimp.Layer(img, "Background", {width}, {height}, RGB_IMAGE, 100, NORMAL_MODE)
img.add_layer(layer, 0)
gimp.set_foreground(({r}, {g}, {b}))
pdb.gimp_edit_fill(layer, FOREGROUND_FILL)
pdb.gimp_xcf_save(0, img, layer, "{temp_path}", "{temp_path}")
"""
```

**Export PNG**:
```python
python_code = f"""
from gimpfu import *
img = pdb.gimp_file_load("{input_path}", "{input_path}")
layer = img.active_layer
pdb.file_png_save_defaults(img, layer, "{output_path}", "{output_path}")
"""
```

**Windows-Specific Considerations**:
- GIMP executable: Typically `gimp-2.10.exe` in `C:\Program Files\GIMP 2\bin\`
- Path handling: Use raw strings or double backslashes in Python code
- File locking: GIMP creates `.xcf.lock` files during editing

**Limitations & Workarounds**:
- GIMP 2.10 Python-Fu is Python 2.7 (deprecated but still works)
- Complex filters may not be available in batch mode
- Workaround: For complex operations, generate Script-Fu instead
- Future: Migrate to GIMP 3.0 when stable (Python 3 support)

**Error Handling**:
- GIMP errors go to stderr
- Parse for "batch command experienced an execution error"
- Validate output file exists after operation
- Handle missing fonts/resources gracefully

---

## R5: Windows Tool Detection Strategies

### Decision: Multi-Method Detection with Priority Order

**Chosen Approach**: Try multiple detection methods in priority order

**Detection Priority**:
1. **User-specified path** (from config file)
2. **Windows Registry** (official installation location)
3. **Common installation paths** (Program Files, etc.)
4. **PATH environment variable**
5. **Manual fallback** (prompt user)

**Rationale**:
- Different installation methods create different footprints
- Registry most reliable for official installers
- PATH useful for portable/Steam versions
- Common paths catch manual installs
- User override allows custom locations

**Implementation Approach**:

**Godot Detection**:
```python
import winreg
import os
from pathlib import Path

def detect_godot():
    # Method 1: Check registry (if installed via MSI)
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Godot")
        path = winreg.QueryValueEx(key, "InstallPath")[0]
        godot_exe = Path(path) / "godot.exe"
        if godot_exe.exists():
            return str(godot_exe)
    except WindowsError:
        pass
    
    # Method 2: Common install locations
    common_paths = [
        Path(os.environ["ProgramFiles"]) / "Godot" / "godot.exe",
        Path(os.environ["ProgramFiles(x86)"]) / "Godot" / "godot.exe",
        Path.home() / "AppData" / "Local" / "Godot" / "godot.exe",
    ]
    for path in common_paths:
        if path.exists():
            return str(path)
    
    # Method 3: Check PATH
    path_godot = shutil.which("godot")
    if path_godot:
        return path_godot
    
    return None  # Not found
```

**Blender Detection**:
```python
def detect_blender():
    # Method 1: Registry (Blender Foundation installer)
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                             r"SOFTWARE\BlenderFoundation")
        # Enumerate subkeys for versions (e.g., "Blender 3.6")
        # Get InstallDir value
        # Return path/blender.exe
    except WindowsError:
        pass
    
    # Method 2: Common paths
    common_paths = [
        Path(os.environ["ProgramFiles"]) / "Blender Foundation" / "Blender 3.6" / "blender.exe",
        # Add more versions
    ]
    
    # Method 3: PATH
    return shutil.which("blender")
```

**GIMP Detection**:
```python
def detect_gimp():
    # GIMP typically: C:\Program Files\GIMP 2\bin\gimp-2.10.exe
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GIMP-2_is1")
        install_location = winreg.QueryValueEx(key, "InstallLocation")[0]
        gimp_exe = Path(install_location) / "bin" / "gimp-2.10.exe"
        if gimp_exe.exists():
            return str(gimp_exe)
    except WindowsError:
        pass
    
    # Common paths and PATH checks...
```

**Version Detection**:
```python
def get_tool_version(executable_path, version_flag="--version"):
    result = subprocess.run(
        [executable_path, version_flag],
        capture_output=True,
        text=True,
        timeout=5
    )
    # Parse version from output
    # Example: "Godot Engine v4.2.1.stable.official"
    return parse_version_string(result.stdout)
```

**Validation**:
```python
def validate_tool_installation(executable_path):
    """Verify executable exists and runs."""
    if not Path(executable_path).exists():
        return False, "Executable not found"
    
    try:
        result = subprocess.run(
            [executable_path, "--version"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Valid"
        else:
            return False, "Executable failed to run"
    except Exception as e:
        return False, f"Error: {str(e)}"
```

**Configuration Storage**:
```json
{
  "tools": {
    "godot": {
      "path": "auto",  // or explicit path
      "detected_path": "C:\\Program Files\\Godot\\godot.exe",
      "version": "4.2.1",
      "detection_method": "registry",
      "last_validated": "2025-10-26T10:30:00Z"
    }
  }
}
```

---

## R6: Concurrent File Access Patterns

### Decision: File Locking + Atomic Writes

**Chosen Approach**: Combine file locking with atomic write pattern

**Rationale**:
- Prevents race conditions when multiple MCP operations run simultaneously
- Atomic writes ensure no partial/corrupted files
- File locking coordinates access between operations
- Compatible with external tool file watchers (Godot, etc.)

**Implementation Approach**:

**File Locking (Windows)**:
```python
import msvcrt
import os

class FileLock:
    def __init__(self, file_path, timeout=5):
        self.file_path = file_path
        self.timeout = timeout
        self.lock_file = f"{file_path}.lock"
        self.lock_handle = None
    
    def __enter__(self):
        start_time = time.time()
        while True:
            try:
                self.lock_handle = os.open(
                    self.lock_file,
                    os.O_CREAT | os.O_EXCL | os.O_RDWR
                )
                return self
            except FileExistsError:
                if time.time() - start_time > self.timeout:
                    raise TimeoutError(f"Could not acquire lock on {self.file_path}")
                time.sleep(0.1)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lock_handle:
            os.close(self.lock_handle)
            os.remove(self.lock_file)
```

**Atomic Write Pattern**:
```python
import tempfile
import shutil

def atomic_write(file_path, content):
    """Write file atomically to prevent corruption."""
    dir_path = os.path.dirname(file_path)
    
    # Write to temporary file in same directory (same filesystem)
    with tempfile.NamedTemporaryFile(
        mode='w',
        dir=dir_path,
        delete=False,
        suffix='.tmp'
    ) as tmp_file:
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    # Atomic rename (replaces existing file)
    shutil.move(tmp_path, file_path)
```

**Combined Safe Write**:
```python
def safe_write_file(file_path, content, backup=True):
    """Write file with locking and atomic write."""
    with FileLock(file_path):
        # Backup original if requested
        if backup and os.path.exists(file_path):
            backup_path = f"{file_path}.backup"
            shutil.copy2(file_path, backup_path)
        
        # Atomic write
        atomic_write(file_path, content)
```

**Operation Queue (Optional Enhancement)**:
```python
import queue
import threading

class OperationQueue:
    """Serialize operations on same file."""
    def __init__(self):
        self.queues = {}  # file_path -> queue
        self.locks = {}   # file_path -> lock
    
    def execute(self, file_path, operation):
        """Queue operation for file."""
        if file_path not in self.queues:
            self.queues[file_path] = queue.Queue()
            self.locks[file_path] = threading.Lock()
        
        result_future = threading.Event()
        self.queues[file_path].put((operation, result_future))
        
        # Process queue if not already running
        # ... worker thread logic ...
```

**Error Handling**:
```python
def handle_lock_timeout(file_path):
    """Handle case where lock cannot be acquired."""
    # Check if lock file is stale (older than X minutes)
    lock_file = f"{file_path}.lock"
    if os.path.exists(lock_file):
        age = time.time() - os.path.getmtime(lock_file)
        if age > 300:  # 5 minutes
            # Stale lock, remove it
            os.remove(lock_file)
            logging.warning(f"Removed stale lock file: {lock_file}")
        else:
            raise Exception(f"File is locked by another process: {file_path}")
```

**Tool-Specific Considerations**:

**Godot**:
- Godot watches files and auto-reloads on change
- Use atomic writes to ensure Godot never sees partial file
- Lock files before modifying to prevent conflicts with Godot's own saves

**Blender/GIMP**:
- These tools may lock files when open in GUI
- Detect lock files (`.blend.lock`, `.xcf.lock`)
- Refuse to modify if tool has file open: clear error message

**Testing Strategy**:
```python
def test_concurrent_writes():
    """Test multiple operations on same file don't corrupt."""
    import concurrent.futures
    
    file_path = "test_file.gd"
    
    def write_operation(content):
        safe_write_file(file_path, content)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(write_operation, f"Content {i}")
            for i in range(10)
        ]
        concurrent.futures.wait(futures)
    
    # Verify file is valid (not corrupted)
    assert os.path.exists(file_path)
    with open(file_path) as f:
        content = f.read()
        assert content.startswith("Content")
```

---

## Summary of Technology Decisions

| Component | Technology | Rationale |
|-----------|------------|-----------|
| MCP Framework | Official `mcp` Python SDK | Standard, well-supported, stdio transport |
| Godot Integration | Direct text file parsing + CLI validation | Lightweight, no engine dependency |
| Blender Automation | `bpy` via `--background` subprocess | Full API access, headless capable |
| GIMP Automation | Python-Fu batch mode (`-i -b`) | Built-in scripting, PNG export support |
| Tool Detection | Multi-method (registry → common paths → PATH) | Reliable across installation types |
| File Safety | File locking + atomic writes | Prevents corruption, coordinates access |

---

## Implementation Readiness

✅ All research tasks complete  
✅ All technology decisions documented  
✅ All NEEDS CLARIFICATION items resolved  
✅ Ready for Phase 1: Design & Contracts

**Next Step**: Proceed with creating `data-model.md`, operation contracts, and `quickstart.md`

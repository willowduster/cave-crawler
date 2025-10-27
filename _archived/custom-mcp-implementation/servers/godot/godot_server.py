"""Godot Engine MCP Server implementation."""

from typing import Dict, Any, List, Optional
from pathlib import Path
import subprocess
from servers.common.base_server import BaseMCPServer
from servers.common.config import ServerConfig
from servers.godot.detector import GodotDetector
from servers.godot.scene_parser import GodotScene


class GodotMCPServer(BaseMCPServer):
    """MCP Server for Godot Engine operations."""
    
    def __init__(
        self,
        config: ServerConfig,
        log_file: str,
        log_level: str = "INFO",
    ):
        """Initialize Godot MCP server.
        
        Args:
            config: Server configuration
            log_file: Path to log file
            log_level: Logging level
        """
        super().__init__("godot", config, log_file, log_level)
        self.godot_exe: Optional[str] = None
        self.working_dir: Optional[Path] = None
    
    def initialize(self) -> None:
        """Initialize Godot server."""
        self.logger.info("Initializing Godot MCP server...")
        
        # Detect or validate Godot installation
        if self.config.executable_path:
            self.godot_exe = self.config.executable_path
            self.logger.info(f"Using configured Godot: {self.godot_exe}")
        elif self.config.auto_detect:
            detector = GodotDetector(self.logger)
            installation = detector.detect(self.config.detection_methods)
            
            if not installation:
                raise RuntimeError("Godot Engine not found. Please install Godot or configure executable_path.")
            
            self.godot_exe = installation.executable_path
            self.logger.info(f"Detected Godot {installation.version}: {self.godot_exe}")
        else:
            raise RuntimeError("Godot executable_path not configured and auto_detect is disabled.")
        
        # Validate executable exists
        if not Path(self.godot_exe).exists():
            raise RuntimeError(f"Godot executable not found: {self.godot_exe}")
        
        # Set working directory
        if self.config.working_directory:
            self.working_dir = Path(self.config.working_directory)
            if not self.working_dir.exists():
                raise RuntimeError(f"Working directory does not exist: {self.working_dir}")
        
        self._set_initialized(True)
    
    def shutdown(self) -> None:
        """Shutdown Godot server."""
        self.logger.info("Shutting down Godot MCP server...")
        self._set_initialized(False)
    
    def execute_operation(
        self,
        operation: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute a Godot operation.
        
        Args:
            operation: Operation name
            parameters: Operation parameters
        
        Returns:
            Operation result
        """
        if not self.is_initialized():
            return self.create_error_response("Server not initialized")
        
        # Route to operation handlers
        handlers = {
            "list_project_files": self._list_project_files,
            "read_scene": self._read_scene,
            "create_scene": self._create_scene,
            "read_script": self._read_script,
            "create_script": self._create_script,
            "validate_script": self._validate_script,
            "list_scenes": self._list_scenes,
            "list_scripts": self._list_scripts,
        }
        
        handler = handlers.get(operation)
        if not handler:
            return self.create_error_response(
                f"Unknown operation: {operation}",
                details=f"Available operations: {list(handlers.keys())}"
            )
        
        try:
            return handler(parameters)
        except Exception as e:
            self.logger.error(f"Operation {operation} failed: {e}", exc_info=True)
            return self.create_error_response(str(e), details=type(e).__name__)
    
    def _list_project_files(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List files in Godot project.
        
        Args:
            params: Optional 'pattern' for file filtering
        
        Returns:
            List of file paths
        """
        if not self.working_dir:
            return self.create_error_response("Working directory not configured")
        
        pattern = params.get("pattern", "**/*")
        files = [
            str(f.relative_to(self.working_dir))
            for f in self.working_dir.glob(pattern)
            if f.is_file() and not f.name.startswith('.')
        ]
        
        return self.create_success_response(
            {"files": sorted(files), "count": len(files)},
            message=f"Found {len(files)} files"
        )
    
    def _read_scene(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a Godot scene file.
        
        Args:
            params: 'path' - relative path to .tscn file
        
        Returns:
            Scene structure
        """
        self.validate_parameters(params, required=["path"])
        
        scene_path = self._resolve_path(params["path"])
        if not scene_path.exists():
            return self.create_error_response(f"Scene not found: {params['path']}")
        
        if not scene_path.suffix == ".tscn":
            return self.create_error_response(f"Not a scene file: {params['path']}")
        
        scene = GodotScene(str(scene_path))
        return self.create_success_response(
            scene.to_dict(),
            message=f"Loaded scene with {len(scene.nodes)} nodes"
        )
    
    def _create_scene(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Godot scene file.
        
        Args:
            params: 'path' - relative path, 'root_type' - root node type
        
        Returns:
            Success message
        """
        self.validate_parameters(params, required=["path"], optional=["root_type"])
        
        scene_path = self._resolve_path(params["path"])
        root_type = params.get("root_type", "Node2D")
        
        # Create scene content
        scene_content = f"""[gd_scene load_steps=1 format=3]

[node name="{scene_path.stem}" type="{root_type}"]
"""
        
        # Create parent directories
        scene_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write scene file
        scene_path.write_text(scene_content, encoding="utf-8")
        
        return self.create_success_response(
            {"path": str(scene_path.relative_to(self.working_dir))},
            message=f"Created scene with root type {root_type}"
        )
    
    def _read_script(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a GDScript file.
        
        Args:
            params: 'path' - relative path to .gd file
        
        Returns:
            Script content
        """
        self.validate_parameters(params, required=["path"])
        
        script_path = self._resolve_path(params["path"])
        if not script_path.exists():
            return self.create_error_response(f"Script not found: {params['path']}")
        
        content = script_path.read_text(encoding="utf-8")
        
        return self.create_success_response(
            {"path": params["path"], "content": content, "lines": len(content.splitlines())},
            message=f"Read script ({len(content.splitlines())} lines)"
        )
    
    def _create_script(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new GDScript file.
        
        Args:
            params: 'path' - relative path, 'content' - script content (optional)
        
        Returns:
            Success message
        """
        self.validate_parameters(params, required=["path"], optional=["content"])
        
        script_path = self._resolve_path(params["path"])
        content = params.get("content", 'extends Node\n\n# Called when the node enters the scene tree.\nfunc _ready():\n\tpass\n')
        
        # Create parent directories
        script_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write script file
        script_path.write_text(content, encoding="utf-8")
        
        return self.create_success_response(
            {"path": str(script_path.relative_to(self.working_dir))},
            message="Created script file"
        )
    
    def _validate_script(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a GDScript file using Godot.
        
        Args:
            params: 'path' - relative path to .gd file
        
        Returns:
            Validation result
        """
        self.validate_parameters(params, required=["path"])
        
        script_path = self._resolve_path(params["path"])
        if not script_path.exists():
            return self.create_error_response(f"Script not found: {params['path']}")
        
        # Run Godot script checker
        try:
            result = subprocess.run(
                [self.godot_exe, "--check-only", "--script", str(script_path)],
                capture_output=True,
                text=True,
                timeout=10.0,
                cwd=str(self.working_dir) if self.working_dir else None,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            valid = result.returncode == 0
            
            return self.create_success_response(
                {"valid": valid, "errors": result.stderr if not valid else None},
                message="Script is valid" if valid else "Script has errors"
            )
        except subprocess.TimeoutExpired:
            return self.create_error_response("Validation timeout")
        except Exception as e:
            return self.create_error_response(f"Validation failed: {e}")
    
    def _list_scenes(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all scene files in project.
        
        Returns:
            List of scene paths
        """
        if not self.working_dir:
            return self.create_error_response("Working directory not configured")
        
        scenes = [
            str(f.relative_to(self.working_dir))
            for f in self.working_dir.glob("**/*.tscn")
            if not any(part.startswith('.') for part in f.parts)
        ]
        
        return self.create_success_response(
            {"scenes": sorted(scenes), "count": len(scenes)},
            message=f"Found {len(scenes)} scenes"
        )
    
    def _list_scripts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all GDScript files in project.
        
        Returns:
            List of script paths
        """
        if not self.working_dir:
            return self.create_error_response("Working directory not configured")
        
        scripts = [
            str(f.relative_to(self.working_dir))
            for f in self.working_dir.glob("**/*.gd")
            if not any(part.startswith('.') for part in f.parts)
        ]
        
        return self.create_success_response(
            {"scripts": sorted(scripts), "count": len(scripts)},
            message=f"Found {len(scripts)} scripts"
        )
    
    def _resolve_path(self, relative_path: str) -> Path:
        """Resolve a relative path to absolute path in working directory.
        
        Args:
            relative_path: Relative path (supports res:// prefix)
        
        Returns:
            Absolute path
        """
        if not self.working_dir:
            raise RuntimeError("Working directory not configured")
        
        # Strip res:// prefix if present
        if relative_path.startswith("res://"):
            relative_path = relative_path[6:]
        
        return self.working_dir / relative_path

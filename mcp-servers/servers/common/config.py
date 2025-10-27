"""Configuration management for MCP servers.

Provides Pydantic models and configuration loading/saving.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ServerConfig(BaseModel):
    """Configuration for a single MCP server."""
    
    enabled: bool
    executable_path: Optional[str] = None
    working_directory: Optional[str] = None
    auto_detect: bool = True
    detection_methods: List[str] = Field(
        default_factory=lambda: ["registry", "path", "common_paths"]
    )
    operation_timeout: Optional[int] = None
    environment: Dict[str, str] = Field(default_factory=dict)
    additional_args: List[str] = Field(default_factory=list)
    
    @field_validator("detection_methods")
    @classmethod
    def validate_detection_methods(cls, v: List[str]) -> List[str]:
        """Validate detection methods."""
        valid_methods = {"registry", "path", "common_paths", "steam"}
        for method in v:
            if method not in valid_methods:
                raise ValueError(
                    f"Invalid detection method: {method}. "
                    f"Must be one of {valid_methods}"
                )
        return v


class GlobalConfig(BaseModel):
    """Global MCP server settings."""
    
    log_level: str = "INFO"
    log_directory: str = "logs"
    state_file: str = "state/mcp-state.json"
    max_concurrent_operations: int = 5
    operation_timeout_seconds: int = 30
    servers: Dict[str, ServerConfig] = Field(default_factory=dict)
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v not in valid_levels:
            raise ValueError(
                f"Invalid log level: {v}. Must be one of {valid_levels}"
            )
        return v
    
    @field_validator("max_concurrent_operations")
    @classmethod
    def validate_max_concurrent(cls, v: int) -> int:
        """Validate max concurrent operations."""
        if v < 1 or v > 20:
            raise ValueError("max_concurrent_operations must be between 1 and 20")
        return v


class ServersConfig(BaseModel):
    """Container for all server configurations."""
    
    godot: ServerConfig
    blender: ServerConfig
    gimp: ServerConfig


class MCPConfig(BaseModel):
    """Root MCP configuration model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    version: str
    servers: ServersConfig
    global_settings: GlobalConfig = Field(default_factory=GlobalConfig, alias="global")
    
    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate version format."""
        if v != "1.0":
            raise ValueError(f"Unsupported config version: {v}. Expected 1.0")
        return v


class ConfigManager:
    """Manager for loading and saving MCP configuration."""
    
    def __init__(self, config_path: str):
        """Initialize config manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
    
    def load(self) -> MCPConfig:
        """Load configuration from file.
        
        Returns:
            Parsed and validated configuration
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config is invalid JSON
            pydantic.ValidationError: If config doesn't match schema
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        content = self.config_path.read_text(encoding="utf-8")
        data = json.loads(content)
        
        return MCPConfig(**data)
    
    def save(self, config: MCPConfig) -> None:
        """Save configuration to file.
        
        Args:
            config: Configuration to save
        """
        # Create parent directory if needed
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dict and save
        data = config.model_dump(by_alias=True, exclude_none=True)
        content = json.dumps(data, indent=2)
        
        self.config_path.write_text(content, encoding="utf-8")
    
    def get_example_config(self) -> MCPConfig:
        """Get an example configuration.
        
        Returns:
            Example configuration with sensible defaults
        """
        return MCPConfig(
            version="1.0",
            servers=ServersConfig(
                godot=ServerConfig(enabled=True),
                blender=ServerConfig(enabled=True),
                gimp=ServerConfig(enabled=True),
            )
        )


def load_config(config_path: str) -> GlobalConfig:
    """
    Load global configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Loaded configuration
    """
    path = Path(config_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    content = path.read_text(encoding="utf-8")
    data = json.loads(content)
    
    return GlobalConfig(**data)

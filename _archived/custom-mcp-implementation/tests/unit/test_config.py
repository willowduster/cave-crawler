"""Unit tests for configuration manager."""

import pytest
import json
from pathlib import Path
from pydantic import ValidationError
from servers.common.config import ConfigManager, MCPConfig, ServerConfig


def test_config_manager_loads_valid_config(tmp_path: Path) -> None:
    """Test that ConfigManager loads valid configuration file."""
    config_file = tmp_path / "config.json"
    config_data = {
        "version": "1.0",
        "servers": {
            "godot": {"enabled": True},
            "blender": {"enabled": False},
            "gimp": {"enabled": True}
        },
        "global": {
            "logLevel": "INFO",
            "logDirectory": "logs",
            "maxConcurrentOperations": 5,
            "operationTimeoutSeconds": 30
        }
    }
    config_file.write_text(json.dumps(config_data))
    
    manager = ConfigManager(str(config_file))
    config = manager.load()
    
    assert config.version == "1.0"
    assert config.servers.godot.enabled is True
    assert config.servers.blender.enabled is False
    assert config.global_settings.log_level == "INFO"


def test_config_manager_raises_on_invalid_json(tmp_path: Path) -> None:
    """Test that ConfigManager raises error for invalid JSON."""
    config_file = tmp_path / "config.json"
    config_file.write_text("{ invalid json }")
    
    manager = ConfigManager(str(config_file))
    with pytest.raises(json.JSONDecodeError):
        manager.load()


def test_config_manager_validates_schema(tmp_path: Path) -> None:
    """Test that ConfigManager validates configuration against schema."""
    config_file = tmp_path / "config.json"
    invalid_config = {
        "version": "1.0",
        "servers": {
            "godot": {"enabled": "not_a_boolean"}  # Invalid type
        }
    }
    config_file.write_text(json.dumps(invalid_config))
    
    manager = ConfigManager(str(config_file))
    with pytest.raises(ValidationError):
        manager.load()


def test_config_manager_saves_config(tmp_path: Path) -> None:
    """Test that ConfigManager saves configuration to file."""
    config_file = tmp_path / "config.json"
    
    config = MCPConfig(
        version="1.0",
        servers={
            "godot": ServerConfig(enabled=True),
            "blender": ServerConfig(enabled=False),
            "gimp": ServerConfig(enabled=True)
        }
    )
    
    manager = ConfigManager(str(config_file))
    manager.save(config)
    
    assert config_file.exists()
    loaded_data = json.loads(config_file.read_text())
    assert loaded_data["version"] == "1.0"
    assert loaded_data["servers"]["godot"]["enabled"] is True


def test_server_config_default_values() -> None:
    """Test that ServerConfig uses correct default values."""
    config = ServerConfig(enabled=True)
    
    assert config.enabled is True
    assert config.auto_detect is True
    assert config.detection_methods == ["registry", "path", "common_paths"]
    assert config.executable_path is None
    assert config.operation_timeout is None


def test_mcp_config_validates_version() -> None:
    """Test that MCPConfig validates version format."""
    with pytest.raises(ValidationError):
        MCPConfig(
            version="2.0",  # Invalid version
            servers={
                "godot": ServerConfig(enabled=True),
                "blender": ServerConfig(enabled=False),
                "gimp": ServerConfig(enabled=True)
            }
        )

"""Integration test suite for MCP servers."""

import pytest
import json
import tempfile
from pathlib import Path
from servers.common.config import ServerConfig, GlobalConfig


def create_test_config(tmp_path: Path) -> Path:
    """Create a complete test configuration."""
    config_file = tmp_path / "integration-config.json"
    
    # Create project directories
    godot_project = tmp_path / "godot_project"
    godot_project.mkdir()
    (godot_project / "project.godot").write_text("")
    (godot_project / "scenes").mkdir()
    (godot_project / "scripts").mkdir()
    
    # Create sample files
    (godot_project / "scenes" / "main.tscn").write_text(
        "[gd_scene format=3]\n\n[node name='Main' type='Node2D']\n"
    )
    (godot_project / "scripts" / "player.gd").write_text(
        "extends CharacterBody2D\n\nfunc _ready():\n\tpass\n"
    )
    
    # Create config
    config = GlobalConfig(
        log_level="INFO",
        log_directory=str(tmp_path / "logs"),
        state_file=str(tmp_path / "state" / "mcp-state.json"),
        servers={
            "godot": ServerConfig(
                enabled=True,
                executable_path="C:\\fake\\godot.exe",  # Fake path for testing
                auto_detect=False,
                working_directory=str(godot_project),
            ),
        },
    )
    
    config_file.write_text(json.dumps(config.model_dump(), indent=2))
    return config_file


@pytest.mark.asyncio
async def test_end_to_end_godot_workflow(tmp_path: Path):
    """Test complete workflow with Godot server."""
    from servers.common.orchestrator import ServerOrchestrator
    from servers.common.state_manager import StateManager
    
    # Setup
    config_file = create_test_config(tmp_path)
    state_file = tmp_path / "state" / "mcp-state.json"
    
    # Create orchestrator
    orchestrator = ServerOrchestrator(config_file)
    await orchestrator.initialize()
    
    assert "godot" in orchestrator.servers
    assert orchestrator.is_healthy()
    
    # Create state manager
    state_manager = StateManager(state_file)
    state_manager.update_server_state("godot", status="running", pid=12345)
    
    # Execute operations
    result = orchestrator.execute_operation("godot", "list_scenes", {})
    assert result["status"] == "success"
    
    state_manager.log_operation(
        "godot",
        "list_scenes",
        {},
        result,
        duration_ms=10.5,
    )
    
    # Check state
    state = state_manager.get_server_state("godot")
    assert state.operations_count == 1
    
    # Cleanup
    await orchestrator.shutdown()


def test_configuration_loading(tmp_path: Path):
    """Test configuration loading and validation."""
    from servers.common.config import load_config
    
    config_file = create_test_config(tmp_path)
    config = load_config(str(config_file))
    
    assert config.log_level == "INFO"
    assert "godot" in config.servers
    assert config.servers["godot"].enabled


def test_state_persistence(tmp_path: Path):
    """Test state persistence across manager instances."""
    from servers.common.state_manager import StateManager
    
    state_file = tmp_path / "state.json"
    
    # Create first manager
    manager1 = StateManager(state_file)
    manager1.update_server_state("godot", status="running", pid=1234)
    manager1.log_operation("godot", "test_op", {}, {"status": "success"}, 10.0)
    
    # Create second manager (should load state)
    manager2 = StateManager(state_file)
    state = manager2.get_server_state("godot")
    
    assert state is not None
    assert state.pid == 1234
    assert state.operations_count == 1


def test_godot_scene_operations(tmp_path: Path):
    """Test Godot scene reading and creation."""
    from servers.godot.godot_server import GodotMCPServer
    from servers.common.config import ServerConfig
    
    # Setup
    godot_project = tmp_path / "godot_project"
    godot_project.mkdir()
    (godot_project / "project.godot").write_text("")
    (godot_project / "scenes").mkdir()
    
    # Create sample scene
    (godot_project / "scenes" / "test.tscn").write_text(
        "[gd_scene format=3]\n\n[node name='Test' type='Node2D']\n"
    )
    
    config = ServerConfig(
        enabled=True,
        executable_path="C:\\fake\\godot.exe",
        auto_detect=False,
        working_directory=str(godot_project),
    )
    
    server = GodotMCPServer(config, str(tmp_path / "test.log"))
    server.godot_exe = config.executable_path
    server.working_dir = Path(config.working_directory)
    server._set_initialized(True)
    
    # List scenes
    result = server.execute_operation("list_scenes", {})
    assert result["status"] == "success"
    assert any("test.tscn" in s for s in result["data"]["scenes"])
    
    # Read scene
    result = server.execute_operation("read_scene", {"path": "scenes/test.tscn"})
    assert result["status"] == "success"
    assert result["data"]["node_count"] > 0


def test_error_handling(tmp_path: Path):
    """Test error handling in operations."""
    from servers.godot.godot_server import GodotMCPServer
    from servers.common.config import ServerConfig
    
    config = ServerConfig(
        enabled=True,
        executable_path="C:\\fake\\godot.exe",
        auto_detect=False,
        working_directory=str(tmp_path),
    )
    
    server = GodotMCPServer(config, str(tmp_path / "test.log"))
    server.godot_exe = config.executable_path
    server.working_dir = Path(config.working_directory)
    server._set_initialized(True)
    
    # Invalid operation
    result = server.execute_operation("invalid_op", {})
    assert result["status"] == "error"
    assert "Unknown operation" in result["error"]
    
    # Missing file
    result = server.execute_operation("read_scene", {"path": "nonexistent.tscn"})
    assert result["status"] == "error"

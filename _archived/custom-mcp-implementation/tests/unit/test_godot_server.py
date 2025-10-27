"""Unit tests for Godot MCP Server."""

import pytest
from pathlib import Path
from servers.godot.godot_server import GodotMCPServer
from servers.common.config import ServerConfig


@pytest.fixture
def mock_godot_project(tmp_path: Path) -> Path:
    """Create a mock Godot project structure."""
    project_dir = tmp_path / "godot_project"
    project_dir.mkdir()
    
    # Create some test files
    (project_dir / "project.godot").write_text("")
    (project_dir / "scenes").mkdir()
    (project_dir / "scripts").mkdir()
    
    # Create a sample scene
    scene_content = """[gd_scene load_steps=1 format=3]

[node name="TestScene" type="Node2D"]
"""
    (project_dir / "scenes" / "test.tscn").write_text(scene_content)
    
    # Create a sample script
    script_content = """extends Node

func _ready():
    print("Hello")
"""
    (project_dir / "scripts" / "test.gd").write_text(script_content)
    
    return project_dir


def test_godot_server_init():
    """Test Godot server initialization."""
    config = ServerConfig(
        enabled=True,
        executable_path="C:\\fake\\godot.exe",  # Will skip detection
        auto_detect=False,
    )
    
    server = GodotMCPServer(config, "test.log")
    assert server.name == "godot"
    assert not server.is_initialized()


def test_list_project_files(mock_godot_project: Path):
    """Test listing project files."""
    config = ServerConfig(
        enabled=True,
        executable_path="C:\\fake\\godot.exe",
        auto_detect=False,
        working_directory=str(mock_godot_project),
    )
    
    server = GodotMCPServer(config, "test.log")
    server.godot_exe = config.executable_path  # Skip validation
    server.working_dir = Path(config.working_directory)
    server._set_initialized(True)
    
    result = server.execute_operation("list_project_files", {})
    
    assert result["status"] == "success"
    assert "files" in result["data"]
    assert len(result["data"]["files"]) > 0


def test_create_scene(mock_godot_project: Path):
    """Test creating a new scene."""
    config = ServerConfig(
        enabled=True,
        executable_path="C:\\fake\\godot.exe",
        auto_detect=False,
        working_directory=str(mock_godot_project),
    )
    
    server = GodotMCPServer(config, "test.log")
    server.godot_exe = config.executable_path
    server.working_dir = Path(config.working_directory)
    server._set_initialized(True)
    
    result = server.execute_operation("create_scene", {
        "path": "scenes/new_scene.tscn",
        "root_type": "Node3D",
    })
    
    assert result["status"] == "success"
    assert (mock_godot_project / "scenes" / "new_scene.tscn").exists()


def test_read_scene(mock_godot_project: Path):
    """Test reading a scene file."""
    config = ServerConfig(
        enabled=True,
        executable_path="C:\\fake\\godot.exe",
        auto_detect=False,
        working_directory=str(mock_godot_project),
    )
    
    server = GodotMCPServer(config, "test.log")
    server.godot_exe = config.executable_path
    server.working_dir = Path(config.working_directory)
    server._set_initialized(True)
    
    result = server.execute_operation("read_scene", {
        "path": "scenes/test.tscn",
    })
    
    assert result["status"] == "success"
    assert "nodes" in result["data"]
    assert result["data"]["node_count"] > 0


def test_create_script(mock_godot_project: Path):
    """Test creating a new script."""
    config = ServerConfig(
        enabled=True,
        executable_path="C:\\fake\\godot.exe",
        auto_detect=False,
        working_directory=str(mock_godot_project),
    )
    
    server = GodotMCPServer(config, "test.log")
    server.godot_exe = config.executable_path
    server.working_dir = Path(config.working_directory)
    server._set_initialized(True)
    
    result = server.execute_operation("create_script", {
        "path": "scripts/enemy.gd",
        "content": "extends Node\n\nfunc attack():\n\tpass\n",
    })
    
    assert result["status"] == "success"
    script_path = mock_godot_project / "scripts" / "enemy.gd"
    assert script_path.exists()
    assert "attack" in script_path.read_text()


def test_list_scenes(mock_godot_project: Path):
    """Test listing all scenes."""
    config = ServerConfig(
        enabled=True,
        executable_path="C:\\fake\\godot.exe",
        auto_detect=False,
        working_directory=str(mock_godot_project),
    )
    
    server = GodotMCPServer(config, "test.log")
    server.godot_exe = config.executable_path
    server.working_dir = Path(config.working_directory)
    server._set_initialized(True)
    
    result = server.execute_operation("list_scenes", {})
    
    assert result["status"] == "success"
    assert "scenes" in result["data"]
    assert any("test.tscn" in s for s in result["data"]["scenes"])


def test_unknown_operation(mock_godot_project: Path):
    """Test handling unknown operation."""
    config = ServerConfig(
        enabled=True,
        executable_path="C:\\fake\\godot.exe",
        auto_detect=False,
        working_directory=str(mock_godot_project),
    )
    
    server = GodotMCPServer(config, "test.log")
    server.godot_exe = config.executable_path
    server.working_dir = Path(config.working_directory)
    server._set_initialized(True)
    
    result = server.execute_operation("invalid_operation", {})
    
    assert result["status"] == "error"
    assert "Unknown operation" in result["error"]

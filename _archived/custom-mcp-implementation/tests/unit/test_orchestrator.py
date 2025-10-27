"""Unit tests for server orchestrator."""

import pytest
from pathlib import Path
from servers.common.orchestrator import ServerOrchestrator
from servers.common.config import ServerConfig, GlobalConfig


@pytest.fixture
def test_config(tmp_path: Path) -> Path:
    """Create a test configuration file."""
    config_file = tmp_path / "test-config.json"
    
    config = GlobalConfig(
        log_level="INFO",
        log_directory="logs",
        state_file="state/mcp-state.json",
        servers={
            "godot": ServerConfig(
                enabled=True,
                executable_path="C:\\fake\\godot.exe",
                auto_detect=False,
                working_directory=str(tmp_path / "godot_project"),
            ),
        },
    )
    
    # Create working directory
    (tmp_path / "godot_project").mkdir()
    (tmp_path / "godot_project" / "project.godot").write_text("")
    
    # Save config
    import json
    config_file.write_text(json.dumps(config.model_dump(), indent=2))
    
    return config_file


@pytest.mark.asyncio
async def test_orchestrator_init(test_config: Path):
    """Test orchestrator initialization."""
    orchestrator = ServerOrchestrator(test_config)
    
    success = await orchestrator.initialize()
    assert success
    assert "godot" in orchestrator.servers
    
    await orchestrator.shutdown()


@pytest.mark.asyncio
async def test_orchestrator_server_states(test_config: Path):
    """Test getting server states."""
    orchestrator = ServerOrchestrator(test_config)
    await orchestrator.initialize()
    
    # Get single state
    state = orchestrator.get_server_state("godot")
    assert state is not None
    assert state.name == "godot"
    assert state.status == "running"
    
    # Get all states
    all_states = orchestrator.get_all_states()
    assert "godot" in all_states
    
    await orchestrator.shutdown()


@pytest.mark.asyncio
async def test_orchestrator_running_servers(test_config: Path):
    """Test getting running servers list."""
    orchestrator = ServerOrchestrator(test_config)
    await orchestrator.initialize()
    
    running = orchestrator.get_running_servers()
    assert "godot" in running
    
    await orchestrator.shutdown()


@pytest.mark.asyncio
async def test_orchestrator_health_check(test_config: Path):
    """Test health check."""
    orchestrator = ServerOrchestrator(test_config)
    await orchestrator.initialize()
    
    assert orchestrator.is_healthy()
    
    await orchestrator.shutdown()


@pytest.mark.asyncio
async def test_orchestrator_execute_operation(test_config: Path):
    """Test executing an operation."""
    orchestrator = ServerOrchestrator(test_config)
    await orchestrator.initialize()
    
    # Execute a valid operation
    result = orchestrator.execute_operation(
        "godot",
        "list_scenes",
        {}
    )
    
    assert result["status"] in ["success", "error"]
    
    # Execute on non-existent server
    result = orchestrator.execute_operation(
        "nonexistent",
        "some_op",
        {}
    )
    
    assert result["status"] == "error"
    assert "not found" in result["error"]
    
    await orchestrator.shutdown()


@pytest.mark.asyncio
async def test_orchestrator_shutdown(test_config: Path):
    """Test graceful shutdown."""
    orchestrator = ServerOrchestrator(test_config)
    await orchestrator.initialize()
    
    assert len(orchestrator.servers) > 0
    
    await orchestrator.shutdown()
    
    assert len(orchestrator.servers) == 0
    assert len(orchestrator.server_states) == 0

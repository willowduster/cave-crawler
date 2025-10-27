"""Unit tests for state manager."""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
from servers.common.state_manager import StateManager


@pytest.fixture
def state_file(tmp_path: Path) -> Path:
    """Create a temporary state file path."""
    return tmp_path / "test-state.json"


def test_state_manager_init(state_file: Path):
    """Test state manager initialization."""
    manager = StateManager(state_file)
    
    assert manager.state_file == state_file
    assert len(manager.states) == 0
    assert len(manager.operation_log) == 0


def test_update_server_state(state_file: Path):
    """Test updating server state."""
    manager = StateManager(state_file)
    
    # Add new server
    manager.update_server_state(
        "godot",
        status="running",
        pid=1234,
    )
    
    state = manager.get_server_state("godot")
    assert state is not None
    assert state.name == "godot"
    assert state.status == "running"
    assert state.pid == 1234
    assert state.started_at is not None
    
    # Update existing server
    manager.update_server_state(
        "godot",
        error="Test error",
    )
    
    state = manager.get_server_state("godot")
    assert state.error_count == 1
    assert state.last_error == "Test error"


def test_log_operation(state_file: Path):
    """Test logging operations."""
    manager = StateManager(state_file)
    
    # Initialize server
    manager.update_server_state("godot", status="running")
    
    # Log operation
    manager.log_operation(
        "godot",
        "read_scene",
        {"path": "test.tscn"},
        {"status": "success", "data": {}},
        123.45,
    )
    
    # Check state updated
    state = manager.get_server_state("godot")
    assert state.operations_count == 1
    assert state.last_operation_at is not None
    
    # Check log entry
    log = manager.get_operation_log(limit=1)
    assert len(log) == 1
    assert log[0].server_name == "godot"
    assert log[0].operation == "read_scene"
    assert log[0].status == "success"
    assert log[0].duration_ms == 123.45


def test_log_operation_error(state_file: Path):
    """Test logging failed operations."""
    manager = StateManager(state_file)
    
    manager.update_server_state("godot", status="running")
    
    # Log error
    manager.log_operation(
        "godot",
        "invalid_op",
        {},
        {"status": "error", "error": "Unknown operation"},
        10.0,
    )
    
    # Check error tracking
    state = manager.get_server_state("godot")
    assert state.error_count == 1
    assert state.last_error == "Unknown operation"
    
    # Check log
    log = manager.get_operation_log(limit=1)
    assert log[0].status == "error"
    assert log[0].error == "Unknown operation"


def test_get_all_states(state_file: Path):
    """Test getting all server states."""
    manager = StateManager(state_file)
    
    manager.update_server_state("godot", status="running")
    manager.update_server_state("blender", status="running")
    
    all_states = manager.get_all_states()
    
    assert len(all_states) == 2
    assert "godot" in all_states
    assert "blender" in all_states


def test_get_operation_log_filter(state_file: Path):
    """Test filtering operation log."""
    manager = StateManager(state_file)
    
    manager.update_server_state("godot", status="running")
    manager.update_server_state("blender", status="running")
    
    # Log operations for different servers
    manager.log_operation("godot", "op1", {}, {"status": "success"}, 10.0)
    manager.log_operation("blender", "op2", {}, {"status": "success"}, 20.0)
    manager.log_operation("godot", "op3", {}, {"status": "success"}, 30.0)
    
    # Get all logs
    all_logs = manager.get_operation_log()
    assert len(all_logs) == 3
    
    # Filter by server
    godot_logs = manager.get_operation_log(server_name="godot")
    assert len(godot_logs) == 2
    assert all(log.server_name == "godot" for log in godot_logs)


def test_state_persistence(state_file: Path):
    """Test state persistence across instances."""
    # Create first manager and add state
    manager1 = StateManager(state_file)
    manager1.update_server_state("godot", status="running", pid=1234)
    manager1.log_operation("godot", "test", {}, {"status": "success"}, 10.0)
    
    # Create second manager (should load existing state)
    manager2 = StateManager(state_file)
    
    state = manager2.get_server_state("godot")
    assert state is not None
    assert state.pid == 1234
    
    logs = manager2.get_operation_log()
    assert len(logs) == 1
    assert logs[0].operation == "test"


def test_clear_old_logs(state_file: Path):
    """Test clearing old logs."""
    manager = StateManager(state_file)
    manager.update_server_state("godot", status="running")
    
    # Add some logs
    for i in range(10):
        manager.log_operation("godot", f"op{i}", {}, {"status": "success"}, 10.0)
    
    # Manually set some logs to be old
    cutoff = datetime.now() - timedelta(days=8)
    for i in range(5):
        manager.operation_log[i].timestamp = cutoff
    
    # Clear old logs
    manager.clear_old_logs(days=7)
    
    # Should have 5 recent logs left
    logs = manager.get_operation_log()
    assert len(logs) == 5

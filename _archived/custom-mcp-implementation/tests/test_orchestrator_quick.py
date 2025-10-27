"""Quick test of orchestrator."""
import sys
import asyncio
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from servers.common.orchestrator import ServerOrchestrator
from servers.common.config import ServerConfig, GlobalConfig
import json
import tempfile

async def test_orchestrator():
    """Test orchestrator basic functionality."""
    # Create temp config
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        config_file = tmp_path / "test-config.json"
        
        # Create working directory
        project_dir = tmp_path / "godot_project"
        project_dir.mkdir()
        (project_dir / "project.godot").write_text("")
        
        # Create config
        config = GlobalConfig(
            log_level="INFO",
            log_directory="logs",
            state_file="state/mcp-state.json",
            servers={
                "godot": ServerConfig(
                    enabled=True,
                    executable_path="C:\\fake\\godot.exe",
                    auto_detect=False,
                    working_directory=str(project_dir),
                ),
            },
        )
        
        config_file.write_text(json.dumps(config.model_dump(), indent=2))
        
        # Test orchestrator
        orchestrator = ServerOrchestrator(config_file)
        
        print("Initializing orchestrator...")
        success = await orchestrator.initialize()
        print(f"Initialized: {success}")
        
        if success:
            print(f"Servers: {list(orchestrator.servers.keys())}")
            print(f"Running: {orchestrator.get_running_servers()}")
            print(f"Healthy: {orchestrator.is_healthy()}")
            
            # Test operation
            result = orchestrator.execute_operation("godot", "list_scenes", {})
            print(f"Operation result: {result['status']}")
            
            await orchestrator.shutdown()
            print("Shutdown complete")
            
            return True
        else:
            print("Failed to initialize")
            return False

if __name__ == "__main__":
    result = asyncio.run(test_orchestrator())
    sys.exit(0 if result else 1)

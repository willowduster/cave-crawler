"""Server orchestrator for managing multiple MCP servers."""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
import psutil

from servers.common.config import load_config, GlobalConfig
from servers.common.models import MCPServerState, DetectedTools
from servers.godot.godot_server import GodotMCPServer


class ServerOrchestrator:
    """Manages lifecycle of multiple MCP servers."""
    
    def __init__(self, config_path: str | Path):
        """
        Initialize orchestrator.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config: Optional[GlobalConfig] = None
        self.servers: Dict[str, any] = {}
        self.server_states: Dict[str, MCPServerState] = {}
        self.logger = logging.getLogger(__name__)
        
    async def initialize(self) -> bool:
        """
        Load configuration and initialize servers.
        
        Returns:
            True if successful
        """
        # Load config
        self.config = load_config(str(self.config_path))
        
        # Initialize each enabled server
        for name, server_config in self.config.servers.items():
            if not server_config.enabled:
                self.logger.info(f"Server '{name}' is disabled")
                continue
                
            self.logger.info(f"Initializing server: {name}")
            
            # Create server instance based on type
            server = None
            if name == "godot":
                server = GodotMCPServer(
                    server_config,
                    f"logs/{name}-mcp.log"
                )
            # Add other server types here
            # elif name == "blender":
            #     server = BlenderMCPServer(...)
            # elif name == "gimp":
            #     server = GIMPMCPServer(...)
            
            if server:
                # Try to initialize
                try:
                    server.initialize()
                    self.servers[name] = server
                    
                    # Update state
                    self.server_states[name] = MCPServerState(
                        name=name,
                        status="running",
                        pid=psutil.Process().pid,  # Current process
                        started_at=None,  # Will be set by state manager
                        operations_count=0,
                        last_operation_at=None,
                        error_count=0,
                        last_error=None,
                    )
                    
                    self.logger.info(f"Server '{name}' initialized successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize server '{name}': {e}")
                    self.server_states[name] = MCPServerState(
                        name=name,
                        status="error",
                        pid=None,
                        started_at=None,
                        operations_count=0,
                        last_operation_at=None,
                        error_count=1,
                        last_error=str(e),
                    )
            else:
                self.logger.warning(f"Unknown server type: {name}")
        
        return len(self.servers) > 0
    
    async def shutdown(self):
        """Shutdown all servers gracefully."""
        self.logger.info("Shutting down all servers...")
        
        for name, server in self.servers.items():
            self.logger.info(f"Shutting down server: {name}")
            try:
                server.shutdown()
            except Exception as e:
                self.logger.error(f"Error shutting down {name}: {e}")
        
        self.servers.clear()
        self.server_states.clear()
        
        self.logger.info("All servers shut down")
    
    def execute_operation(
        self,
        server_name: str,
        operation: str,
        params: Dict
    ) -> Dict:
        """
        Execute an operation on a specific server.
        
        Args:
            server_name: Name of the server
            operation: Operation to execute
            params: Operation parameters
            
        Returns:
            Operation result
        """
        if server_name not in self.servers:
            return {
                "status": "error",
                "error": f"Server '{server_name}' not found or not running",
            }
        
        server = self.servers[server_name]
        
        try:
            result = server.execute_operation(operation, params)
            
            # Update state
            if server_name in self.server_states:
                state = self.server_states[server_name]
                state.operations_count += 1
                state.last_operation_at = None  # Will be set by state manager
                
                if result.get("status") == "error":
                    state.error_count += 1
                    state.last_error = result.get("error")
            
            return result
        except Exception as e:
            self.logger.error(f"Error executing operation on '{server_name}': {e}")
            
            # Update state
            if server_name in self.server_states:
                state = self.server_states[server_name]
                state.error_count += 1
                state.last_error = str(e)
            
            return {
                "status": "error",
                "error": str(e),
            }
    
    def get_server_state(self, server_name: str) -> Optional[MCPServerState]:
        """
        Get state of a specific server.
        
        Args:
            server_name: Name of the server
            
        Returns:
            Server state or None
        """
        return self.server_states.get(server_name)
    
    def get_all_states(self) -> Dict[str, MCPServerState]:
        """
        Get states of all servers.
        
        Returns:
            Dictionary of server states
        """
        return self.server_states.copy()
    
    def get_running_servers(self) -> List[str]:
        """
        Get list of running server names.
        
        Returns:
            List of server names
        """
        return [
            name for name, state in self.server_states.items()
            if state.status == "running"
        ]
    
    def is_healthy(self) -> bool:
        """
        Check if all servers are healthy.
        
        Returns:
            True if all servers are running without errors
        """
        if not self.servers:
            return False
        
        for state in self.server_states.values():
            if state.status != "running":
                return False
        
        return True

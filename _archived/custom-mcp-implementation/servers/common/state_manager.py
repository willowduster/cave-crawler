"""State manager for tracking MCP server state."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from threading import Lock

from servers.common.models import MCPServerState, OperationLogEntry
from servers.common.file_lock import FileLock
from servers.common.atomic_write import atomic_write


class StateManager:
    """Manages persistent state for MCP servers."""
    
    def __init__(self, state_file: str | Path):
        """
        Initialize state manager.
        
        Args:
            state_file: Path to state file
        """
        self.state_file = Path(state_file)
        self.state_lock = Lock()
        self.logger = logging.getLogger(__name__)
        
        # Ensure directory exists
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing state
        self.states: Dict[str, MCPServerState] = {}
        self.operation_log: list[OperationLogEntry] = []
        self._load_state()
    
    def _load_state(self):
        """Load state from file."""
        if not self.state_file.exists():
            self.logger.info("No existing state file found")
            return
        
        try:
            with FileLock(str(self.state_file)):
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                
                # Load server states
                if "servers" in data:
                    for name, state_dict in data["servers"].items():
                        self.states[name] = MCPServerState(**state_dict)
                
                # Load operation log
                if "operation_log" in data:
                    for entry_dict in data["operation_log"]:
                        self.operation_log.append(OperationLogEntry(**entry_dict))
                
                self.logger.info(f"Loaded state for {len(self.states)} servers")
        except Exception as e:
            self.logger.error(f"Failed to load state: {e}")
    
    def _save_state(self):
        """Save state to file."""
        try:
            with self.state_lock:
                data = {
                    "servers": {
                        name: state.model_dump()
                        for name, state in self.states.items()
                    },
                    "operation_log": [
                        entry.model_dump()
                        for entry in self.operation_log[-1000:]  # Keep last 1000 entries
                    ],
                }
                
                atomic_write(
                    str(self.state_file),
                    json.dumps(data, indent=2, default=str)
                )
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
    
    def update_server_state(
        self,
        server_name: str,
        status: Optional[str] = None,
        pid: Optional[int] = None,
        error: Optional[str] = None,
    ):
        """
        Update state of a server.
        
        Args:
            server_name: Name of the server
            status: New status
            pid: Process ID
            error: Error message if any
        """
        with self.state_lock:
            if server_name not in self.states:
                self.states[server_name] = MCPServerState(
                    name=server_name,
                    status=status or "unknown",
                    pid=pid,
                    started_at=datetime.now() if status == "running" else None,
                    operations_count=0,
                    last_operation_at=None,
                    error_count=0,
                    last_error=None,
                )
            else:
                state = self.states[server_name]
                
                if status:
                    state.status = status
                    if status == "running" and not state.started_at:
                        state.started_at = datetime.now()
                
                if pid is not None:
                    state.pid = pid
                
                if error:
                    state.error_count += 1
                    state.last_error = error
            
            self._save_state()
    
    def log_operation(
        self,
        server_name: str,
        operation: str,
        params: Dict,
        result: Dict,
        duration_ms: float,
    ):
        """
        Log an operation execution.
        
        Args:
            server_name: Name of the server
            operation: Operation name
            params: Operation parameters
            result: Operation result
            duration_ms: Execution duration in milliseconds
        """
        with self.state_lock:
            # Update server state
            if server_name in self.states:
                state = self.states[server_name]
                state.operations_count += 1
                state.last_operation_at = datetime.now()
                
                if result.get("status") == "error":
                    state.error_count += 1
                    state.last_error = result.get("error")
            
            # Add to log
            entry = OperationLogEntry(
                timestamp=datetime.now(),
                server_name=server_name,
                operation=operation,
                params=params,
                status=result.get("status", "unknown"),
                duration_ms=duration_ms,
                error=result.get("error"),
            )
            self.operation_log.append(entry)
            
            self._save_state()
    
    def get_server_state(self, server_name: str) -> Optional[MCPServerState]:
        """
        Get state of a specific server.
        
        Args:
            server_name: Name of the server
            
        Returns:
            Server state or None
        """
        with self.state_lock:
            return self.states.get(server_name)
    
    def get_all_states(self) -> Dict[str, MCPServerState]:
        """
        Get states of all servers.
        
        Returns:
            Dictionary of server states
        """
        with self.state_lock:
            return self.states.copy()
    
    def get_operation_log(
        self,
        server_name: Optional[str] = None,
        limit: int = 100
    ) -> list[OperationLogEntry]:
        """
        Get operation log entries.
        
        Args:
            server_name: Filter by server name (optional)
            limit: Maximum number of entries
            
        Returns:
            List of log entries
        """
        with self.state_lock:
            entries = self.operation_log
            
            if server_name:
                entries = [e for e in entries if e.server_name == server_name]
            
            return entries[-limit:]
    
    def clear_old_logs(self, days: int = 7):
        """
        Clear operation logs older than specified days.
        
        Args:
            days: Number of days to keep
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        with self.state_lock:
            self.operation_log = [
                entry for entry in self.operation_log
                if entry.timestamp.timestamp() > cutoff
            ]
            
            self._save_state()
            
            self.logger.info(f"Cleared logs older than {days} days")

"""Data models for MCP operations and state management."""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ToolInstallation(BaseModel):
    """Information about a detected tool installation."""
    
    executable_path: str
    version: Optional[str] = None
    installation_path: Optional[str] = None
    detection_method: str = "unknown"
    detected_at: datetime = Field(default_factory=datetime.now)


class MCPOperationRequest(BaseModel):
    """Request for an MCP operation."""
    
    operation: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    timeout: Optional[int] = None
    request_id: Optional[str] = None


class MCPOperationResponse(BaseModel):
    """Response from an MCP operation."""
    
    status: str  # "success" or "error"
    data: Optional[Any] = None
    error: Optional[str] = None
    details: Optional[str] = None
    execution_time: Optional[float] = None


class OperationLogEntry(BaseModel):
    """Log entry for an operation execution."""
    
    timestamp: datetime = Field(default_factory=datetime.now)
    server_name: str
    operation: str
    params: Dict[str, Any] = Field(default_factory=dict)
    status: str
    duration_ms: float
    error: Optional[str] = None


class MCPServerState(BaseModel):
    """State information for an MCP server."""
    
    name: str
    status: str  # "running", "stopped", "error", "unknown"
    pid: Optional[int] = None
    started_at: Optional[datetime] = None
    operations_count: int = 0
    last_operation_at: Optional[datetime] = None
    error_count: int = 0
    last_error: Optional[str] = None


class DetectedTools(BaseModel):
    """Collection of detected tool installations."""
    
    godot: Optional[ToolInstallation] = None
    blender: Optional[ToolInstallation] = None
    gimp: Optional[ToolInstallation] = None
    detection_timestamp: datetime = Field(default_factory=datetime.now)

"""Base MCP server class.

Provides abstract base for tool-specific MCP servers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
from servers.common.logger import setup_logger
from servers.common.config import ServerConfig


class BaseMCPServer(ABC):
    """Abstract base class for MCP servers.
    
    Subclasses must implement:
    - initialize(): Set up server-specific resources
    - shutdown(): Clean up resources
    - execute_operation(): Handle tool-specific operations
    """
    
    def __init__(
        self,
        name: str,
        config: ServerConfig,
        log_file: str,
        log_level: str = "INFO",
    ):
        """Initialize base server.
        
        Args:
            name: Server name (e.g., "godot", "blender")
            config: Server configuration
            log_file: Path to log file
            log_level: Logging level
        """
        self.name = name
        self.config = config
        self.logger = setup_logger(
            f"mcp.{name}",
            log_file,
            level=getattr(logging, log_level),
        )
        self._initialized = False
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize server-specific resources.
        
        Called once before server starts handling operations.
        Subclasses should:
        - Validate tool installation
        - Set up working directory
        - Prepare any necessary resources
        
        Raises:
            RuntimeError: If initialization fails
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Clean up server resources.
        
        Called when server is shutting down.
        Subclasses should:
        - Close any open connections
        - Save state if needed
        - Clean up temporary files
        """
        pass
    
    @abstractmethod
    def execute_operation(
        self,
        operation: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute a tool-specific operation.
        
        Args:
            operation: Operation name (e.g., "create_scene")
            parameters: Operation parameters
        
        Returns:
            Operation result with status and data
        
        Raises:
            ValueError: If operation is unknown
            RuntimeError: If operation fails
        """
        pass
    
    def is_initialized(self) -> bool:
        """Check if server is initialized.
        
        Returns:
            True if server is ready to handle operations
        """
        return self._initialized
    
    def _set_initialized(self, value: bool) -> None:
        """Set initialization status.
        
        Args:
            value: Initialization status
        """
        self._initialized = value
        if value:
            self.logger.info(f"{self.name} server initialized successfully")
        else:
            self.logger.warning(f"{self.name} server marked as not initialized")
    
    def validate_parameters(
        self,
        parameters: Dict[str, Any],
        required: list[str],
        optional: Optional[list[str]] = None,
    ) -> None:
        """Validate operation parameters.
        
        Args:
            parameters: Parameters to validate
            required: Required parameter names
            optional: Optional parameter names (default: [])
        
        Raises:
            ValueError: If required parameters are missing or unknown parameters present
        """
        optional = optional or []
        
        # Check required parameters
        missing = [p for p in required if p not in parameters]
        if missing:
            raise ValueError(f"Missing required parameters: {missing}")
        
        # Check for unknown parameters
        allowed = set(required) | set(optional)
        unknown = [p for p in parameters if p not in allowed]
        if unknown:
            raise ValueError(f"Unknown parameters: {unknown}")
    
    def create_success_response(
        self,
        data: Any,
        message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create successful operation response.
        
        Args:
            data: Operation result data
            message: Optional success message
        
        Returns:
            Standardized success response
        """
        response = {
            "status": "success",
            "data": data,
        }
        if message:
            response["message"] = message
        return response
    
    def create_error_response(
        self,
        error: str,
        details: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create error operation response.
        
        Args:
            error: Error message
            details: Optional error details
        
        Returns:
            Standardized error response
        """
        response = {
            "status": "error",
            "error": error,
        }
        if details:
            response["details"] = details
        return response

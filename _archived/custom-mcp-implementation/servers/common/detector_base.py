"""Base tool detector class.

Provides abstract base for detecting tool installations on Windows.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List
import os
import logging
import winreg


class ToolInstallation:
    """Information about a detected tool installation."""
    
    def __init__(
        self,
        executable_path: str,
        version: Optional[str] = None,
        installation_path: Optional[str] = None,
        detection_method: str = "unknown",
    ):
        """Initialize tool installation info.
        
        Args:
            executable_path: Full path to tool executable
            version: Tool version string
            installation_path: Installation directory
            detection_method: How tool was detected
        """
        self.executable_path = executable_path
        self.version = version
        self.installation_path = installation_path
        self.detection_method = detection_method
    
    def to_dict(self) -> dict:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "executable_path": self.executable_path,
            "version": self.version,
            "installation_path": self.installation_path,
            "detection_method": self.detection_method,
        }


class BaseDetector(ABC):
    """Abstract base class for tool detectors.
    
    Provides common detection methods for Windows tools.
    Subclasses must implement tool-specific registry keys and paths.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize detector.
        
        Args:
            logger: Logger instance (optional)
        """
        self.logger = logger or logging.getLogger(__name__)
    
    @abstractmethod
    def get_registry_keys(self) -> List[str]:
        """Get Windows registry keys to check.
        
        Returns:
            List of registry key paths
        """
        pass
    
    @abstractmethod
    def get_common_paths(self) -> List[str]:
        """Get common installation paths to check.
        
        Returns:
            List of directory paths
        """
        pass
    
    @abstractmethod
    def get_executable_name(self) -> str:
        """Get executable filename.
        
        Returns:
            Executable name (e.g., "godot.exe")
        """
        pass
    
    @abstractmethod
    def extract_version(self, executable_path: str) -> Optional[str]:
        """Extract version from tool executable.
        
        Args:
            executable_path: Path to executable
        
        Returns:
            Version string or None if cannot determine
        """
        pass
    
    def detect(self, methods: Optional[List[str]] = None) -> Optional[ToolInstallation]:
        """Detect tool installation using specified methods.
        
        Args:
            methods: Detection methods to try (default: all)
                     Options: "registry", "path", "common_paths"
        
        Returns:
            ToolInstallation if found, None otherwise
        """
        methods = methods or ["registry", "path", "common_paths"]
        
        for method in methods:
            if method == "registry":
                result = self._detect_from_registry()
                if result:
                    return result
            elif method == "path":
                result = self._detect_from_path()
                if result:
                    return result
            elif method == "common_paths":
                result = self._detect_from_common_paths()
                if result:
                    return result
            else:
                self.logger.warning(f"Unknown detection method: {method}")
        
        return None
    
    def _detect_from_registry(self) -> Optional[ToolInstallation]:
        """Detect tool from Windows registry.
        
        Returns:
            ToolInstallation if found, None otherwise
        """
        for reg_key in self.get_registry_keys():
            try:
                # Try HKEY_LOCAL_MACHINE
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key)
                path, _ = winreg.QueryValueEx(key, "InstallLocation")
                winreg.CloseKey(key)
                
                exe_path = Path(path) / self.get_executable_name()
                if exe_path.exists():
                    version = self.extract_version(str(exe_path))
                    self.logger.info(f"Found tool via registry: {exe_path}")
                    return ToolInstallation(
                        executable_path=str(exe_path),
                        version=version,
                        installation_path=path,
                        detection_method="registry",
                    )
            except (WindowsError, FileNotFoundError):
                continue
            
            try:
                # Try HKEY_CURRENT_USER
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key)
                path, _ = winreg.QueryValueEx(key, "InstallLocation")
                winreg.CloseKey(key)
                
                exe_path = Path(path) / self.get_executable_name()
                if exe_path.exists():
                    version = self.extract_version(str(exe_path))
                    self.logger.info(f"Found tool via registry (HKCU): {exe_path}")
                    return ToolInstallation(
                        executable_path=str(exe_path),
                        version=version,
                        installation_path=path,
                        detection_method="registry",
                    )
            except (WindowsError, FileNotFoundError):
                continue
        
        return None
    
    def _detect_from_path(self) -> Optional[ToolInstallation]:
        """Detect tool from system PATH.
        
        Returns:
            ToolInstallation if found, None otherwise
        """
        exe_name = self.get_executable_name()
        
        # Check each directory in PATH
        for directory in os.environ.get("PATH", "").split(os.pathsep):
            exe_path = Path(directory) / exe_name
            if exe_path.exists():
                version = self.extract_version(str(exe_path))
                self.logger.info(f"Found tool in PATH: {exe_path}")
                return ToolInstallation(
                    executable_path=str(exe_path),
                    version=version,
                    installation_path=directory,
                    detection_method="path",
                )
        
        return None
    
    def _detect_from_common_paths(self) -> Optional[ToolInstallation]:
        """Detect tool from common installation paths.
        
        Returns:
            ToolInstallation if found, None otherwise
        """
        exe_name = self.get_executable_name()
        
        for base_path in self.get_common_paths():
            # Expand environment variables
            expanded_path = os.path.expandvars(base_path)
            path = Path(expanded_path)
            
            if not path.exists():
                continue
            
            # Check direct path
            exe_path = path / exe_name
            if exe_path.exists():
                version = self.extract_version(str(exe_path))
                self.logger.info(f"Found tool in common path: {exe_path}")
                return ToolInstallation(
                    executable_path=str(exe_path),
                    version=version,
                    installation_path=str(path),
                    detection_method="common_paths",
                )
            
            # Check subdirectories (one level deep)
            if path.is_dir():
                for subdir in path.iterdir():
                    if subdir.is_dir():
                        exe_path = subdir / exe_name
                        if exe_path.exists():
                            version = self.extract_version(str(exe_path))
                            self.logger.info(f"Found tool in common path: {exe_path}")
                            return ToolInstallation(
                                executable_path=str(exe_path),
                                version=version,
                                installation_path=str(subdir),
                                detection_method="common_paths",
                            )
        
        return None

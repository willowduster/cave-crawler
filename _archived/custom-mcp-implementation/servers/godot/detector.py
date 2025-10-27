"""Godot Engine detector for Windows."""

from typing import List, Optional
import subprocess
import re
from pathlib import Path
from servers.common.detector_base import BaseDetector, ToolInstallation


class GodotDetector(BaseDetector):
    """Detector for Godot Engine installations on Windows."""
    
    def get_registry_keys(self) -> List[str]:
        """Get Windows registry keys to check for Godot.
        
        Returns:
            List of registry key paths
        """
        return [
            r"SOFTWARE\GodotEngine\Godot",
            r"SOFTWARE\Wow6432Node\GodotEngine\Godot",
        ]
    
    def get_common_paths(self) -> List[str]:
        """Get common installation paths for Godot.
        
        Returns:
            List of directory paths
        """
        return [
            r"C:\Program Files\Godot",
            r"C:\Program Files (x86)\Godot",
            r"%LOCALAPPDATA%\Godot",
            r"%APPDATA%\Godot",
            r"C:\Godot",
            # Steam installation paths
            r"C:\Program Files (x86)\Steam\steamapps\common\Godot Engine",
            r"C:\Program Files\Steam\steamapps\common\Godot Engine",
        ]
    
    def get_executable_name(self) -> str:
        """Get Godot executable filename.
        
        Returns:
            Executable name
        """
        return "Godot_v4-stable_win64.exe"  # Common name, will also check variations
    
    def extract_version(self, executable_path: str) -> Optional[str]:
        """Extract version from Godot executable.
        
        Args:
            executable_path: Path to Godot executable
        
        Returns:
            Version string or None
        """
        try:
            # Run Godot with --version flag
            result = subprocess.run(
                [executable_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5.0,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            # Parse version from output (e.g., "4.2.1.stable.official.b09f793f5")
            version_match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
            if version_match:
                return version_match.group(1)
                
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
        
        # Try to extract from filename (e.g., "Godot_v4.2.1-stable_win64.exe")
        filename = Path(executable_path).name
        version_match = re.search(r'v?(\d+\.\d+(?:\.\d+)?)', filename)
        if version_match:
            return version_match.group(1)
        
        return None
    
    def _detect_from_common_paths(self) -> Optional[ToolInstallation]:
        """Override to check for different Godot executable name variations.
        
        Returns:
            ToolInstallation if found, None otherwise
        """
        # Common Godot executable name patterns
        exe_patterns = [
            "Godot_v4*.exe",
            "Godot*.exe",
            "godot.exe",
        ]
        
        import os
        
        for base_path in self.get_common_paths():
            # Expand environment variables
            expanded_path = os.path.expandvars(base_path)
            path = Path(expanded_path)
            
            if not path.exists():
                continue
            
            # Try each exe pattern
            for pattern in exe_patterns:
                # Check direct path
                for exe_path in path.glob(pattern):
                    if exe_path.is_file():
                        version = self.extract_version(str(exe_path))
                        self.logger.info(f"Found Godot in common path: {exe_path}")
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
                            for exe_path in subdir.glob(pattern):
                                if exe_path.is_file():
                                    version = self.extract_version(str(exe_path))
                                    self.logger.info(f"Found Godot in common path: {exe_path}")
                                    return ToolInstallation(
                                        executable_path=str(exe_path),
                                        version=version,
                                        installation_path=str(subdir),
                                        detection_method="common_paths",
                                    )
        
        return None

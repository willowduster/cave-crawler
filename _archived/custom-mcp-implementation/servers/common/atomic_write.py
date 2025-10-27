"""Atomic write utility for safe file operations.

Provides atomic file writes with backup to prevent data corruption.
"""

import shutil
from pathlib import Path
from typing import Optional, Union
from servers.common.file_lock import FileLock


def atomic_write(
    file_path: str,
    content: Union[str, bytes],
    encoding: Optional[str] = "utf-8",
) -> None:
    """Write content to file atomically with backup.
    
    Steps:
    1. Acquire file lock
    2. Create backup of existing file (if exists)
    3. Write to temporary file
    4. Replace original with temporary file
    5. Release lock
    
    If any step fails, the original file is preserved.
    
    Args:
        file_path: Path to file to write
        content: Content to write (str or bytes)
        encoding: Text encoding (None for binary mode)
    
    Raises:
        IOError: If write operation fails
    """
    path = Path(file_path)
    temp_path = Path(str(file_path) + ".tmp")
    backup_path = Path(str(file_path) + ".backup")
    
    # Create parent directories if needed
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Acquire lock for safe concurrent access
    with FileLock(file_path, timeout=5.0):
        try:
            # Create backup of existing file
            if path.exists():
                shutil.copy2(path, backup_path)
            
            # Write to temporary file
            if encoding is None:
                # Binary mode
                temp_path.write_bytes(content)  # type: ignore
            else:
                # Text mode
                temp_path.write_text(content, encoding=encoding)  # type: ignore
            
            # Replace original with temp file
            temp_path.replace(path)
            
        except Exception as e:
            # Clean up temp file if it exists
            if temp_path.exists():
                temp_path.unlink()
            
            # Restore from backup if available
            if backup_path.exists() and not path.exists():
                shutil.copy2(backup_path, path)
            
            raise IOError(f"Failed to write {file_path}: {e}") from e

"""File locking utility for safe concurrent file access.

Provides cross-platform file locking to prevent concurrent modifications.
Uses OS-level file locking on Windows via msvcrt.
"""

import time
import msvcrt
import os
from pathlib import Path
from typing import Optional


class LockTimeout(Exception):
    """Raised when file lock acquisition times out."""
    pass


class FileLock:
    """Context manager for file locking.
    
    Uses Windows msvcrt file locking for proper OS-level locks.
    
    Example:
        >>> with FileLock("myfile.txt", timeout=5.0):
        ...     # Safe to modify file
        ...     pass
    """
    
    def __init__(self, file_path: str, timeout: float = 10.0):
        """Initialize file lock.
        
        Args:
            file_path: Path to file to lock
            timeout: Maximum time to wait for lock (seconds)
        """
        self.file_path = Path(file_path)
        self.lock_file = Path(str(file_path) + ".lock")
        self.timeout = timeout
        self.acquired = False
        self.lock_handle = None
    
    def __enter__(self) -> "FileLock":
        """Acquire the lock."""
        start_time = time.time()
        
        # Create lock file if it doesn't exist
        self.lock_file.touch(exist_ok=True)
        
        while True:
            try:
                # Open lock file and try to acquire exclusive lock
                self.lock_handle = open(self.lock_file, 'r+')
                msvcrt.locking(self.lock_handle.fileno(), msvcrt.LK_NBLCK, 1)
                self.acquired = True
                return self
            except (OSError, IOError):
                # Could not acquire lock
                if self.lock_handle:
                    self.lock_handle.close()
                    self.lock_handle = None
                
                elapsed = time.time() - start_time
                if elapsed >= self.timeout:
                    raise LockTimeout(
                        f"Failed to acquire lock on {self.file_path} "
                        f"within {self.timeout} seconds"
                    )
                # Wait a bit before retrying
                time.sleep(0.05)
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Release the lock."""
        if self.acquired and self.lock_handle:
            try:
                msvcrt.locking(self.lock_handle.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass
            finally:
                self.lock_handle.close()
                self.acquired = False
                # Clean up lock file
                try:
                    if self.lock_file.exists():
                        self.lock_file.unlink()
                except:
                    pass

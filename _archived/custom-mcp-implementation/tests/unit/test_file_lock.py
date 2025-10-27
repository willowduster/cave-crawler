"""Unit tests for file locking utility."""

import pytest
import time
from pathlib import Path
from threading import Thread
from servers.common.file_lock import FileLock, LockTimeout


def test_file_lock_creates_lock_file(tmp_path: Path) -> None:
    """Test that FileLock creates a lock file."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    
    with FileLock(str(file_path), timeout=1.0):
        lock_file = Path(str(file_path) + ".lock")
        assert lock_file.exists()
    
    # Lock file should be removed after context exit
    assert not lock_file.exists()


def test_file_lock_prevents_concurrent_access(tmp_path: Path) -> None:
    """Test that FileLock prevents concurrent access to the same file."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    
    lock_acquired = []
    
    def acquire_lock() -> None:
        try:
            with FileLock(str(file_path), timeout=0.5):
                lock_acquired.append(True)
                time.sleep(0.5)  # Hold lock longer
        except LockTimeout:
            lock_acquired.append(False)
    
    # First thread acquires lock
    thread1 = Thread(target=acquire_lock)
    thread1.start()
    time.sleep(0.2)  # Ensure thread1 has lock
    
    # Second thread should timeout
    thread2 = Thread(target=acquire_lock)
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    assert lock_acquired[0] is True
    assert lock_acquired[1] is False


def test_file_lock_timeout_raises_exception(tmp_path: Path) -> None:
    """Test that FileLock raises LockTimeout when timeout is exceeded."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    
    # Acquire lock in first context
    lock1 = FileLock(str(file_path), timeout=1.0)
    lock1.__enter__()
    
    try:
        # Second lock should timeout immediately
        with pytest.raises(LockTimeout):
            with FileLock(str(file_path), timeout=0.1):
                pass
    finally:
        lock1.__exit__(None, None, None)


def test_file_lock_releases_on_exception(tmp_path: Path) -> None:
    """Test that FileLock releases lock even when exception occurs."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    
    try:
        with FileLock(str(file_path), timeout=1.0):
            raise ValueError("Test exception")
    except ValueError:
        pass
    
    # Lock should be released, second acquisition should succeed
    with FileLock(str(file_path), timeout=0.5):
        assert True


def test_file_lock_with_nonexistent_file(tmp_path: Path) -> None:
    """Test that FileLock works with nonexistent files."""
    file_path = tmp_path / "nonexistent.txt"
    
    with FileLock(str(file_path), timeout=1.0):
        lock_file = Path(str(file_path) + ".lock")
        assert lock_file.exists()

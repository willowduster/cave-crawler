"""Test runner for final verification."""
import subprocess
import sys
from pathlib import Path

def run_test_group(name: str, test_files: list[str]) -> tuple[bool, str]:
    """Run a group of tests."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    cmd = [
        sys.executable,
        "-m", "pytest",
        *test_files,
        "-v",
        "--tb=short",
        "-q"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Parse output for passed/failed
    output = result.stdout + result.stderr
    
    if result.returncode == 0:
        print(f"✅ {name}: PASSED")
        return True, output
    else:
        print(f"❌ {name}: FAILED")
        return False, output

def main():
    """Run all test groups."""
    base_path = Path(__file__).parent
    tests_dir = base_path / "tests" / "unit"
    
    test_groups = [
        ("Logger", [str(tests_dir / "test_logger.py")]),
        ("File Lock", [str(tests_dir / "test_file_lock.py")]),
        ("Atomic Write", [str(tests_dir / "test_atomic_write.py")]),
        ("Config", [str(tests_dir / "test_config.py")]),
        ("Scene Parser", [str(tests_dir / "test_scene_parser.py")]),
        ("Godot Server", [str(tests_dir / "test_godot_server.py")]),
        ("State Manager", [str(tests_dir / "test_state_manager.py")]),
    ]
    
    results = []
    outputs = []
    
    for name, files in test_groups:
        success, output = run_test_group(name, files)
        results.append((name, success))
        outputs.append((name, output))
    
    # Summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} test groups passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test group(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

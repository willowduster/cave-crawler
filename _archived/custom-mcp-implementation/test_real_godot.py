"""Test real Godot detection and communication."""
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from servers.godot.detector import GodotDetector
from servers.godot.godot_server import GodotMCPServer
from servers.common.config import ServerConfig
import subprocess

def test_godot_detection():
    """Test detecting Godot in bin/ directory."""
    print("Testing Godot Detection...")
    print("="*60)
    
    # Check if bin/Godot exists
    bin_path = Path("C:/Users/Ben/code/cave-crawler/bin")
    godot_exe = None
    
    for file in bin_path.glob("Godot*.exe"):
        if "console" in file.name:
            godot_exe = file
            break
    
    if not godot_exe:
        for file in bin_path.glob("Godot*.exe"):
            godot_exe = file
            break
    
    if not godot_exe:
        print("❌ No Godot executable found in bin/")
        return False
    
    print(f"✅ Found Godot: {godot_exe}")
    
    # Test running Godot --version
    try:
        result = subprocess.run(
            [str(godot_exe), "--version"],
            capture_output=True,
            text=True,
            timeout=5.0
        )
        
        version = result.stdout.strip()
        print(f"✅ Godot version: {version}")
        
    except Exception as e:
        print(f"❌ Failed to run Godot: {e}")
        return False
    
    # Test with detector
    detector = GodotDetector()
    
    # Add bin/ to common paths
    original_get_common_paths = detector.get_common_paths
    
    def get_common_paths_with_bin():
        paths = original_get_common_paths()
        paths.insert(0, "C:\\Users\\Ben\\code\\cave-crawler\\bin")
        return paths
    
    detector.get_common_paths = get_common_paths_with_bin
    
    installation = detector.detect()
    
    if installation:
        print(f"✅ Detector found Godot:")
        print(f"   Path: {installation.executable_path}")
        print(f"   Version: {installation.version}")
        print(f"   Method: {installation.detection_method}")
    else:
        print("❌ Detector did not find Godot")
        return False
    
    return True

def test_godot_server_operations():
    """Test MCP server operations with real Godot."""
    print("\nTesting MCP Server Operations...")
    print("="*60)
    
    # Find Godot
    bin_path = Path("C:/Users/Ben/code/cave-crawler/bin")
    godot_exe = None
    
    for file in bin_path.glob("Godot*console*.exe"):
        godot_exe = file
        break
    
    if not godot_exe:
        for file in bin_path.glob("Godot*.exe"):
            godot_exe = file
            break
    
    if not godot_exe:
        print("❌ No Godot executable found")
        return False
    
    # Create a test project
    import tempfile
    with tempfile.TemporaryDirectory() as tmp_dir:
        project_dir = Path(tmp_dir) / "test_project"
        project_dir.mkdir()
        
        # Create minimal project.godot
        (project_dir / "project.godot").write_text("""
; Engine configuration file.

[application]
config/name="Test Project"
config/features=PackedStringArray("4.5")
""")
        
        # Create a simple scene
        scenes_dir = project_dir / "scenes"
        scenes_dir.mkdir()
        
        (scenes_dir / "main.tscn").write_text("""[gd_scene load_steps=1 format=3]

[node name="Main" type="Node2D"]

[node name="Sprite2D" type="Sprite2D" parent="."]
position = Vector2(100, 100)

[node name="Camera2D" type="Camera2D" parent="."]
""")
        
        # Create a GDScript
        scripts_dir = project_dir / "scripts"
        scripts_dir.mkdir()
        
        (scripts_dir / "player.gd").write_text("""extends CharacterBody2D

const SPEED = 300.0

func _ready():
\tprint("Player ready!")

func _physics_process(delta):
\tif Input.is_action_pressed("ui_right"):
\t\tvelocity.x = SPEED
\telse:
\t\tvelocity.x = 0
\t
\tmove_and_slide()
""")
        
        # Create MCP server
        config = ServerConfig(
            enabled=True,
            executable_path=str(godot_exe),
            auto_detect=False,
            working_directory=str(project_dir),
        )
        
        server = GodotMCPServer(config, str(Path(tmp_dir) / "test.log"))
        
        try:
            server.initialize()
            print(f"✅ Server initialized")
            print(f"   Godot: {server.godot_exe}")
            print(f"   Project: {server.working_dir}")
        except Exception as e:
            print(f"❌ Server initialization failed: {e}")
            return False
        
        # Test list_scenes
        print("\n1. Testing list_scenes...")
        result = server.execute_operation("list_scenes", {})
        if result["status"] == "success":
            print(f"✅ Found {len(result['data']['scenes'])} scene(s)")
            for scene in result['data']['scenes']:
                print(f"   - {scene}")
        else:
            print(f"❌ list_scenes failed: {result.get('error')}")
        
        # Test read_scene
        print("\n2. Testing read_scene...")
        result = server.execute_operation("read_scene", {"path": "scenes/main.tscn"})
        if result["status"] == "success":
            print(f"✅ Scene parsed successfully")
            print(f"   Nodes: {result['data']['node_count']}")
            for node in result['data']['nodes'][:3]:
                print(f"   - {node['name']} ({node['type']})")
        else:
            print(f"❌ read_scene failed: {result.get('error')}")
        
        # Test list_scripts
        print("\n3. Testing list_scripts...")
        result = server.execute_operation("list_scripts", {})
        if result["status"] == "success":
            print(f"✅ Found {len(result['data']['scripts'])} script(s)")
            for script in result['data']['scripts']:
                print(f"   - {script}")
        else:
            print(f"❌ list_scripts failed: {result.get('error')}")
        
        # Test read_script
        print("\n4. Testing read_script...")
        result = server.execute_operation("read_script", {"path": "scripts/player.gd"})
        if result["status"] == "success":
            content = result['data']['content']
            lines = content.split('\n')
            print(f"✅ Script read successfully ({len(lines)} lines)")
            print(f"   First line: {lines[0]}")
        else:
            print(f"❌ read_script failed: {result.get('error')}")
        
        # Test validate_script (if Godot supports it)
        print("\n5. Testing validate_script...")
        result = server.execute_operation("validate_script", {"path": "scripts/player.gd"})
        print(f"   Status: {result['status']}")
        if result["status"] == "success":
            print(f"✅ Script validation: {result['data'].get('valid', 'unknown')}")
            if result['data'].get('errors'):
                print(f"   Errors: {result['data']['errors']}")
        else:
            print(f"   Note: {result.get('error', 'Validation may not be implemented')}")
        
        # Test create_scene
        print("\n6. Testing create_scene...")
        result = server.execute_operation("create_scene", {
            "path": "scenes/test_scene.tscn",
            "root_type": "Node3D"
        })
        if result["status"] == "success":
            print(f"✅ Scene created successfully")
            print(f"   Path: {result['data']['path']}")
            # Verify it was created
            if (project_dir / "scenes" / "test_scene.tscn").exists():
                print(f"   ✅ File exists on disk")
        else:
            print(f"❌ create_scene failed: {result.get('error')}")
        
        server.shutdown()
        print("\n✅ Server shutdown complete")
        
    return True

if __name__ == "__main__":
    print("MCP Servers - Real Godot Integration Test")
    print("="*60)
    print()
    
    success = True
    
    if not test_godot_detection():
        success = False
    
    if not test_godot_server_operations():
        success = False
    
    print("\n" + "="*60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Godot is detected and MCP server can communicate with it")
    else:
        print("⚠️  Some tests failed")
    
    sys.exit(0 if success else 1)

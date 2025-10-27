"""Unit tests for Godot scene parser."""

import pytest
from pathlib import Path
from servers.godot.scene_parser import GodotScene


def test_parse_simple_scene(tmp_path: Path) -> None:
    """Test parsing a simple scene file."""
    scene_content = """[gd_scene load_steps=1 format=3]

[node name="Root" type="Node2D"]

[node name="Sprite" type="Sprite2D" parent="."]
position = Vector2(100, 100)

[node name="Camera" type="Camera2D" parent="."]
"""
    scene_file = tmp_path / "test.tscn"
    scene_file.write_text(scene_content)
    
    scene = GodotScene(str(scene_file))
    
    assert len(scene.get_nodes()) == 3
    assert scene.get_node_by_name("Root")["type"] == "Node2D"
    assert scene.get_node_by_name("Sprite")["type"] == "Sprite2D"
    assert scene.get_node_by_name("Camera")["type"] == "Camera2D"


def test_parse_scene_with_resources(tmp_path: Path) -> None:
    """Test parsing scene with external resources."""
    scene_content = """[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://player.gd" id="1"]

[node name="Player" type="CharacterBody2D"]
script = ExtResource("1")
"""
    scene_file = tmp_path / "test.tscn"
    scene_file.write_text(scene_content)
    
    scene = GodotScene(str(scene_file))
    
    assert len(scene.get_resources()) == 1
    scripts = scene.get_script_resources()
    assert "res://player.gd" in scripts


def test_get_nodes_by_type(tmp_path: Path) -> None:
    """Test filtering nodes by type."""
    scene_content = """[gd_scene load_steps=1 format=3]

[node name="Root" type="Node2D"]

[node name="Sprite1" type="Sprite2D" parent="."]

[node name="Sprite2" type="Sprite2D" parent="."]

[node name="Camera" type="Camera2D" parent="."]
"""
    scene_file = tmp_path / "test.tscn"
    scene_file.write_text(scene_content)
    
    scene = GodotScene(str(scene_file))
    
    sprites = scene.get_nodes_by_type("Sprite2D")
    assert len(sprites) == 2
    assert all(n["type"] == "Sprite2D" for n in sprites)


def test_scene_to_dict(tmp_path: Path) -> None:
    """Test converting scene to dictionary."""
    scene_content = """[gd_scene load_steps=1 format=3]

[node name="Root" type="Node2D"]
"""
    scene_file = tmp_path / "test.tscn"
    scene_file.write_text(scene_content)
    
    scene = GodotScene(str(scene_file))
    scene_dict = scene.to_dict()
    
    assert "file_path" in scene_dict
    assert "nodes" in scene_dict
    assert "resources" in scene_dict
    assert scene_dict["node_count"] == 1
    assert scene_dict["resource_count"] == 0


def test_nonexistent_scene(tmp_path: Path) -> None:
    """Test loading nonexistent scene."""
    scene_file = tmp_path / "nonexistent.tscn"
    scene = GodotScene(str(scene_file))
    
    assert len(scene.get_nodes()) == 0
    assert scene.content == ""

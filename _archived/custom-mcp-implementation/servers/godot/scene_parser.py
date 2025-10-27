"""Godot scene file (.tscn) parser and manipulator."""

from typing import Dict, List, Optional, Any
from pathlib import Path
import re


class GodotScene:
    """Represents a Godot scene file (.tscn).
    
    Provides methods to parse and query scene structure.
    """
    
    def __init__(self, file_path: str):
        """Initialize scene from file path.
        
        Args:
            file_path: Path to .tscn file
        """
        self.file_path = Path(file_path)
        self.content = ""
        self.nodes: List[Dict[str, Any]] = []
        self.resources: List[Dict[str, Any]] = []
        
        if self.file_path.exists():
            self.load()
    
    def load(self) -> None:
        """Load and parse the scene file."""
        self.content = self.file_path.read_text(encoding="utf-8")
        self._parse_nodes()
        self._parse_resources()
    
    def _parse_nodes(self) -> None:
        """Parse node definitions from scene content."""
        self.nodes = []
        
        # Pattern for node definitions: [node name="NodeName" type="NodeType" parent="."]
        node_pattern = re.compile(
            r'\[node\s+name="([^"]+)"\s+type="([^"]+)"(?:\s+parent="([^"]*)")?\]'
        )
        
        for match in node_pattern.finditer(self.content):
            node = {
                "name": match.group(1),
                "type": match.group(2),
                "parent": match.group(3) or ".",
            }
            self.nodes.append(node)
    
    def _parse_resources(self) -> None:
        """Parse external resource declarations."""
        self.resources = []
        
        # Pattern: [ext_resource type="Script" path="res://script.gd" id="1"]
        resource_pattern = re.compile(
            r'\[ext_resource\s+(?:type="([^"]+)")?\s*(?:path="([^"]+)")?\s*(?:id="([^"]+)")?\]'
        )
        
        for match in resource_pattern.finditer(self.content):
            resource = {
                "type": match.group(1),
                "path": match.group(2),
                "id": match.group(3),
            }
            self.resources.append(resource)
    
    def get_nodes(self) -> List[Dict[str, Any]]:
        """Get all nodes in the scene.
        
        Returns:
            List of node dictionaries
        """
        return self.nodes.copy()
    
    def get_node_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a node by its name.
        
        Args:
            name: Node name
        
        Returns:
            Node dictionary or None if not found
        """
        for node in self.nodes:
            if node["name"] == name:
                return node.copy()
        return None
    
    def get_nodes_by_type(self, node_type: str) -> List[Dict[str, Any]]:
        """Get all nodes of a specific type.
        
        Args:
            node_type: Node type (e.g., "Sprite2D", "Node2D")
        
        Returns:
            List of matching nodes
        """
        return [n.copy() for n in self.nodes if n["type"] == node_type]
    
    def get_resources(self) -> List[Dict[str, Any]]:
        """Get all external resources.
        
        Returns:
            List of resource dictionaries
        """
        return self.resources.copy()
    
    def get_script_resources(self) -> List[str]:
        """Get paths to all script resources.
        
        Returns:
            List of script file paths
        """
        return [
            r["path"] for r in self.resources
            if r["type"] == "Script" and r["path"]
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scene to dictionary representation.
        
        Returns:
            Dictionary with scene info
        """
        return {
            "file_path": str(self.file_path),
            "nodes": self.get_nodes(),
            "resources": self.get_resources(),
            "node_count": len(self.nodes),
            "resource_count": len(self.resources),
        }

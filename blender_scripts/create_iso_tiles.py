"""
Blender script to create isometric cave tiles
This creates proper isometric perspective tiles for the cave crawler game

Tile specifications:
- Base tile: 64x32 pixels (2:1 ratio)
- Isometric angle: 26.565° (arctan(0.5))
- Camera setup: Orthographic with isometric angle
- Output: PNG sprites with transparency
"""

import bpy
import math
import os

# Configuration
TILE_SIZE = 64  # Base width in pixels
TILE_HEIGHT_RATIO = 0.5  # Height is 0.5 of width (64x32)
ISO_ANGLE = math.atan(0.5)  # 26.565 degrees
RENDER_RESOLUTION = 128  # Higher res for better quality, will scale down
OUTPUT_DIR = "C:/Users/Ben/code/cave-crawler/assets/tiles"

def setup_scene():
    """Clear scene and set up for isometric rendering"""
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Clear existing materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    # Set up render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64  # Lower for faster renders
    scene.render.resolution_x = RENDER_RESOLUTION
    scene.render.resolution_y = int(RENDER_RESOLUTION * TILE_HEIGHT_RATIO)
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    
    return scene

def create_isometric_camera():
    """Create camera with isometric perspective"""
    # Create camera
    bpy.ops.object.camera_add(location=(0, 0, 10))
    camera = bpy.context.object
    camera.name = "IsoCamera"
    
    # Set to orthographic
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 3.0
    
    # Rotate for isometric view (45° around Z, then arctan(0.5) around X)
    camera.rotation_euler = (ISO_ANGLE, 0, math.radians(45))
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    return camera

def create_material(name, color, roughness=0.8):
    """Create a Principled BSDF material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Get Principled BSDF
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*color, 1.0)
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Specular IOR Level'].default_value = 0.2
    
    return mat

def create_floor_tile():
    """Create isometric floor tile"""
    # Create plane
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "FloorTile"
    
    # Apply material - dark stone color
    stone_color = (0.25, 0.2, 0.15)  # Dark brown/gray
    mat = create_material("StoneMaterial", stone_color, roughness=0.9)
    floor.data.materials.append(mat)
    
    # Add some geometry for detail
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=3)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return floor

def create_wall_tile():
    """Create isometric wall tile with height"""
    # Create cube for wall
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -1, 0.5))
    wall = bpy.context.object
    wall.name = "WallTile"
    wall.scale = (1, 0.1, 0.5)  # Thin wall with height
    
    # Apply material - slightly lighter stone
    wall_color = (0.3, 0.25, 0.2)
    mat = create_material("WallMaterial", wall_color, roughness=0.85)
    wall.data.materials.append(mat)
    
    return wall

def create_lighting():
    """Set up lighting for cave atmosphere"""
    # Remove default light
    if "Light" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)
    
    # Add sun light (main directional light)
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.object
    sun.name = "MainLight"
    sun.data.energy = 1.5
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # Add fill light (ambient)
    bpy.ops.object.light_add(type='SUN', location=(-5, 5, 8))
    fill = bpy.context.object
    fill.name = "FillLight"
    fill.data.energy = 0.5
    fill.rotation_euler = (math.radians(120), 0, math.radians(-45))
    
    # Set world background to dark (cave atmosphere)
    world = bpy.context.scene.world
    if not world.use_nodes:
        world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.08, 1.0)

def render_tile(output_name):
    """Render current scene to file"""
    output_path = os.path.join(OUTPUT_DIR, f"{output_name}.png")
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {output_path}")

def main():
    """Main function to generate all tiles"""
    print("Starting isometric tile generation...")
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Setup scene
    scene = setup_scene()
    camera = create_isometric_camera()
    create_lighting()
    
    # Render floor tile
    print("Creating floor tile...")
    floor = create_floor_tile()
    render_tile("cave_floor_iso")
    floor.select_set(True)
    bpy.ops.object.delete()
    
    # Render wall tile
    print("Creating wall tile...")
    wall = create_wall_tile()
    render_tile("cave_wall_iso")
    wall.select_set(True)
    bpy.ops.object.delete()
    
    print("Isometric tile generation complete!")
    print(f"Tiles saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

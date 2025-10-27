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

# Configuration - use portable relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
TILE_SIZE = 64  # Base width in pixels
TILE_HEIGHT_RATIO = 0.5  # Height is 0.5 of width (64x32)
ISO_ANGLE = math.atan(0.5)  # 26.565 degrees
RENDER_RESOLUTION = 128  # Higher res for better quality, will scale down
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'assets', 'tiles')

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
    
    # Apply material - MUCH BRIGHTER stone color
    stone_color = (0.6, 0.5, 0.4)  # Bright brown (was 0.25, 0.2, 0.15)
    mat = create_material("StoneMaterial", stone_color, roughness=0.7)
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

def create_floor_tile_variant(variant_name, color_variation=0.0):
    """Create floor tile with color variation"""
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = f"FloorTile_{variant_name}"
    
    # Vary the stone color
    base_color = (0.25 + color_variation, 0.2 + color_variation, 0.15 + color_variation)
    mat = create_material(f"Stone_{variant_name}", base_color, roughness=0.9)
    floor.data.materials.append(mat)
    
    # Add geometry detail
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=3)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return floor

def create_corner_wall_outer():
    """Create outer corner wall tile (L-shaped)"""
    # Create two wall segments meeting at 90 degrees
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -1, 0.5))
    wall1 = bpy.context.object
    wall1.scale = (1, 0.1, 0.5)
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=(1, 0, 0.5))
    wall2 = bpy.context.object
    wall2.scale = (0.1, 1, 0.5)
    
    # Join them
    wall1.select_set(True)
    wall2.select_set(True)
    bpy.context.view_layer.objects.active = wall1
    bpy.ops.object.join()
    
    corner = bpy.context.object
    corner.name = "CornerWallOuter"
    
    wall_color = (0.3, 0.25, 0.2)
    mat = create_material("WallCornerMaterial", wall_color, roughness=0.85)
    corner.data.materials.append(mat)
    
    return corner

def create_corner_wall_inner():
    """Create inner corner wall tile (concave corner)"""
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5))
    corner = bpy.context.object
    corner.name = "CornerWallInner"
    corner.scale = (1, 1, 0.5)
    
    # Cut out the inner corner
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    wall_color = (0.3, 0.25, 0.2)
    mat = create_material("WallCornerInnerMaterial", wall_color, roughness=0.85)
    corner.data.materials.append(mat)
    
    return corner

def create_stalactite():
    """Create hanging stalactite prop"""
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.3, radius2=0.05, depth=1.5, location=(0, 0, 1.5))
    stalactite = bpy.context.object
    stalactite.name = "Stalactite"
    stalactite.rotation_euler = (math.radians(180), 0, 0)  # Point down
    
    # Dark gray stone
    stone_color = (0.15, 0.15, 0.18)
    mat = create_material("StalactiteMaterial", stone_color, roughness=0.7)
    stalactite.data.materials.append(mat)
    
    return stalactite

def create_stalagmite():
    """Create floor stalagmite prop"""
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.4, radius2=0.05, depth=1.2, location=(0, 0, 0.6))
    stalagmite = bpy.context.object
    stalagmite.name = "Stalagmite"
    
    # Dark gray stone
    stone_color = (0.15, 0.15, 0.18)
    mat = create_material("StalagmiteMaterial", stone_color, roughness=0.7)
    stalagmite.data.materials.append(mat)
    
    return stalagmite

def create_rock_small():
    """Create small rock obstacle"""
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.5, location=(0, 0, 0.25))
    rock = bpy.context.object
    rock.name = "RockSmall"
    rock.scale = (1, 0.8, 0.6)  # Irregular shape
    
    # Gray-brown rock
    rock_color = (0.35, 0.3, 0.25)
    mat = create_material("RockMaterial", rock_color, roughness=0.95)
    rock.data.materials.append(mat)
    
    return rock

def create_rock_large():
    """Create large rock obstacle"""
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.8, location=(0, 0, 0.4))
    rock = bpy.context.object
    rock.name = "RockLarge"
    rock.scale = (1.2, 1, 0.7)  # Irregular shape
    
    # Gray-brown rock
    rock_color = (0.35, 0.3, 0.25)
    mat = create_material("RockLargeMaterial", rock_color, roughness=0.95)
    rock.data.materials.append(mat)
    
    return rock

def create_crystal():
    """Create glowing crystal prop"""
    # Create crystal shape (elongated diamond)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.2, radius2=0, depth=0.8, location=(0, 0, 0.4))
    crystal = bpy.context.object
    crystal.name = "Crystal"
    
    # Cyan glowing material
    crystal_color = (0.3, 0.6, 0.8)
    mat = create_material("CrystalMaterial", crystal_color, roughness=0.1)
    
    # Add emission for glow
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Emission Color'].default_value = (0.4, 0.8, 1.0, 1.0)
        bsdf.inputs['Emission Strength'].default_value = 2.0
    
    crystal.data.materials.append(mat)
    
    return crystal

def create_lighting():
    """Set up lighting for cave atmosphere"""
    # Remove default light
    if "Light" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)
    
    # Add sun light (main directional light) - MUCH BRIGHTER
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.object
    sun.name = "MainLight"
    sun.data.energy = 3.0  # Doubled from 1.5
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # Add fill light (ambient) - BRIGHTER
    bpy.ops.object.light_add(type='SUN', location=(-5, 5, 8))
    fill = bpy.context.object
    fill.name = "FillLight"
    fill.data.energy = 2.0  # Quadrupled from 0.5
    fill.rotation_euler = (math.radians(120), 0, math.radians(-45))
    
    # Set world background to LIGHTER (was very dark)
    world = bpy.context.scene.world
    if not world.use_nodes:
        world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.3, 0.3, 0.35, 1.0)  # Much lighter!

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
    
    # === FLOOR TILES ===
    print("Creating floor tiles...")
    floor = create_floor_tile()
    render_tile("cave_floor_iso")
    floor.select_set(True)
    bpy.ops.object.delete()
    
    # Floor variations
    floor_dark = create_floor_tile_variant("dark", -0.05)
    render_tile("cave_floor_dark")
    floor_dark.select_set(True)
    bpy.ops.object.delete()
    
    floor_light = create_floor_tile_variant("light", 0.05)
    render_tile("cave_floor_light")
    floor_light.select_set(True)
    bpy.ops.object.delete()
    
    # === WALL TILES ===
    print("Creating wall tiles...")
    wall = create_wall_tile()
    render_tile("cave_wall_iso")
    wall.select_set(True)
    bpy.ops.object.delete()
    
    # Corner walls
    print("Creating corner tiles...")
    corner_out = create_corner_wall_outer()
    render_tile("cave_wall_corner_outer")
    corner_out.select_set(True)
    bpy.ops.object.delete()
    
    corner_in = create_corner_wall_inner()
    render_tile("cave_wall_corner_inner")
    corner_in.select_set(True)
    bpy.ops.object.delete()
    
    # === PROPS ===
    print("Creating props...")
    
    # Stalactite (hanging)
    stalactite = create_stalactite()
    render_tile("prop_stalactite")
    stalactite.select_set(True)
    bpy.ops.object.delete()
    
    # Stalagmite (floor)
    stalagmite = create_stalagmite()
    render_tile("prop_stalagmite")
    stalagmite.select_set(True)
    bpy.ops.object.delete()
    
    # Rocks
    rock_sm = create_rock_small()
    render_tile("prop_rock_small")
    rock_sm.select_set(True)
    bpy.ops.object.delete()
    
    rock_lg = create_rock_large()
    render_tile("prop_rock_large")
    rock_lg.select_set(True)
    bpy.ops.object.delete()
    
    # Crystal
    crystal = create_crystal()
    render_tile("prop_crystal")
    crystal.select_set(True)
    bpy.ops.object.delete()
    
    print("\n" + "="*50)
    print("Isometric tile generation complete!")
    print(f"Generated 12 tiles total:")
    print("  - 3 floor variations")
    print("  - 3 wall types (straight + corners)")
    print("  - 6 props (stalactite, stalagmite, rocks, crystal)")
    print(f"Tiles saved to: {OUTPUT_DIR}")
    print("="*50)

if __name__ == "__main__":
    main()

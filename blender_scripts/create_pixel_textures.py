import bpy
import os
import math

# Configuration - use portable relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'assets', 'textures')
TILE_SIZE = 64  # SNES-style higher resolution
RENDER_SIZE = 128  # Render at 2x for better quality

# SNES-style color palette (more colors, better gradients)
PALETTE = {
    # Cave floors - darker, more subtle with more variation
    'stone_dark': (0.18, 0.16, 0.14, 1.0),
    'stone_med': (0.24, 0.22, 0.19, 1.0),
    'stone_light': (0.30, 0.28, 0.24, 1.0),
    'stone_lighter': (0.36, 0.33, 0.29, 1.0),
    'stone_pale': (0.42, 0.38, 0.32, 1.0),  # NEW - lighter highlights
    
    # Pebbles and debris
    'pebble_dark': (0.20, 0.18, 0.16, 1.0),  # NEW
    'pebble_light': (0.32, 0.30, 0.26, 1.0),  # NEW
    'dirt': (0.22, 0.18, 0.14, 1.0),  # NEW - earthy tone
    
    # Water - more blue tones
    'water_dark': (0.08, 0.15, 0.22, 1.0),
    'water_med': (0.12, 0.22, 0.32, 1.0),
    'water_light': (0.18, 0.30, 0.42, 1.0),
    
    # Fire/lava
    'lava_dark': (0.40, 0.10, 0.05, 1.0),
    'lava_med': (0.85, 0.25, 0.15, 1.0),
    'lava_bright': (0.95, 0.50, 0.20, 1.0),
    'fire_yellow': (0.98, 0.85, 0.30, 1.0),
    
    # Moss/nature
    'moss_dark': (0.15, 0.25, 0.15, 1.0),
    'moss_med': (0.22, 0.35, 0.22, 1.0),
    'moss_light': (0.28, 0.45, 0.28, 1.0),
    
    # Crystal/magic
    'crystal_blue': (0.40, 0.60, 0.85, 1.0),
    'crystal_blue_bright': (0.60, 0.80, 0.95, 1.0),
    'crystal_purple': (0.55, 0.35, 0.75, 1.0),
    'crystal_purple_bright': (0.70, 0.50, 0.90, 1.0),
    'crystal_green': (0.30, 0.70, 0.45, 1.0),
    'crystal_red': (0.75, 0.25, 0.35, 1.0),
    
    # Metal/treasure
    'gold_dark': (0.65, 0.50, 0.20, 1.0),
    'gold': (0.85, 0.70, 0.30, 1.0),
    'gold_bright': (0.95, 0.85, 0.50, 1.0),
    'silver': (0.70, 0.70, 0.75, 1.0),
    'bronze': (0.60, 0.40, 0.25, 1.0),
    
    # Wood
    'wood_dark': (0.20, 0.12, 0.08, 1.0),
    'wood_med': (0.35, 0.22, 0.15, 1.0),
    'wood_light': (0.45, 0.30, 0.20, 1.0),
}

def setup_scene():
    """Clear scene and setup for pixel art rendering"""
    # Delete all existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Setup render settings for pixel art
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT'  # Blender 4.5+
    scene.render.resolution_x = RENDER_SIZE
    scene.render.resolution_y = RENDER_SIZE
    scene.render.film_transparent = True
    
    # Pixel-perfect settings (skip EEVEE-specific settings for compatibility)
    scene.render.filter_size = 0.01  # Sharp pixels
    
    # Create camera (top-down orthographic for tiles)
    bpy.ops.object.camera_add(location=(0, 0, 5))
    camera = bpy.context.object
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 2.0
    camera.rotation_euler = (0, 0, 0)
    scene.camera = camera
    
    # Simple flat lighting for pixel art look
    bpy.ops.object.light_add(type='SUN', location=(2, 2, 5))
    sun = bpy.context.object
    sun.data.energy = 2.0
    sun.rotation_euler = (math.radians(45), math.radians(45), 0)

def create_material(name, base_color, emission=0.0):
    """Create a simple flat material for pixel art"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Simple emission + diffuse for flat look
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    if emission > 0:
        emit = nodes.new('ShaderNodeEmission')
        emit.inputs[0].default_value = base_color
        emit.inputs[1].default_value = emission
        mat.node_tree.links.new(emit.outputs[0], output.inputs[0])
    else:
        diffuse = nodes.new('ShaderNodeBsdfDiffuse')
        diffuse.inputs[0].default_value = base_color
        mat.node_tree.links.new(diffuse.outputs[0], output.inputs[0])
    
    return mat

def create_smooth_material(name, color1, color2, color3, noise_scale=4.0):
    """Create a smooth blended material with subtle noise for organic look"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)
    
    diffuse = nodes.new('ShaderNodeBsdfDiffuse')
    diffuse.location = (600, 0)
    
    # Color ramp for gradient
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (400, 0)
    color_ramp.color_ramp.elements[0].color = color1
    color_ramp.color_ramp.elements[1].color = color2
    # Add third color
    color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[1].color = color3
    
    # Noise texture for variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (200, 0)
    noise.inputs['Scale'].default_value = noise_scale
    noise.inputs['Detail'].default_value = 4.0
    noise.inputs['Roughness'].default_value = 0.6
    
    mat.node_tree.links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    mat.node_tree.links.new(color_ramp.outputs['Color'], diffuse.inputs[0])
    mat.node_tree.links.new(diffuse.outputs[0], output.inputs[0])
    
    return mat

def create_detailed_floor_material(name, base_colors, detail_colors, crack_color):
    """Create detailed floor with gradients, depressions, and scattered details"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1200, 0)
    
    diffuse = nodes.new('ShaderNodeBsdfDiffuse')
    diffuse.location = (1000, 0)
    
    # Mix final colors
    color_mix = nodes.new('ShaderNodeMix')
    color_mix.data_type = 'RGBA'
    color_mix.location = (800, 0)
    
    # Base gradient (main floor texture)
    base_ramp = nodes.new('ShaderNodeValToRGB')
    base_ramp.location = (400, 100)
    base_ramp.color_ramp.elements[0].color = base_colors[0]
    base_ramp.color_ramp.elements[1].color = base_colors[1]
    base_ramp.color_ramp.elements.new(0.5)
    base_ramp.color_ramp.elements[1].color = base_colors[2]
    
    # Detail noise (cracks, pebbles, depressions)
    detail_ramp = nodes.new('ShaderNodeValToRGB')
    detail_ramp.location = (400, -100)
    detail_ramp.color_ramp.elements[0].color = detail_colors[0]
    detail_ramp.color_ramp.elements[1].color = detail_colors[1]
    # Add dark cracks
    detail_ramp.color_ramp.elements.new(0.15)
    detail_ramp.color_ramp.elements[0].color = crack_color
    
    # Base noise (large gradients for depressions)
    base_noise = nodes.new('ShaderNodeTexNoise')
    base_noise.location = (200, 100)
    base_noise.inputs['Scale'].default_value = 3.0  # Large features
    base_noise.inputs['Detail'].default_value = 6.0
    base_noise.inputs['Roughness'].default_value = 0.7
    
    # Detail noise (small features: pebbles, cracks, litter)
    detail_noise = nodes.new('ShaderNodeTexNoise')
    detail_noise.location = (200, -100)
    detail_noise.inputs['Scale'].default_value = 20.0  # Small features
    detail_noise.inputs['Detail'].default_value = 8.0
    detail_noise.inputs['Roughness'].default_value = 0.5
    
    # Voronoi for depression patterns
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (0, 0)
    voronoi.voronoi_dimensions = '2D'
    voronoi.inputs['Scale'].default_value = 5.0
    
    # Mix voronoi with base noise for depression gradients
    voronoi_mix = nodes.new('ShaderNodeMix')
    voronoi_mix.data_type = 'FLOAT'
    voronoi_mix.location = (200, 0)
    voronoi_mix.inputs['Factor'].default_value = 0.3
    
    # Connect nodes
    mat.node_tree.links.new(voronoi.outputs['Distance'], voronoi_mix.inputs[6])  # A
    mat.node_tree.links.new(base_noise.outputs['Fac'], voronoi_mix.inputs[7])  # B
    mat.node_tree.links.new(voronoi_mix.outputs[2], base_ramp.inputs['Fac'])  # Result to base
    
    mat.node_tree.links.new(detail_noise.outputs['Fac'], detail_ramp.inputs['Fac'])
    
    mat.node_tree.links.new(base_ramp.outputs['Color'], color_mix.inputs[6])  # A
    mat.node_tree.links.new(detail_ramp.outputs['Color'], color_mix.inputs[7])  # B
    mat.node_tree.links.new(detail_noise.outputs['Fac'], color_mix.inputs['Factor'])  # Mix with detail noise
    
    mat.node_tree.links.new(color_mix.outputs[2], diffuse.inputs[0])
    mat.node_tree.links.new(diffuse.outputs[0], output.inputs[0])
    
    return mat

def create_cave_floor():
    """Cave floor tile - natural with depressions, gradients, and scattered details"""
    bpy.ops.mesh.primitive_plane_add(size=1.9)
    plane = bpy.context.object
    
    mat = create_detailed_floor_material('cave_floor',
                                          base_colors=[PALETTE['stone_dark'], PALETTE['stone_med'], PALETTE['stone_light']],
                                          detail_colors=[PALETTE['stone_med'], PALETTE['stone_lighter']],
                                          crack_color=(0.10, 0.09, 0.08, 1.0))  # Dark cracks
    plane.data.materials.append(mat)
    
    render_texture('cave_floor_tile')
    bpy.ops.object.delete()

def create_cave_floor_moss():
    """Mossy cave floor - natural gradients with moss patches and pebbles"""
    bpy.ops.mesh.primitive_plane_add(size=1.9)
    plane = bpy.context.object
    
    mat = create_detailed_floor_material('cave_floor_moss',
                                          base_colors=[PALETTE['stone_dark'], PALETTE['moss_dark'], PALETTE['moss_med']],
                                          detail_colors=[PALETTE['moss_med'], PALETTE['moss_light']],
                                          crack_color=(0.12, 0.15, 0.12, 1.0))  # Dark moss cracks
    plane.data.materials.append(mat)
    
    render_texture('cave_floor_moss')
    bpy.ops.object.delete()

def create_cave_floor_wet():
    """Wet cave floor - depressions filled with water, darker gradients"""
    bpy.ops.mesh.primitive_plane_add(size=1.9)
    plane = bpy.context.object
    
    mat = create_detailed_floor_material('cave_floor_wet',
                                          base_colors=[PALETTE['stone_dark'], PALETTE['water_dark'], PALETTE['stone_med']],
                                          detail_colors=[PALETTE['water_dark'], PALETTE['water_med']],
                                          crack_color=(0.05, 0.10, 0.15, 1.0))  # Dark water-filled cracks
    plane.data.materials.append(mat)
    
    render_texture('cave_floor_wet')
    bpy.ops.object.delete()

def create_water_tile():
    """Animated-looking water tile"""
    bpy.ops.mesh.primitive_plane_add(size=1.9)
    plane = bpy.context.object
    
    mat = create_smooth_material('water', 
                                  PALETTE['water_dark'], 
                                  PALETTE['water_med'],
                                  PALETTE['water_light'],
                                  noise_scale=5.0)
    plane.data.materials.append(mat)
    
    render_texture('water_tile')
    bpy.ops.object.delete()

def create_lava_tile():
    """Glowing lava tile with gradient"""
    bpy.ops.mesh.primitive_plane_add(size=1.9)
    plane = bpy.context.object
    
    mat = bpy.data.materials.new(name='lava')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)
    
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (400, 0)
    emission.inputs[1].default_value = 2.0  # Emission strength
    
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (200, 0)
    color_ramp.color_ramp.elements[0].color = PALETTE['lava_dark']
    color_ramp.color_ramp.elements[1].color = PALETTE['lava_bright']
    color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[1].color = PALETTE['lava_med']
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, 0)
    noise.inputs['Scale'].default_value = 6.0
    
    mat.node_tree.links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    mat.node_tree.links.new(color_ramp.outputs['Color'], emission.inputs[0])
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    
    plane.data.materials.append(mat)
    
    render_texture('lava_tile')
    bpy.ops.object.delete()

def create_campfire():
    """Campfire - realistic proportions (small, about 2 feet wide)"""
    # Fire base - more detailed
    bpy.ops.mesh.primitive_cube_add(size=0.4, location=(0, 0, 0.2))
    fire = bpy.context.object
    fire.scale[2] = 1.2
    mat_fire = create_material('fire', PALETTE['fire_yellow'], emission=5.0)
    fire.data.materials.append(mat_fire)
    
    # Wood logs - crossed pattern
    for i, rot in enumerate([0, 90]):
        bpy.ops.mesh.primitive_cube_add(size=0.08, location=(0, 0, 0.06))
        log = bpy.context.object
        log.scale[0] = 3.0
        log.rotation_euler = (0, 0, math.radians(rot))
        mat_wood = create_material('wood', PALETTE['wood_med'])
        log.data.materials.append(mat_wood)
    
    # Rocks around fire
    for i in range(6):
        angle = i * math.pi / 3
        x = math.cos(angle) * 0.25
        y = math.sin(angle) * 0.25
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.06, location=(x, y, 0.03))
        rock = bpy.context.object
        mat_rock = create_material(f'rock_{i}', PALETTE['stone_light'])
        rock.data.materials.append(mat_rock)
    
    render_texture('campfire')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_crystal():
    """Large glowing crystal cluster - about 3 feet tall"""
    # Blue variant
    # Main crystal
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.15, depth=0.8, location=(0, 0, 0.4))
    crystal = bpy.context.object
    crystal.rotation_euler = (math.radians(10), 0, math.radians(25))
    mat = create_material('crystal', PALETTE['crystal_blue_bright'], emission=3.0)
    crystal.data.materials.append(mat)
    
    # Smaller crystals around it
    for i in range(3):
        angle = i * math.pi * 2 / 3
        x = math.cos(angle) * 0.12
        y = math.sin(angle) * 0.12
        size = 0.3 + (i * 0.1)
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.08, depth=size, location=(x, y, size/2))
        small_crystal = bpy.context.object
        small_crystal.rotation_euler = (math.radians(15), 0, angle)
        small_crystal.data.materials.append(mat)
    
    render_texture('crystal_blue')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_crystal_purple():
    """Purple crystal variant"""
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.15, depth=0.8, location=(0, 0, 0.4))
    crystal = bpy.context.object
    crystal.rotation_euler = (math.radians(10), 0, math.radians(25))
    mat = create_material('crystal_purple', PALETTE['crystal_purple_bright'], emission=3.0)
    crystal.data.materials.append(mat)
    
    for i in range(3):
        angle = i * math.pi * 2 / 3
        x = math.cos(angle) * 0.12
        y = math.sin(angle) * 0.12
        size = 0.3 + (i * 0.1)
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.08, depth=size, location=(x, y, size/2))
        small_crystal = bpy.context.object
        small_crystal.rotation_euler = (math.radians(15), 0, angle)
        small_crystal.data.materials.append(mat)
    
    render_texture('crystal_purple')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_crystal_green():
    """Green crystal variant"""
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.15, depth=0.8, location=(0, 0, 0.4))
    crystal = bpy.context.object
    crystal.rotation_euler = (math.radians(10), 0, math.radians(25))
    mat = create_material('crystal_green', PALETTE['crystal_green'], emission=3.0)
    crystal.data.materials.append(mat)
    
    for i in range(3):
        angle = i * math.pi * 2 / 3
        x = math.cos(angle) * 0.12
        y = math.sin(angle) * 0.12
        size = 0.3 + (i * 0.1)
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.08, depth=size, location=(x, y, size/2))
        small_crystal = bpy.context.object
        small_crystal.rotation_euler = (math.radians(15), 0, angle)
        small_crystal.data.materials.append(mat)
    
    render_texture('crystal_green')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_treasure_chest():
    """Simple treasure chest"""
    # Bottom
    bpy.ops.mesh.primitive_cube_add(size=0.4, location=(0, 0, 0.15))
    bottom = bpy.context.object
    bottom.scale[2] = 0.5
    mat_wood = create_material('chest_wood', (0.4, 0.25, 0.15, 1.0))
    bottom.data.materials.append(mat_wood)
    
    # Lid
    bpy.ops.mesh.primitive_cube_add(size=0.4, location=(0, 0, 0.35))
    lid = bpy.context.object
    lid.scale[2] = 0.3
    mat_gold = create_material('chest_gold', PALETTE['gold'], emission=0.5)
    lid.data.materials.append(mat_gold)
    
    render_texture('treasure_chest')
    bpy.ops.object.delete()
    bpy.ops.object.delete()

def create_rock_pile():
    """Small rock pile"""
    for i in range(3):
        size = 0.3 - i * 0.08
        z = i * 0.15
        x = (i - 1) * 0.1
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=size, location=(x, 0, z))
        rock = bpy.context.object
        mat = create_material(f'rock_{i}', PALETTE['stone_light'])
        rock.data.materials.append(mat)
    
    render_texture('rock_pile')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_mushrooms():
    """Glowing mushrooms"""
    for i in range(3):
        # Stem
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.15, location=(i*0.2-0.2, 0, 0.075))
        stem = bpy.context.object
        mat_stem = create_material(f'stem_{i}', (0.9, 0.85, 0.7, 1.0))
        stem.data.materials.append(mat_stem)
        
        # Cap
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(i*0.2-0.2, 0, 0.18))
        cap = bpy.context.object
        cap.scale[2] = 0.5
        mat_cap = create_material(f'cap_{i}', PALETTE['moss_light'], emission=1.0)
        cap.data.materials.append(mat_cap)
    
    render_texture('mushrooms')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_stalagmite():
    """Cave stalagmite"""
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.25, depth=0.8, location=(0, 0, 0.4))
    stala = bpy.context.object
    
    mat = create_material('stalagmite', PALETTE['stone_light'])
    stala.data.materials.append(mat)
    
    render_texture('stalagmite')
    bpy.ops.object.delete()

def create_stalactite():
    """Cave stalactite (hanging)"""
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.25, depth=0.8, location=(0, 0, 0))
    stalac = bpy.context.object
    stalac.rotation_euler = (math.radians(180), 0, 0)
    
    mat = create_material('stalactite', PALETTE['stone_med'])
    stalac.data.materials.append(mat)
    
    render_texture('stalactite')
    bpy.ops.object.delete()

def create_bones():
    """Skeleton bones"""
    # Skull
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(0, 0, 0.1))
    skull = bpy.context.object
    skull.scale[2] = 1.2
    mat_bone = create_material('bone', (0.95, 0.92, 0.85, 1.0))
    skull.data.materials.append(mat_bone)
    
    # Bones
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.2, location=(0.15, 0, 0.05))
    bone1 = bpy.context.object
    bone1.rotation_euler = (0, math.radians(90), 0)
    bone1.data.materials.append(mat_bone)
    
    render_texture('bones')
    bpy.ops.object.delete()
    bpy.ops.object.delete()

def create_torch():
    """Wall torch"""
    # Handle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.5, location=(0, 0, 0.25))
    handle = bpy.context.object
    mat_wood = create_material('torch_wood', (0.3, 0.2, 0.1, 1.0))
    handle.data.materials.append(mat_wood)
    
    # Flame
    bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.2, location=(0, 0, 0.55))
    flame = bpy.context.object
    mat_fire = create_material('torch_fire', PALETTE['fire_yellow'], emission=5.0)
    flame.data.materials.append(mat_fire)
    
    render_texture('torch')
    bpy.ops.object.delete()
    bpy.ops.object.delete()

def render_texture(name):
    """Render current scene to texture file"""
    filepath = os.path.join(OUTPUT_DIR, f"{name}.png")
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {name}.png")

def main():
    """Generate all pixel art textures"""
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Generating NES/Gameboy style pixel art textures...")
    
    # Floor tiles
    setup_scene()
    create_cave_floor()
    
    setup_scene()
    create_cave_floor_moss()
    
    setup_scene()
    create_water_tile()
    
    setup_scene()
    create_lava_tile()
    
    # Props and features
    setup_scene()
    create_campfire()
    
    setup_scene()
    create_crystal()
    
    setup_scene()
    create_crystal_purple()
    
    setup_scene()
    create_crystal_green()
    
    setup_scene()
    create_treasure_chest()
    
    setup_scene()
    create_rock_pile()
    
    setup_scene()
    create_mushrooms()
    
    setup_scene()
    create_stalagmite()
    
    setup_scene()
    create_stalactite()
    
    setup_scene()
    create_bones()
    
    setup_scene()
    create_torch()
    
    # Additional floor variations
    setup_scene()
    create_cave_floor_wet()
    
    print(f"\nAll textures generated in: {OUTPUT_DIR}")
    print("Total textures: 16")

if __name__ == "__main__":
    main()

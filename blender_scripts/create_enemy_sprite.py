"""
Generic Enemy Sprite Generator
Creates animated enemy sprites with walk, attack, and death animations.
Outputs sprite sheets for use in Godot.

Usage: Run via run_blender.ps1 create_enemy_sprite.py --enemy-name <name>
"""

import bpy
import math
import os
import sys
from mathutils import Vector

# Parse command line arguments
def get_arg(name, default=None):
    """Get command line argument value"""
    args = sys.argv
    if "--" in args:
        args = args[args.index("--") + 1:]
    
    for i, arg in enumerate(args):
        if arg == name and i + 1 < len(args):
            return args[i + 1]
    return default

# Enemy configuration
ENEMY_NAME = get_arg("--enemy-name", "slime")
BODY_COLOR = tuple(map(float, get_arg("--body-color", "0.2,0.8,0.3,1.0").split(",")))
EYE_COLOR = tuple(map(float, get_arg("--eye-color", "1.0,1.0,1.0,1.0").split(",")))
SIZE = float(get_arg("--size", "1.0"))
OUTPUT_DIR = get_arg("--output-dir", "C:/Users/Ben/code/cave-crawler/assets/enemies")

# Animation settings
SPRITE_SIZE = 64
FRAMES_PER_ANIMATION = {
    "idle": 4,
    "walk": 8,
    "attack": 6,
    "death": 8
}

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def setup_scene():
    """Setup camera, lighting, and render settings"""
    # Add camera
    bpy.ops.object.camera_add(location=(0, -5, 3))
    camera = bpy.context.object
    camera.rotation_euler = (math.radians(60), 0, 0)
    bpy.context.scene.camera = camera
    
    # Add sun light
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.object
    sun.data.energy = 2.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # Add fill light
    bpy.ops.object.light_add(type='AREA', location=(-3, -3, 5))
    fill = bpy.context.object
    fill.data.energy = 0.5
    
    # Setup render settings
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.render.resolution_x = SPRITE_SIZE
    scene.render.resolution_y = SPRITE_SIZE
    scene.render.film_transparent = True
    
    # Setup world
    if not scene.world:
        scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (0, 0, 0, 0)  # Transparent

def create_enemy_body():
    """Create the enemy body (generic blob/slime shape)"""
    # Create main body sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=SIZE, location=(0, 0, SIZE * 0.5))
    body = bpy.context.object
    body.name = f"{ENEMY_NAME}_body"
    
    # Scale to make it blob-like (squash vertically)
    body.scale = (1.0, 1.0, 0.7)
    bpy.ops.object.transform_apply(scale=True)
    
    # Add subdivision and smooth
    bpy.ops.object.modifier_add(type='SUBSURF')
    body.modifiers["Subdivision"].levels = 2
    bpy.ops.object.shade_smooth()
    
    # Create material
    mat = bpy.data.materials.new(name=f"{ENEMY_NAME}_material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Add Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = BODY_COLOR
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.3
    
    # Add output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    if body.data.materials:
        body.data.materials[0] = mat
    else:
        body.data.materials.append(mat)
    
    return body

def create_eyes(body):
    """Create enemy eyes"""
    eyes = []
    
    for i, x_offset in enumerate([-0.3, 0.3]):
        # Create eye sphere
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=SIZE * 0.15,
            location=(x_offset * SIZE, SIZE * 0.4, SIZE * 0.8)
        )
        eye = bpy.context.object
        eye.name = f"{ENEMY_NAME}_eye_{i}"
        
        # Create eye material
        mat = bpy.data.materials.new(name=f"{ENEMY_NAME}_eye_material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes['Principled BSDF']
        bsdf.inputs['Base Color'].default_value = EYE_COLOR
        bsdf.inputs['Emission Strength'].default_value = 0.5
        
        # Assign material
        if eye.data.materials:
            eye.data.materials[0] = mat
        else:
            eye.data.materials.append(mat)
        
        # Parent to body
        eye.parent = body
        eyes.append(eye)
    
    return eyes

def animate_idle(body, eyes, start_frame, end_frame):
    """Create idle animation - gentle breathing/bobbing"""
    mid_frame = (start_frame + end_frame) // 2
    
    # Body bobbing
    body.location = (0, 0, 0)
    body.keyframe_insert(data_path="location", frame=start_frame)
    
    body.location = (0, 0, SIZE * 0.1)
    body.keyframe_insert(data_path="location", frame=mid_frame)
    
    body.location = (0, 0, 0)
    body.keyframe_insert(data_path="location", frame=end_frame)
    
    # Slight scale breathing
    body.scale = (1.0, 1.0, 1.0)
    body.keyframe_insert(data_path="scale", frame=start_frame)
    
    body.scale = (1.02, 1.02, 0.98)
    body.keyframe_insert(data_path="scale", frame=mid_frame)
    
    body.scale = (1.0, 1.0, 1.0)
    body.keyframe_insert(data_path="scale", frame=end_frame)

def animate_walk(body, eyes, start_frame, end_frame):
    """Create walk animation - bouncing movement"""
    frames = end_frame - start_frame
    step_frames = frames // 2
    
    for i in range(3):
        frame = start_frame + (i * step_frames // 2)
        if i % 2 == 0:
            # Down position (compressed)
            body.location = (0, 0, SIZE * -0.1)
            body.scale = (1.15, 1.15, 0.85)
        else:
            # Up position (stretched)
            body.location = (0, 0, SIZE * 0.2)
            body.scale = (0.95, 0.95, 1.05)
        
        body.keyframe_insert(data_path="location", frame=frame)
        body.keyframe_insert(data_path="scale", frame=frame)

def animate_attack(body, eyes, start_frame, end_frame):
    """Create attack animation - lunge forward"""
    frames = end_frame - start_frame
    
    # Wind up
    wind_frame = start_frame + frames // 3
    body.location = (0, SIZE * -0.3, SIZE * 0.1)
    body.scale = (0.85, 0.85, 1.15)
    body.keyframe_insert(data_path="location", frame=start_frame)
    body.keyframe_insert(data_path="scale", frame=start_frame)
    
    body.location = (0, SIZE * -0.5, SIZE * 0.2)
    body.scale = (0.8, 0.8, 1.2)
    body.keyframe_insert(data_path="location", frame=wind_frame)
    body.keyframe_insert(data_path="scale", frame=wind_frame)
    
    # Strike
    strike_frame = start_frame + 2 * frames // 3
    body.location = (0, SIZE * 0.6, SIZE * 0.1)
    body.scale = (1.2, 1.4, 0.8)
    body.keyframe_insert(data_path="location", frame=strike_frame)
    body.keyframe_insert(data_path="scale", frame=strike_frame)
    
    # Return
    body.location = (0, 0, 0)
    body.scale = (1.0, 1.0, 1.0)
    body.keyframe_insert(data_path="location", frame=end_frame)
    body.keyframe_insert(data_path="scale", frame=end_frame)

def animate_death(body, eyes, start_frame, end_frame):
    """Create death animation - collapse and fade"""
    frames = end_frame - start_frame
    
    # Start normal
    body.location = (0, 0, 0)
    body.scale = (1.0, 1.0, 1.0)
    body.keyframe_insert(data_path="location", frame=start_frame)
    body.keyframe_insert(data_path="scale", frame=start_frame)
    
    # Collapse
    mid_frame = start_frame + frames // 2
    body.location = (0, 0, SIZE * -0.3)
    body.scale = (1.4, 1.4, 0.3)
    body.keyframe_insert(data_path="location", frame=mid_frame)
    body.keyframe_insert(data_path="scale", frame=mid_frame)
    
    # Flatten completely
    body.location = (0, 0, SIZE * -0.5)
    body.scale = (1.6, 1.6, 0.1)
    body.keyframe_insert(data_path="location", frame=end_frame)
    body.keyframe_insert(data_path="scale", frame=end_frame)

def render_animation(animation_name, start_frame, end_frame):
    """Render animation frames to sprite sheet"""
    scene = bpy.context.scene
    output_path = os.path.join(OUTPUT_DIR, ENEMY_NAME, animation_name)
    os.makedirs(output_path, exist_ok=True)
    
    print(f"Rendering {animation_name} animation ({end_frame - start_frame + 1} frames)...")
    
    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        scene.render.filepath = os.path.join(output_path, f"frame_{frame - start_frame:04d}.png")
        bpy.ops.render.render(write_still=True)
    
    print(f"✓ {animation_name} complete")

def main():
    """Main generation function"""
    print(f"\n{'='*60}")
    print(f"Generating Enemy: {ENEMY_NAME}")
    print(f"Size: {SIZE}")
    print(f"Body Color: {BODY_COLOR}")
    print(f"Output: {OUTPUT_DIR}/{ENEMY_NAME}")
    print(f"{'='*60}\n")
    
    # Setup
    clear_scene()
    setup_scene()
    
    # Create enemy
    body = create_enemy_body()
    eyes = create_eyes(body)
    
    # Create animations
    current_frame = 1
    animations = []
    
    for anim_name, frame_count in FRAMES_PER_ANIMATION.items():
        start = current_frame
        end = current_frame + frame_count - 1
        
        print(f"Creating {anim_name} animation (frames {start}-{end})...")
        
        if anim_name == "idle":
            animate_idle(body, eyes, start, end)
        elif anim_name == "walk":
            animate_walk(body, eyes, start, end)
        elif anim_name == "attack":
            animate_attack(body, eyes, start, end)
        elif anim_name == "death":
            animate_death(body, eyes, start, end)
        
        animations.append((anim_name, start, end))
        current_frame = end + 1
    
    # Render all animations
    print("\nRendering animations...")
    for anim_name, start, end in animations:
        render_animation(anim_name, start, end)
    
    print(f"\n{'='*60}")
    print(f"✓ Enemy '{ENEMY_NAME}' generated successfully!")
    print(f"  Output: {OUTPUT_DIR}/{ENEMY_NAME}/")
    print(f"  Animations: {', '.join(FRAMES_PER_ANIMATION.keys())}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()

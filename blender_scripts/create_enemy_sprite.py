#!/usr/bin/env python3
"""
Enemy Sprite Generator for Godot
Generates animated 2D sprites from 3D Blender models
Creates puddle-style slime enemy with splash and dry-up animations
"""

import bpy
import math
import os
import sys
from mathutils import Vector

# Get the project root directory (2 levels up from blender_scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Parse command line arguments
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

# Default values
ENEMY_NAME = "slime"
BODY_COLOR = (0.2, 0.8, 0.3, 1.0)  # Green slime
EYE_COLOR = (1.0, 1.0, 1.0, 1.0)   # White eyes
SIZE = 1.0
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "assets", "enemies")

# Parse arguments
i = 0
while i < len(args):
    if args[i] == "--enemy-name" and i + 1 < len(args):
        ENEMY_NAME = args[i + 1]
        i += 2
    elif args[i] == "--body-color" and i + 1 < len(args):
        color_values = [float(x) for x in args[i + 1].split(',')]
        BODY_COLOR = tuple(color_values)
        i += 2
    elif args[i] == "--eye-color" and i + 1 < len(args):
        color_values = [float(x) for x in args[i + 1].split(',')]
        EYE_COLOR = tuple(color_values)
        i += 2
    elif args[i] == "--size" and i + 1 < len(args):
        SIZE = float(args[i + 1])
        i += 2
    elif args[i] == "--output-dir" and i + 1 < len(args):
        OUTPUT_DIR = args[i + 1]
        i += 2
    else:
        i += 1

# Constants
SPRITE_SIZE = 64
FPS = 24

print("\n" + "="*60)
print(f"Generating Enemy: {ENEMY_NAME}")
print(f"Size: {SIZE}")
print(f"Body Color: {BODY_COLOR}")
print(f"Output: {os.path.join(OUTPUT_DIR, ENEMY_NAME)}")
print("="*60 + "\n")

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def setup_camera():
    """Setup orthographic camera for sprite rendering"""
    bpy.ops.object.camera_add(location=(0, -8, 2))
    camera = bpy.context.object
    camera.rotation_euler = (math.radians(75), 0, 0)
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 3.5
    bpy.context.scene.camera = camera
    return camera

def setup_lighting():
    """Setup three-point lighting"""
    # Key light
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    key = bpy.context.object
    key.data.energy = 1.5
    key.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # Fill light
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

def create_puddle_body():
    """Create a puddle-style slime body"""
    # Create a flat cylinder for the puddle base
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=SIZE * 0.8,
        depth=SIZE * 0.15,
        location=(0, 0, SIZE * 0.08)
    )
    body = bpy.context.object
    body.name = f"{ENEMY_NAME}_body"
    
    # Switch to edit mode for deformation
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Add random deformation for organic puddle shape
    bpy.ops.transform.vertex_random(offset=0.2, uniform=0.15, seed=42)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Add subdivision for smooth organic shape
    subdiv = body.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 3
    subdiv.render_levels = 3
    
    # Smooth shading
    bpy.ops.object.shade_smooth()
    
    # Create glossy slime material with transparency
    mat = bpy.data.materials.new(name=f"{ENEMY_NAME}_material")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Principled BSDF for glossy slime
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = BODY_COLOR
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.15
    bsdf.inputs['Transmission Weight'].default_value = 0.6
    bsdf.inputs['IOR'].default_value = 1.33
    bsdf.inputs['Alpha'].default_value = 0.9
    bsdf.inputs['Sheen Weight'].default_value = 0.3
    
    # Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    body.data.materials.append(mat)
    
    return body

def create_eyes(body):
    """Create floating eyes in the puddle"""
    eyes = []
    
    for i, x_offset in enumerate([-0.25, 0.25]):
        # Create eye sphere
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=SIZE * 0.12,
            location=(x_offset * SIZE, 0, SIZE * 0.15)
        )
        eye = bpy.context.object
        eye.name = f"{ENEMY_NAME}_eye_{i}"
        bpy.ops.object.shade_smooth()
        
        # Create eye material with emission
        mat = bpy.data.materials.new(name=f"{ENEMY_NAME}_eye_material_{i}")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes['Principled BSDF']
        bsdf.inputs['Base Color'].default_value = EYE_COLOR
        bsdf.inputs['Emission Color'].default_value = EYE_COLOR
        bsdf.inputs['Emission Strength'].default_value = 0.8
        bsdf.inputs['Roughness'].default_value = 0.1
        
        eye.data.materials.append(mat)
        
        # Parent to body
        eye.parent = body
        eyes.append(eye)
    
    return eyes

def animate_idle(body, eyes, start_frame, end_frame):
    """Gentle breathing/bobbing animation"""
    scene = bpy.context.scene
    
    # Clear existing animation
    if body.animation_data:
        body.animation_data_clear()
    
    frames_per_cycle = end_frame - start_frame + 1
    
    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        t = (frame - start_frame) / frames_per_cycle
        
        # Gentle pulsing - expand and contract slightly
        pulse = 1.0 + math.sin(t * math.pi * 2) * 0.05
        body.scale = (pulse, pulse, 1.0 + math.sin(t * math.pi * 2) * 0.1)
        body.keyframe_insert(data_path="scale", frame=frame)
        
        # Eyes bob slightly
        for eye in eyes:
            bob = math.sin(t * math.pi * 2) * 0.03
            eye.location.z = SIZE * 0.15 + bob
            eye.keyframe_insert(data_path="location", frame=frame)

def animate_walk(body, eyes, start_frame, end_frame):
    """Sliding/oozing movement animation"""
    scene = bpy.context.scene
    
    frames_per_cycle = end_frame - start_frame + 1
    
    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        t = (frame - start_frame) / frames_per_cycle
        
        # Compress forward, stretch back (like oozing forward)
        compress_x = 1.0 + math.sin(t * math.pi * 4) * 0.15
        compress_z = 1.0 - math.sin(t * math.pi * 4) * 0.1
        body.scale = (compress_x, 0.95, compress_z)
        body.keyframe_insert(data_path="scale", frame=frame)
        
        # Ripple effect on edges
        body.rotation_euler.z = math.sin(t * math.pi * 4) * 0.05
        body.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        # Eyes move with the ooze
        for i, eye in enumerate(eyes):
            offset = i * math.pi  # Offset between eyes
            eye.location.z = SIZE * 0.15 + math.sin(t * math.pi * 4 + offset) * 0.05
            eye.keyframe_insert(data_path="location", frame=frame)

def animate_attack(body, eyes, start_frame, end_frame):
    """Splash attack animation - expand rapidly then return"""
    scene = bpy.context.scene
    
    frames_per_cycle = end_frame - start_frame + 1
    
    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        t = (frame - start_frame) / frames_per_cycle
        
        if t < 0.3:  # Wind up - compress
            scale = 1.0 - (t / 0.3) * 0.3
            height = 1.0 + (t / 0.3) * 0.4
            body.scale = (scale, scale, height)
        elif t < 0.5:  # Splash! - expand rapidly
            progress = (t - 0.3) / 0.2
            scale = 0.7 + progress * 0.9  # From 0.7 to 1.6
            height = 1.4 - progress * 0.8  # From 1.4 to 0.6 (flatten)
            body.scale = (scale, scale, height)
        else:  # Return to normal
            progress = (t - 0.5) / 0.5
            scale = 1.6 - progress * 0.6  # From 1.6 back to 1.0
            height = 0.6 + progress * 0.4  # From 0.6 back to 1.0
            body.scale = (scale, scale, height)
        
        body.keyframe_insert(data_path="scale", frame=frame)
        
        # Eyes move dramatically during splash
        for i, eye in enumerate(eyes):
            if t < 0.5:  # During splash
                eye.location.z = SIZE * 0.15 + (t / 0.5) * 0.2
            else:  # Return
                progress = (t - 0.5) / 0.5
                eye.location.z = SIZE * 0.35 - progress * 0.2
            eye.keyframe_insert(data_path="location", frame=frame)

def animate_death(body, eyes, start_frame, end_frame):
    """Dry up and disappear - puddle shrinks and fades"""
    scene = bpy.context.scene
    
    frames_per_cycle = end_frame - start_frame + 1
    
    # Animate material alpha for fade out
    mat = body.data.materials[0]
    alpha_node = mat.node_tree.nodes['Principled BSDF'].inputs['Alpha']
    
    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        t = (frame - start_frame) / frames_per_cycle
        
        # Puddle dries up - flattens and shrinks
        shrink = 1.0 - t * 0.95  # Shrink to almost nothing
        flatten = 1.0 - t * 0.9   # Flatten completely
        body.scale = (shrink, shrink, flatten * 0.2)
        body.keyframe_insert(data_path="scale", frame=frame)
        
        # Fade out transparency
        alpha = 0.9 - t * 0.9
        alpha_node.default_value = max(alpha, 0.0)
        alpha_node.keyframe_insert(data_path="default_value", frame=frame)
        
        # Eyes sink and fade
        for eye in eyes:
            eye.location.z = SIZE * 0.15 * (1.0 - t)
            eye.scale = Vector((1.0 - t * 0.5, 1.0 - t * 0.5, 1.0 - t * 0.5))
            eye.keyframe_insert(data_path="location", frame=frame)
            eye.keyframe_insert(data_path="scale", frame=frame)

def render_animation(animation_name, start_frame, end_frame, output_path):
    """Render animation frames to PNG sequence"""
    os.makedirs(output_path, exist_ok=True)
    
    scene = bpy.context.scene
    scene.frame_start = start_frame
    scene.frame_end = end_frame
    
    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        scene.render.filepath = os.path.join(output_path, f"frame_{frame - start_frame:04d}.png")
        bpy.ops.render.render(write_still=True)

# Main execution
def main():
    # Setup scene
    clear_scene()
    camera = setup_camera()
    setup_lighting()
    
    # Create enemy
    body = create_puddle_body()
    eyes = create_eyes(body)
    
    # Animation frame ranges
    idle_start = 1
    idle_end = 4
    walk_start = 5
    walk_end = 12
    attack_start = 13
    attack_end = 18
    death_start = 19
    death_end = 26
    
    print("Creating idle animation (frames 1-4)...")
    animate_idle(body, eyes, idle_start, idle_end)
    
    print("Creating walk animation (frames 5-12)...")
    animate_walk(body, eyes, walk_start, walk_end)
    
    print("Creating attack animation (frames 13-18)...")
    animate_attack(body, eyes, attack_start, attack_end)
    
    print("Creating death animation (frames 19-26)...")
    animate_death(body, eyes, death_start, death_end)
    
    # Render animations
    print("\nRendering animations...")
    base_output = os.path.join(OUTPUT_DIR, ENEMY_NAME)
    
    print(f"Rendering idle animation (4 frames)...")
    render_animation("idle", idle_start, idle_end, os.path.join(base_output, "idle"))
    
    print(f"Rendering walk animation (8 frames)...")
    render_animation("walk", walk_start, walk_end, os.path.join(base_output, "walk"))
    
    print(f"Rendering attack animation (6 frames)...")
    render_animation("attack", attack_start, attack_end, os.path.join(base_output, "attack"))
    
    print(f"Rendering death animation (8 frames)...")
    render_animation("death", death_start, death_end, os.path.join(base_output, "death"))
    
    print("\n" + "="*60)
    print(f"Enemy '{ENEMY_NAME}' generation complete!")
    print(f"Output location: {base_output}")
    print("="*60)

if __name__ == "__main__":
    main()

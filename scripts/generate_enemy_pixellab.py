"""
PixelLab API Integration for Enemy Sprite Generation
Generates animated sprite sequences using PixelLab AI
"""

import os
import sys
import json
import time
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

try:
    from pixellab_config import (
        PIXELLAB_API_KEY,
        DEFAULT_SIZE,
        DEFAULT_FRAMES
    )
except ImportError:
    print("Error: pixellab_config.py not found!")
    print("Please create scripts/pixellab_config.py with your API key")
    sys.exit(1)

try:
    import pixellab
except ImportError:
    print("Error: pixellab library not installed!")
    print("Please run: pip install pixellab")
    sys.exit(1)


class PixelLabGenerator:
    """Generate enemy sprites using PixelLab API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or PIXELLAB_API_KEY
        if self.api_key == "your_api_key_here":
            raise ValueError("Please set your PixelLab API key in pixellab_config.py")
        
        self.client = pixellab.Client(secret=self.api_key)
    
    def generate_sprite_frame(self, prompt, size=64, reference_image=None):
        """
        Generate a single sprite frame
        If reference_image is provided, use BitForge for style consistency.
        Args:
            prompt: Description of the sprite
            size: Size of sprite in pixels (default 64x64)
            reference_image: PIL Image or PixelLab Base64Image for style transfer
        Returns:
            Image data or None if failed
        """
        try:
            if reference_image is None:
                # First frame: use PixFlux
                result = self.client.generate_image_pixflux(
                    description=prompt,
                    image_size={"width": size, "height": size}
                )
                if hasattr(result, 'image'):
                    return result.image
                elif hasattr(result, 'output_image'):
                    return result.output_image
                else:
                    if isinstance(result, dict):
                        return result.get('image') or result.get('output_image')
                    return result
            else:
                # Subsequent frames: use BitForge with style_image for consistency
                from PIL import Image
                import io
                # If reference_image is PixelLab Base64Image, convert to PIL
                if hasattr(reference_image, 'base64'):
                    import base64
                    img_bytes = base64.b64decode(reference_image.base64)
                    style_pil = Image.open(io.BytesIO(img_bytes))
                elif isinstance(reference_image, Image.Image):
                    style_pil = reference_image
                else:
                    style_pil = reference_image
                result = self.client.generate_image_bitforge(
                    description=prompt,
                    image_size={"width": size, "height": size},
                    style_image=style_pil,
                    style_strength=40,
                    no_background=True
                )
                if hasattr(result, 'image'):
                    return result.image
                else:
                    return None
        except Exception as e:
            print(f"    Generation error: {e}")
            return None
    
    def generate_animation_frames(self, prompt, animation_type, num_frames, size=64):
        """
        Generate multiple frames for an animation
        Uses reference image for consistency after first frame.
        Args:
            prompt: Base description of the sprite
            animation_type: Type of animation (idle, walk, attack, death)
            num_frames: Number of frames to generate
            size: Size of sprite in pixels
        Returns:
            List of image data
        """
        frames = []
        frame_prompts = self._get_frame_prompts(prompt, animation_type, num_frames)
        reference_image = None
        for i, frame_prompt in enumerate(frame_prompts):
            print(f"    Generating frame {i+1}/{num_frames}...", end="\r")
            frame = self.generate_sprite_frame(frame_prompt, size, reference_image=reference_image)
            if frame:
                frames.append(frame)
                if i == 0:
                    reference_image = frame  # Use first frame as reference for all others
            else:
                print(f"\n    ✗ Failed to generate frame {i+1}")
        print()
        return frames
    
    def _get_frame_prompts(self, base_prompt, animation_type, num_frames):
        """Generate frame-specific prompts for natural animation"""
        prompts = []
        
        for i in range(num_frames):
            progress = i / max(num_frames - 1, 1)  # 0.0 to 1.0
            
            if animation_type == "idle":
                # Subtle breathing/bobbing
                phase = ["resting", "slightly compressed", "normal", "slightly stretched"][i % 4]
                prompt = f"{base_prompt}, {phase}, idle stance, pixel art, top-down view, transparent background"
            
            elif animation_type == "walk":
                # Walking cycle
                phases = ["standing", "lifting foot", "mid-stride", "landing", "standing", "lifting other foot", "mid-stride other side", "landing other side"]
                phase = phases[i % len(phases)]
                prompt = f"{base_prompt}, {phase}, walking animation, pixel art, top-down view, transparent background"
            
            elif animation_type == "attack":
                # Attack sequence
                if progress < 0.33:
                    phase = "winding up attack, pulling back"
                elif progress < 0.66:
                    phase = "lunging forward, attacking"
                else:
                    phase = "returning to stance"
                prompt = f"{base_prompt}, {phase}, attack animation, pixel art, top-down view, transparent background"
            
            elif animation_type == "death":
                # Death sequence
                if progress < 0.25:
                    phase = "hit, recoiling"
                elif progress < 0.5:
                    phase = "collapsing"
                elif progress < 0.75:
                    phase = "fallen, fading"
                else:
                    phase = "dissolving, very faint"
                prompt = f"{base_prompt}, {phase}, death animation, pixel art, top-down view, transparent background"
            
            else:
                prompt = f"{base_prompt}, frame {i+1}, {animation_type} animation, pixel art, top-down view, transparent background"
            
            prompts.append(prompt)
        
        return prompts
    
    def save_image(self, image_data, output_path):
        """Save image data to file"""
        try:
            dir_path = os.path.dirname(output_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            # Handle PixelLab Base64Image type
            if hasattr(image_data, 'base64'):
                import base64
                from PIL import Image
                import io
                # Decode base64 string to bytes
                img_bytes = base64.b64decode(image_data.base64)
                # Create PIL Image from bytes
                img = Image.open(io.BytesIO(img_bytes))
                # Save as PNG
                img.save(output_path, 'PNG')
            elif hasattr(image_data, 'save'):
                # PIL Image
                image_data.save(output_path, 'PNG')
            elif isinstance(image_data, bytes):
                # Raw bytes
                with open(output_path, 'wb') as f:
                    f.write(image_data)
            else:
                # Try to create PIL image from data
                from PIL import Image
                if isinstance(image_data, Image.Image):
                    image_data.save(output_path, 'PNG')
                else:
                    with open(output_path, 'wb') as f:
                        f.write(bytes(image_data))
            
            return True
        except Exception as e:
            print(f"    Save error: {e}")
            import traceback
            traceback.print_exc()
            return False


def generate_enemy(enemy_name, description, output_dir="assets/enemies", size=64, animations=None):
    """
    Generate a complete enemy with all animations
    
    Args:
        enemy_name: Name of the enemy (e.g., "slime", "goblin")
        description: Description for AI generation (e.g., "green puddle of slime")
        output_dir: Base output directory
        size: Sprite size in pixels
        animations: Dict of animation_name: num_frames, or None for defaults
    """
    
    if animations is None:
        animations = DEFAULT_FRAMES
    
    print(f"\n{'='*60}")
    print(f"Generating Enemy: {enemy_name}")
    print(f"Description: {description}")
    print(f"Output: {output_dir}/{enemy_name}")
    print(f"{'='*60}\n")
    
    generator = PixelLabGenerator()
    
    enemy_dir = os.path.join(output_dir, enemy_name)
    total_frames = sum(animations.values())
    completed_frames = 0
    
    for anim_name, num_frames in animations.items():
        print(f"Animation: {anim_name} ({num_frames} frames)")
        
        # Generate animation frames
        frames = generator.generate_animation_frames(
            description,
            anim_name,
            num_frames,
            size
        )
        
        if not frames:
            print(f"  ✗ Failed to generate {anim_name} animation\n")
            continue
        
        # Save frames
        anim_dir = os.path.join(enemy_dir, anim_name)
        os.makedirs(anim_dir, exist_ok=True)
        
        for i, frame_data in enumerate(frames):
            frame_path = os.path.join(anim_dir, f"frame_{i:04d}.png")
            
            if generator.save_image(frame_data, frame_path):
                completed_frames += 1
            else:
                print(f"  ✗ Failed to save frame {i}")
        
        print(f"  ✓ {anim_name} complete ({len(frames)} frames saved)\n")
    
    print(f"\n{'='*60}")
    print(f"Generation Complete!")
    print(f"Total frames: {completed_frames}/{total_frames}")
    print(f"Output directory: {enemy_dir}")
    print(f"{'='*60}\n")
    
    return enemy_dir


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate enemy sprites using PixelLab API")
    parser.add_argument("--name", required=True, help="Enemy name (e.g., 'slime', 'goblin')")
    parser.add_argument("--description", required=True, help="Enemy description for AI")
    parser.add_argument("--output-dir", default="assets/enemies", help="Output directory")
    parser.add_argument("--size", type=int, default=64, help="Sprite size (default: 64)")
    
    args = parser.parse_args()
    
    generate_enemy(
        enemy_name=args.name,
        description=args.description,
        output_dir=args.output_dir,
        size=args.size
    )

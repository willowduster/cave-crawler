"""
Procedural Pixel Art Enemy Generator

Creates simple pixel-art sprite sequences without external APIs.
This is intentionally lightweight and deterministic (via seed) so frames
are consistent across the animation.

Usage:
  python generate_enemy_procedural.py --name goblin --output-dir assets/enemies --size 64 --seed 42

Outputs folder structure compatible with the game's loader:
  assets/enemies/{name}/{animation}/frame_0000.png ...

"""
from __future__ import annotations

import os
import json
import argparse
from pathlib import Path
from typing import Tuple
import random

from PIL import Image, ImageDraw


DEFAULT_FRAMES = {"idle": 4, "walk": 8, "attack": 6, "death": 8}


class ProceduralSprite:
    def __init__(self, name: str, size: int = 64, seed: int | None = None):
        self.name = name
        self.size = size
        self.seed = seed if seed is not None else random.randrange(2**30)
        self.rng = random.Random(self.seed)

        # We'll work on a small grid and scale up to get a crisp pixel look
        self.grid = max(8, self.size // 4)  # e.g., 16 for size 64
        self.scale = self.size // self.grid

        # Base palette for goblin-like characters (can be randomized)
        base_green = (80 + self.rng.randint(-10, 20), 140 + self.rng.randint(-20, 20), 60 + self.rng.randint(-10, 10))
        self.palette = {
            "skin": base_green,
            "eye": (20, 20, 20),
            "accent": (self.rng.randint(60, 200), self.rng.randint(30, 160), self.rng.randint(30, 160)),
            "shadow": (0, 0, 0, 100),
        }

        # Save metadata for reuse
        self.meta = {"seed": self.seed, "palette": self.palette, "grid": self.grid}

    def _new_canvas(self) -> Tuple[Image.Image, ImageDraw.ImageDraw]:
        img = Image.new("RGBA", (self.grid, self.grid), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        return img, draw

    def _upscale(self, img: Image.Image) -> Image.Image:
        return img.resize((self.size, self.size), resample=Image.NEAREST)

    def _draw_base_body(self, draw: ImageDraw.ImageDraw, rng: random.Random):
        # Draw head (top center), body, and legs as simple shapes
        g = self.grid
        # head
        hx = g // 2
        hy = max(2, g // 6)
        head_radius = max(2, g // 6)
        bbox = [hx - head_radius, hy - head_radius, hx + head_radius, hy + head_radius]
        draw.ellipse(bbox, fill=self.palette["skin"])

        # ears
        ear_w = max(1, head_radius // 2)
        draw.polygon([(hx - head_radius, hy), (hx - head_radius - ear_w, hy - ear_w), (hx - head_radius, hy - ear_w*2)], fill=self.palette["skin"])
        draw.polygon([(hx + head_radius, hy), (hx + head_radius + ear_w, hy - ear_w), (hx + head_radius, hy - ear_w*2)], fill=self.palette["skin"])

        # eyes
        eye_y = hy
        eye_x_off = max(1, head_radius // 2)
        draw.point((hx - eye_x_off, eye_y), fill=self.palette["eye"])
        draw.point((hx + eye_x_off, eye_y), fill=self.palette["eye"])

        # body
        body_top = hy + head_radius - 1
        body_bottom = g - max(4, g // 6)
        body_w = max(3, head_radius)
        draw.rectangle([hx - body_w, body_top, hx + body_w, body_bottom], fill=self.palette["accent"])

        # legs
        leg_h = max(1, g // 8)
        draw.rectangle([hx - body_w, body_bottom, hx - body_w//2, body_bottom + leg_h], fill=self.palette["accent"])
        draw.rectangle([hx + body_w//2, body_bottom, hx + body_w, body_bottom + leg_h], fill=self.palette["accent"])

    def _apply_shadow(self, img: Image.Image):
        # Simple shadow overlay to add contrast
        shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        g = self.grid
        sd.ellipse([g//2 - 1, g - 2, g//2 + 1, g], fill=(0,0,0,80))
        return Image.alpha_composite(img, shadow)

    def generate_idle_frames(self, num_frames=4) -> list[Image.Image]:
        frames = []
        for i in range(num_frames):
            img, draw = self._new_canvas()
            # breathing: slight vertical scale
            phase = (i / max(1, num_frames-1)) * 2 * 3.14159
            dy = int(round((1 + 0.08 * (1 + (self.rng.random()-0.5))) * (1 + 0.06 * (random.random()-0.5))))
            # draw base body (deterministic for seed)
            self._draw_base_body(draw, self.rng)
            img = self._apply_shadow(img)
            frames.append(self._upscale(img))
        return frames

    def generate_walk_frames(self, num_frames=8) -> list[Image.Image]:
        frames = []
        g = self.grid
        # We'll implement a simple 4-phase walk cycle so legs move distinctly.
        # Phase mapping: 0 forward-left, 1 mid, 2 forward-right, 3 mid
        for i in range(num_frames):
            img, draw = self._new_canvas()
            # draw base body (head, torso) but we'll redraw limbs for animation
            # reuse the same geometry as _draw_base_body to compute coordinates
            hx = g // 2
            hy = max(2, g // 6)
            head_radius = max(2, g // 6)
            body_top = hy + head_radius - 1
            body_bottom = g - max(4, g // 6)
            body_w = max(3, head_radius)

            # draw head and torso using the existing helper for consistency
            # but avoid drawing default legs (we'll redraw legs below)
            # draw head
            bbox = [hx - head_radius, hy - head_radius, hx + head_radius, hy + head_radius]
            draw.ellipse(bbox, fill=self.palette["skin"])
            # ears
            ear_w = max(1, head_radius // 2)
            draw.polygon([(hx - head_radius, hy), (hx - head_radius - ear_w, hy - ear_w), (hx - head_radius, hy - ear_w*2)], fill=self.palette["skin"])
            draw.polygon([(hx + head_radius, hy), (hx + head_radius + ear_w, hy - ear_w), (hx + head_radius, hy - ear_w*2)], fill=self.palette["skin"])
            # eyes
            eye_y = hy
            eye_x_off = max(1, head_radius // 2)
            draw.point((hx - eye_x_off, eye_y), fill=self.palette["eye"])
            draw.point((hx + eye_x_off, eye_y), fill=self.palette["eye"])
            # torso
            draw.rectangle([hx - body_w, body_top, hx + body_w, body_bottom], fill=self.palette["accent"])

            # walk phase
            phase = i % 4
            # leg baseline positions
            left_leg_x = hx - body_w + 1
            right_leg_x = hx + body_w - 1
            leg_y_top = body_bottom
            leg_y_bottom = body_bottom + max(1, g // 8)

            # compute horizontal foot offset for forward/back positions
            if phase == 0:
                left_offset = 1  # left forward
                right_offset = -1
            elif phase == 1:
                left_offset = 0
                right_offset = 0
            elif phase == 2:
                left_offset = -1
                right_offset = 1  # right forward
            else:
                left_offset = 0
                right_offset = 0

            # draw legs as small rectangles (pixel-art style) with offsets
            draw.rectangle([left_leg_x + left_offset, leg_y_top, left_leg_x + left_offset + 1, leg_y_bottom], fill=self.palette["accent"])
            draw.rectangle([right_leg_x + right_offset, leg_y_top, right_leg_x + right_offset + 1, leg_y_bottom], fill=self.palette["accent"])

            # simple arm swing opposite to leg
            arm_y = body_top + 1
            if phase in (0, 2):
                # extended arm on same side as forward leg
                draw.point((hx - body_w - (1 if phase == 0 else 0), arm_y), fill=self.palette["accent"])
                draw.point((hx + body_w + (1 if phase == 2 else 0), arm_y), fill=self.palette["accent"])
            else:
                draw.point((hx - body_w, arm_y), fill=self.palette["accent"])
                draw.point((hx + body_w, arm_y), fill=self.palette["accent"])

            img = self._apply_shadow(img)
            frames.append(self._upscale(img))
        return frames

    def generate_attack_frames(self, num_frames=6) -> list[Image.Image]:
        frames = []
        g = self.grid
        for i in range(num_frames):
            img, draw = self._new_canvas()
            self._draw_base_body(draw, self.rng)
            # attack: extend an arm as a rectangle/pixel
            extend = 1 + (i % 3)
            draw.rectangle([g//2 + 2, g//2 - 1, min(g-1, g//2 + 2 + extend), g//2 + 1], fill=self.palette["accent"])
            img = self._apply_shadow(img)
            frames.append(self._upscale(img))
        return frames

    def generate_death_frames(self, num_frames=8) -> list[Image.Image]:
        frames = []
        for i in range(num_frames):
            img, draw = self._new_canvas()
            self._draw_base_body(draw, self.rng)
            # fade out progressively
            up = self._upscale(img)
            alpha = int(255 * (1 - (i / max(1, num_frames-1))))
            up.putalpha(alpha)
            frames.append(up)
        return frames


def save_frames(base_dir: Path, name: str, anim: str, frames: list[Image.Image]):
    out = base_dir / name / anim
    out.mkdir(parents=True, exist_ok=True)
    for i, im in enumerate(frames):
        path = out / f"frame_{i:04d}.png"
        im.save(path)


def generate_enemy(name: str, description: str, output_dir: str = "assets/enemies", size: int = 64, animations: dict | None = None, seed: int | None = None):
    if animations is None:
        animations = DEFAULT_FRAMES
    base = Path(output_dir)
    gen = ProceduralSprite(name, size=size, seed=seed)

    # Save seed/meta for reproducibility
    meta_path = base / name / "meta.json"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    with open(meta_path, "w") as f:
        json.dump(gen.meta, f, indent=2)

    # Generate each animation
    results = {}
    for anim, n in animations.items():
        if anim == "idle":
            frames = gen.generate_idle_frames(n)
        elif anim == "walk":
            frames = gen.generate_walk_frames(n)
        elif anim == "attack":
            frames = gen.generate_attack_frames(n)
        elif anim == "death":
            frames = gen.generate_death_frames(n)
        else:
            frames = gen.generate_idle_frames(n)

        save_frames(base, name, anim, frames)
        results[anim] = len(frames)

    return base / name


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--output-dir", default="assets/enemies")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    out = generate_enemy(args.name, args.description, args.output_dir, args.size, seed=args.seed)
    print(f"Generated enemy at: {out}")

# Isometric Tileset Documentation

## Generated Tiles

### cave_floor_iso.png
- **Type**: Floor tile
- **Size**: 128x64 pixels (rendered at 2x for quality)
- **Actual tile size**: 64x32 pixels (2:1 isometric ratio)
- **Color**: Dark stone (RGB: 64, 51, 38)
- **Material**: Stone with high roughness (0.9)
- **Details**: Subdivided for realistic geometry
- **Use**: Main cave floor surfaces

### cave_wall_iso.png
- **Type**: Wall tile with height
- **Size**: 128x64 pixels base
- **Height**: Includes vertical component for depth
- **Color**: Slightly lighter stone (RGB: 77, 64, 51)
- **Material**: Stone with medium-high roughness (0.85)
- **Geometry**: Thin wall (0.1 thickness) with 0.5 height scale
- **Use**: Cave walls, barriers, room boundaries

## Rendering Specifications

### Camera Setup
- **Type**: Orthographic (not perspective)
- **Isometric Angle**: 26.565° (arctan(0.5))
- **Rotation**: 45° around Z-axis, then ISO_ANGLE around X-axis
- **Ortho Scale**: 3.0 units
- **Position**: (0, 0, 10) looking down

### Lighting
- **Main Light**: Sun lamp at 45° angle, energy 1.5
- **Fill Light**: Sun lamp from opposite side, energy 0.5
- **Background**: Dark cave atmosphere (RGB: 13, 13, 20)
- **Style**: Atmospheric cave lighting

### Render Settings
- **Engine**: Cycles
- **Samples**: 64 (balanced quality/speed)
- **Resolution**: 128x64 pixels
- **Transparency**: Enabled (RGBA PNG)
- **Format**: PNG with alpha channel

## Usage in Godot

### Import Settings
1. Open tile in Godot
2. Set **Filter**: Disabled (for pixel-perfect)
3. Set **Mipmaps**: Disabled
4. **Compress**: VRAM Compressed recommended

### TileMap Setup
```gdscript
# Create TileMap node
# Set tile size: 64x32
# Set isometric mode or manual offset
# Paint tiles in scene
```

### Collision
- Floor tiles: No collision (walkable)
- Wall tiles: Add collision shape for boundaries

## Creating More Tiles

### To add variations:
1. Edit `blender_scripts/create_iso_tiles.py`
2. Add new creation functions (e.g., `create_corner_tile()`)
3. Call in `main()` with `render_tile("new_tile_name")`
4. Run: `blender --background --python blender_scripts/create_iso_tiles.py`

### Suggested additions:
- Corner pieces (inner/outer)
- Different floor textures (dirt, gravel, stone)
- Props (stalactites, stalagmites, crystals)
- Destructible objects
- Doorways and passages
- Decorative elements

## Color Palette
- **Floor**: #403326 (64, 51, 38) - Dark brown/gray
- **Walls**: #4D4033 (77, 64, 51) - Lighter stone
- **Background**: #0D0D14 (13, 13, 20) - Deep cave darkness

## Next Steps
1. ✅ Generate base tiles (floor, wall)
2. 🔄 Import into Godot
3. 🔄 Create TileMap with isometric tiles
4. 🔄 Build test level
5. ⏳ Add tile variations
6. ⏳ Create props and decorations
7. ⏳ Add lighting system

---

**Status**: Base tiles generated successfully!
**Files**: Located in `assets/tiles/`
**Ready for**: Godot TileMap integration

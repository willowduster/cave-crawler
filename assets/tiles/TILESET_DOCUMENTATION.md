# Isometric Tileset Documentation

## Generated Tiles (12 Total)

### Floor Tiles (3 variations)

#### cave_floor_iso.png
- **Type**: Floor tile (standard)
- **Size**: 128x64 pixels (rendered at 2x for quality)
- **Actual tile size**: 64x32 pixels (2:1 isometric ratio)
- **Color**: Dark stone (RGB: 64, 51, 38 / #403326)
- **Material**: Stone with high roughness (0.9)
- **Details**: Subdivided for realistic geometry
- **Use**: Main cave floor surfaces

#### cave_floor_dark.png
- **Type**: Floor tile (darker variation)
- **Color**: Darker stone (RGB: 51, 38, 26 / #332619)
- **Material**: Stone with high roughness (0.9)
- **Use**: Shadowed areas, depth variation, visual interest

#### cave_floor_light.png
- **Type**: Floor tile (lighter variation)
- **Color**: Lighter stone (RGB: 77, 64, 51 / #4D4033)
- **Material**: Stone with high roughness (0.9)
- **Use**: Illuminated areas, highlights, contrast

### Wall Tiles (3 types)

#### cave_wall_iso.png
- **Type**: Wall tile with height (straight)
- **Size**: 128x64 pixels base
- **Height**: Includes vertical component for depth
- **Color**: Medium stone (RGB: 77, 64, 51 / #4D4033)
- **Material**: Stone with medium-high roughness (0.85)
- **Geometry**: Thin wall (0.1 thickness) with 0.5 height scale
- **Collision**: Required for boundaries
- **Use**: Cave walls, barriers, corridor sides

#### cave_wall_corner_outer.png
- **Type**: Outer corner wall (L-shaped, convex)
- **Shape**: Two perpendicular wall segments joined
- **Color**: Medium stone (RGB: 77, 64, 51 / #4D4033)
- **Collision**: Required
- **Use**: Convex corners, room exteriors, turning points

#### cave_wall_corner_inner.png
- **Type**: Inner corner wall (concave)
- **Shape**: Recessed corner
- **Color**: Medium stone (RGB: 77, 64, 51 / #4D4033)
- **Collision**: Required
- **Use**: Concave corners, alcoves, indented areas

### Props (6 decorative/obstacle elements)

#### prop_stalactite.png
- **Type**: Hanging ceiling formation
- **Color**: Dark gray-blue (RGB: 38, 38, 46 / #26262E)
- **Shape**: Cone pointing downward (6 vertices)
- **Size**: 0.3 radius, 1.5 height
- **Roughness**: 0.7
- **Collision**: Usually none (decoration)
- **Use**: Ceiling decoration, atmospheric detail

#### prop_stalagmite.png
- **Type**: Floor formation
- **Color**: Dark gray-blue (RGB: 38, 38, 46 / #26262E)
- **Shape**: Cone pointing upward (6 vertices)
- **Size**: 0.4 radius, 1.2 height
- **Roughness**: 0.7
- **Collision**: Optional (depends on gameplay)
- **Use**: Floor obstacles, natural formations

#### prop_rock_small.png
- **Type**: Small obstacle rock
- **Color**: Gray-brown (RGB: 89, 77, 64 / #594D40)
- **Shape**: Irregular icosphere (subdivisions: 1)
- **Scale**: (1, 0.8, 0.6) - asymmetric
- **Roughness**: 0.95 (very rough)
- **Collision**: Recommended
- **Use**: Small obstacles, scattered debris

#### prop_rock_large.png
- **Type**: Large obstacle rock
- **Color**: Gray-brown (RGB: 89, 77, 64 / #594D40)
- **Shape**: Larger irregular icosphere
- **Scale**: (1.2, 1, 0.7) - asymmetric
- **Roughness**: 0.95
- **Collision**: Required
- **Use**: Major obstacles, path blockers, cover

#### prop_crystal.png
- **Type**: Glowing crystal (magical element)
- **Base Color**: Cyan (RGB: 77, 153, 204 / #4D99CC)
- **Emission**: Bright cyan (RGB: 102, 204, 255 / #66CCFF)
- **Emission Strength**: 2.0 (glows visibly!)
- **Shape**: Elongated diamond (4-sided pyramid)
- **Size**: 0.2 radius, 0.8 height
- **Roughness**: 0.1 (very shiny, reflective)
- **Collision**: Optional (collectible or obstacle)
- **Use**: Light sources, collectibles, magic indicators, waypoints

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

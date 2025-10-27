# TileMap Setup Guide

## Overview
The cave crawler now uses a proper isometric TileMap system with 12 tiles generated from Blender.

## Generated Tiles

### Floor Tiles (3 variations)
- `cave_floor_iso.png` - Standard dark stone floor
- `cave_floor_dark.png` - Darker variation for shadows/depth
- `cave_floor_light.png` - Lighter variation for highlights

### Wall Tiles (3 types)
- `cave_wall_iso.png` - Straight wall segment
- `cave_wall_corner_outer.png` - Outer corner (L-shaped)
- `cave_wall_corner_inner.png` - Inner corner (concave)

### Props (6 decorative elements)
- `prop_stalactite.png` - Hanging from ceiling
- `prop_stalagmite.png` - Rising from floor
- `prop_rock_small.png` - Small obstacle
- `prop_rock_large.png` - Large obstacle
- `prop_crystal.png` - Glowing cyan crystal (with emission)

## TileSet Configuration

**File**: `resources/tilesets/cave_tileset.tres`

**Settings**:
- Tile Size: 64x32 (isometric 2:1 ratio)
- Physics Layer: Enabled for walls
- Texture Filter: Nearest (pixel-perfect rendering)
- Tile Shape: Isometric

## Using the TileMap

### Opening in Godot Editor

1. Open `scenes/levels/cave_level_01.tscn`
2. Select the `TileMap` node in the scene tree
3. Click "TileSet" in the bottom panel
4. You'll see all available tiles organized by source

### Painting Tiles

**Floor Tiles** (Sources 0-2):
- Use for walkable areas
- Mix variations for visual interest
- No collision by default

**Wall Tiles** (Sources 3-5):
- Use for boundaries and obstacles
- Have collision shapes automatically
- Use corners for proper wall connections

**Props** (Future implementation):
- Will be added as separate sprite nodes
- Positioned manually for decoration
- Some will have collision (rocks)

### Layer Organization

The scene uses Y-sorting for proper depth:
- Background (z_index: -100) - Solid color
- TileMap (y_sort_enabled: true) - Main level geometry
- Player (z_index: 100) - Character sprite

Objects with higher Y values appear in front of objects with lower Y values.

## Camera Settings

- Zoom: 1.5x (shows more of the level than test scene)
- Position: Follows player (can be made dynamic later)
- Mode: Fixed for now (will add smooth follow)

## Performance Notes

- All tiles are 128x64 in Blender but rendered at 64x32 in Godot
- Using CompressedTexture2D for memory efficiency
- No mipmaps needed (tiles are small and fixed size)
- Y-sorting has minimal performance impact at this scale

## Next Steps

1. **Paint a Basic Level**:
   - Open cave_level_01.tscn in Godot editor
   - Select TileMap node
   - Use floor tiles to create walkable area
   - Add wall tiles around perimeter
   - Test player collision

2. **Add Props**:
   - Place stalactites near ceiling areas
   - Add stalagmites for obstacles
   - Scatter rocks for terrain variation
   - Place crystals for visual interest

3. **Create Multiple Rooms**:
   - Design interconnected cave chambers
   - Use different floor variations for each room
   - Add narrow corridors between rooms

4. **Test Gameplay**:
   - Verify click-to-move works with tiles
   - Check collision boundaries
   - Ensure depth sorting looks correct
   - Test player movement through corridors

## Regenerating Tiles

To create more tiles or modify existing ones:

```powershell
& "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --background --python "C:\Users\Ben\code\cave-crawler\blender_scripts\create_iso_tiles.py"
```

Edit `create_iso_tiles.py` to add new tile types or modify colors/materials.

## Troubleshooting

**Tiles look blurry**:
- Check that texture filter is set to "Nearest" in import settings
- Verify tile_size matches rendered size (64x32)

**Collision not working**:
- Ensure wall tiles have physics_layer_0 collision shapes
- Check that player has collision layer/mask set correctly

**Depth sorting wrong**:
- Verify TileMap has y_sort_enabled = true
- Check that player updates z_index in _process()
- Ensure Background has negative z_index

**Tiles not appearing in editor**:
- Check that cave_tileset.tres loads all texture resources
- Verify PNG files exist in assets/tiles/
- Try reimporting tiles (right-click > Reimport)

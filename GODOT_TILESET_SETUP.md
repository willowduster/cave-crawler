# Setting Up the Isometric TileMap in Godot Editor

## Current Status ✓

- **Tiles Generated**: 12 isometric tiles created using Blender
- **Blender Script**: `blender_scripts/create_iso_tiles.py` (reusable)
- **Tile Location**: `assets/tiles/` folder
- **Scene Ready**: `scenes/levels/cave_level_01.tscn`
- **Player Controls**: Click-to-move working

## Tiles Available

### Floor Tiles
1. `cave_floor_iso.png` - Standard dark stone
2. `cave_floor_dark.png` - Darker variation
3. `cave_floor_light.png` - Lighter variation

### Wall Tiles
4. `cave_wall_iso.png` - Straight wall
5. `cave_wall_corner_outer.png` - L-shaped outer corner
6. `cave_wall_corner_inner.png` - Concave inner corner

### Props
7. `prop_stalactite.png` - Hanging spike
8. `prop_stalagmite.png` - Floor spike
9. `prop_rock_small.png` - Small obstacle
10. `prop_rock_large.png` - Large obstacle
11. `prop_crystal.png` - Glowing crystal

## Step-by-Step: Create TileSet in Godot Editor

### Method 1: Using Godot Editor (Recommended)

1. **Open the Godot editor** (should already be running)
   - The editor will auto-import all PNG files in `assets/tiles/`
   - Wait for import to complete (watch bottom-right corner)

2. **Create a TileSet Resource**:
   - In FileSystem panel, navigate to `assets/tiles/`
   - Right-click any tile PNG → "Create TileSet"
   - Save as `resources/tilesets/cave_tileset.tres`

3. **Configure TileSet**:
   - Double-click `cave_tileset.tres` to open TileSet editor
   - In the bottom panel, you'll see the TileSet editor
   - Click "Add Atlas" button (looks like +)
   - Select all 12 PNG files from `assets/tiles/`

4. **Set Tile Properties**:
   - **Tile Size**: Set to 64x32 (matches isometric ratio)
   - **Texture Filter**: Set to "Nearest" (pixel-perfect)
   - **For Wall Tiles**: Add physics collision shapes:
     - Select wall tile in atlas
     - Click "Physics Layer 0" tab
     - Click "Add Polygon" and draw collision box
     - Repeat for all wall types

5. **Add TileMapLayer to Scene**:
   - Open `scenes/levels/cave_level_01.tscn`
   - Right-click "CaveLevel" node → Add Child Node
   - Search for "TileMapLayer"
   - Name it "TileMap"

6. **Assign TileSet to TileMap**:
   - Select the TileMap node
   - In Inspector panel, find "Tile Set" property
   - Click dropdown → "Load" → Select `cave_tileset.tres`

7. **Configure TileMap Settings**:
   - **Y Sort Enabled**: Check this box (critical for depth sorting!)
   - **Z Index**: Leave at 0 (between background and player)
   - **Transform**: Leave at origin (0, 0)

8. **Paint Your Level**:
   - With TileMap selected, bottom panel shows tile palette
   - Click a tile to select it
   - Click in viewport to place tiles
   - Use floor tiles for walkable areas
   - Use wall tiles for boundaries
   - Test player collision!

### Method 2: Quick Test (Sprites Instead of TileMap)

If TileSet setup is complex, test tiles as sprites first:

1. Add Sprite2D node to scene
2. Set texture to one of the tile PNGs
3. Adjust position
4. Verify tiles look correct before doing full TileMap setup

## Tile Specifications

**Rendered Size**: 128x64 pixels (in Blender)
**Godot Size**: 64x32 pixels (scaled down 2x)
**Isometric Angle**: 26.565° (arctan 0.5)
**Ratio**: 2:1 (width:height)

## Troubleshooting

### Tiles not imported
- Check `assets/tiles/` folder has all PNG files
- Restart Godot editor
- Right-click folder → "Reimport"

### Tiles look blurry
- TileSet → Select atlas → Filter mode: Nearest
- Also check Project Settings → Rendering → Textures → Default Filter: Nearest

### Collision not working
- Ensure wall tiles have collision polygons in TileSet editor
- Check player's collision layer/mask matches TileMap's
- Test by adding debug collision shapes visibility

### Y-sorting not working
- TileMap node must have "Y Sort Enabled" checked
- Player script must update `z_index = int(global_position.y)` in `_process()`
- Background must have negative z_index

### Tiles appear wrong size
- TileSet tile_size should be 64x32
- If tiles are 128x64, they'll appear 2x too large
- Check texture import settings: No compression, no mipmaps

## Next Steps After TileMap Setup

1. **Paint a basic cave room** (10x10 tiles)
2. **Add wall boundaries** around the room
3. **Test player movement** and collision
4. **Add props** (stalactites, rocks) as separate sprites
5. **Create multiple rooms** connected by corridors
6. **Test depth sorting** - player should go behind/in front properly

## Alternative: Manual Scene Creation

If you prefer to work directly with scene files instead of the editor:

```gdscript
# This would be done in GDScript, but it's easier to use the editor
# The TileSet resource format is complex and best created visually
```

## Performance Notes

- 12 tiles = ~1.5 MB total (128x64 each with transparency)
- TileMap is very efficient - can have thousands of tiles
- Y-sorting has minimal overhead for small levels
- Consider tile atlases for better batching (future optimization)

## Regenerating or Adding Tiles

Edit `blender_scripts/create_iso_tiles.py`:

1. Add new `create_xxx_tile()` function
2. Call it in `main()` before the summary
3. Run Blender script:
   ```powershell
   & "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --background --python "C:\Users\Ben\code\cave-crawler\blender_scripts\create_iso_tiles.py"
   ```
4. Godot will auto-reimport new PNGs
5. Add new tile to TileSet in editor

## Quick Reference: TileSet Creation Commands

Since we're using Godot 4.5, TileMapLayer is the modern approach (replaces old TileMap node).

**Key Settings**:
- Tile Size: Vector2i(64, 32)
- Physics Layers: 1 (for collision)
- Y Sort: Enabled
- Rendering Layers: Default

**Wall Collision Shape**:
- Use simple rectangle: (-32, -16) to (32, 16)
- This gives full-tile collision
- Adjust per wall type if needed

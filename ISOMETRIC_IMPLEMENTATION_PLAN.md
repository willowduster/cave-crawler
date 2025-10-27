# Isometric Implementation Plan - Cave Crawler

## Design Decision: Pivot to Isometric (Diablo 2 Style)

**Date**: October 27, 2025  
**Status**: Phase 2 platformer proof-of-concept complete, pivoting to isometric design

## Why Isometric?
- Better fits cave exploration theme
- Diablo 2-style gameplay is more engaging for dungeon crawling
- Allows for more strategic combat and exploration
- Top-down perspective works better for cave systems

## Core Isometric Concepts

### 1. Camera & Perspective
```
Isometric Angle: 2:1 ratio (typical for games)
- Camera tilted at ~26.565° (arctan(0.5))
- Fixed camera angle (no rotation)
- Camera follows player smoothly
- Zoom level: 2-3x for good visibility
```

### 2. Movement System
**8-Directional Movement** (instead of 2D platformer):
- **W** - Move up-left
- **A** - Move down-left  
- **S** - Move down-right
- **D** - Move up-right
- **W+D** - Move up
- **W+A** - Move left
- **S+A** - Move down
- **S+D** - Move right

**Physics Changes**:
- ❌ Remove jumping (not needed in isometric)
- ❌ Remove gravity (top-down view)
- ✅ Keep smooth acceleration/deceleration
- ✅ Add collision with walls and obstacles
- ✅ Implement depth sorting (Y-sorting)

### 3. Depth Sorting (Y-Sorting)
Critical for proper visual layering:
```gdscript
# Objects with lower Y position appear in front
# Player at Y=100 appears in front of tree at Y=50
func _process(_delta):
    z_index = int(global_position.y)
```

### 4. Tile System

#### Isometric Tile Dimensions
```
Base Tile Size: 64x32 pixels (2:1 ratio)
- Width: 64 pixels
- Height: 32 pixels (base)
- Height for walls: 64-96 pixels (includes vertical height)
```

#### Tile Types Needed
1. **Floor Tiles**
   - Cave floor (stone, dirt, gravel)
   - Different textures for variety
   
2. **Wall Tiles**
   - Cave walls (vertical faces)
   - Corner pieces
   - Edges and transitions
   
3. **Objects**
   - Stalactites (ceiling decorations)
   - Stalagmites (floor obstacles)
   - Crystals, rocks, debris
   
4. **Interactive**
   - Doors/passages
   - Treasure chests
   - Interactive objects

### 5. Grid System
```
World Grid: Aligned to isometric coordinates
- Grid cell: 64x32 pixels
- World position to grid conversion
- Grid to screen position conversion

Conversion formulas:
screen_x = (world_x - world_y) * tile_width/2
screen_y = (world_x + world_y) * tile_height/2
```

## Implementation Roadmap

### Phase 2.5: Isometric Conversion (Current)

#### Step 1: Update Player Movement ✋ (Next)
```gdscript
# Remove platformer physics
- Remove JUMP_VELOCITY
- Remove gravity
- Remove is_on_floor() checks

# Add isometric movement
- 8-directional input (WASD)
- Normalize diagonal movement
- Keep acceleration/friction
- Add Y-sorting for depth
```

#### Step 2: Create Isometric Tileset
**Using Blender MCP**:
1. Create base tile template (64x32)
2. Model cave floor tile
3. Model cave wall tiles (with height)
4. Render at proper isometric angle
5. Export as sprite sheets

**Tile Specifications**:
- Resolution: 64x32 for floors, 64x96 for walls
- Perspective: 26.565° isometric angle
- Lighting: Consistent directional light
- Style: Dark cave aesthetic

#### Step 3: Build Isometric Level
- Create TileMap node
- Set up isometric grid
- Paint cave corridors and rooms
- Add collision shapes to walls
- Test player navigation

#### Step 4: Depth Sorting Setup
```gdscript
# In player script and all game objects
func _process(_delta):
    z_index = int(global_position.y)
    # Ensures proper visual layering
```

### Phase 3: Core Isometric Features

#### Movement & Physics
- [ ] 8-directional movement working
- [ ] Collision with walls
- [ ] Smooth camera follow
- [ ] Depth sorting functional
- [ ] Movement speed balanced

#### Visual System
- [ ] Isometric tileset complete
- [ ] Floor tiles rendering
- [ ] Wall tiles with proper height
- [ ] Smooth transitions between tiles
- [ ] Cave lighting/darkness

#### Player Character
- [ ] Isometric character sprite (8 directions or 4 with flip)
- [ ] Idle animation
- [ ] Walk animation (8 directions)
- [ ] Proper depth sorting

### Phase 4: Gameplay Features

#### Combat System
- [ ] Click-to-attack or hotkey abilities
- [ ] Melee attack range
- [ ] Ranged attacks (if applicable)
- [ ] Damage system

#### Exploration
- [ ] Multiple interconnected rooms
- [ ] Doors/passages
- [ ] Hidden areas
- [ ] Interactive objects

#### Progression
- [ ] Health system
- [ ] Experience/leveling (optional)
- [ ] Inventory system
- [ ] Loot drops

## Technical Specifications

### Godot 4.5 Isometric Setup

#### Project Settings
```
Display:
- Resolution: 1280x720 or 1920x1080
- Stretch mode: canvas_items
- Aspect: keep

Physics:
- Default gravity: 0 (no gravity for top-down)
- 2D physics only
```

#### Scene Structure
```
Level (Node2D)
├── TileMap (isometric grid)
├── YSort (Node2D with y_sort_enabled)
│   ├── Player (CharacterBody2D)
│   ├── Enemies (CharacterBody2D group)
│   ├── Objects (StaticBody2D group)
│   └── Effects (Sprites, particles)
└── Camera2D (follows player)
```

### Player Controller
```gdscript
extends CharacterBody2D

const SPEED = 150.0  # Adjusted for isometric
const ACCELERATION = 600.0
const FRICTION = 800.0

func _physics_process(delta):
    # Get 8-directional input
    var input_vector = Vector2.ZERO
    input_vector.x = Input.get_axis("move_left", "move_right")
    input_vector.y = Input.get_axis("move_up", "move_down")
    
    # Normalize for consistent diagonal speed
    input_vector = input_vector.normalized()
    
    # Apply movement
    if input_vector != Vector2.ZERO:
        velocity = velocity.move_toward(
            input_vector * SPEED, 
            ACCELERATION * delta
        )
    else:
        velocity = velocity.move_toward(
            Vector2.ZERO, 
            FRICTION * delta
        )
    
    move_and_slide()

func _process(_delta):
    # Depth sorting
    z_index = int(global_position.y)
```

### Input Configuration
```
move_up: W, Up Arrow
move_down: S, Down Arrow  
move_left: A, Left Arrow
move_right: D, Right Arrow
```

## Art Style Guidelines

### Color Palette
- **Cave Walls**: Dark grays, browns (#2a2a2a, #3d3d3d)
- **Cave Floor**: Medium browns, stone grays (#4a4a4a, #5a5555)
- **Lighting**: Warm torchlight (#ffa500, #ff6600)
- **Crystals/Gems**: Blues, purples, teals (accent colors)
- **Player**: Contrasting color for visibility

### Lighting Approach
1. **Ambient darkness** (dark base)
2. **Local light sources** (torches, crystals)
3. **Player torch/light** (radial light around player)
4. **Shadow casting** (for depth)

## Next Immediate Steps

1. ✅ **Archive platformer proof-of-concept**
   - Move current level to `_archived/platformer_poc/`
   
2. 🔄 **Update player movement script**
   - Implement 8-directional isometric movement
   - Remove jumping/gravity
   - Add depth sorting
   
3. 🎨 **Create first isometric tiles** (using Blender MCP)
   - Basic cave floor tile
   - Basic cave wall tile
   - Test rendering
   
4. 🗺️ **Build test level**
   - Small cave room
   - Test player movement
   - Verify depth sorting

## References & Inspiration
- **Diablo 2**: Classic isometric ARPG
- **Path of Exile**: Modern isometric dungeon crawler
- **Hades**: Isometric action with great art style
- **Godot Isometric Demos**: Reference implementations

## Success Criteria
- [ ] Player moves smoothly in 8 directions
- [ ] Depth sorting works correctly (no visual glitches)
- [ ] Tiles render properly with isometric perspective
- [ ] Camera follows player smoothly
- [ ] Collision works with cave walls
- [ ] Performance is smooth (60 FPS)

---

**Status**: Planning complete, ready to begin isometric implementation
**Next Action**: Update player movement script for isometric controls

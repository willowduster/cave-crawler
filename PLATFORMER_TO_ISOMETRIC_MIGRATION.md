# Platformer to Isometric Migration Guide

## Summary
Successfully tested platformer proof-of-concept. Movement, physics, and scene system working perfectly. Now pivoting to **isometric Diablo 2-style gameplay** for better cave crawler experience.

## What We're Keeping
✅ **Working Systems**:
- Scene loading system
- Player movement physics (acceleration/friction)
- Camera follow system
- Input handling structure
- MCP development workflow

## What We're Changing

### Player Movement
**Before (Platformer)**:
```gdscript
- 2D horizontal movement (left/right)
- Jumping with JUMP_VELOCITY
- Gravity application
- is_on_floor() checks
```

**After (Isometric)**:
```gdscript
- 8-directional movement (WASD → diagonal iso)
- No jumping
- No gravity
- Depth sorting (z_index = y position)
```

### Level Design
**Before (Platformer)**:
- Platforms at different heights
- Vertical navigation via jumping
- Side-view perspective

**After (Isometric)**:
- Top-down isometric tiles (64x32)
- Cave rooms and corridors
- Wall collision
- Depth layering (Y-sort)

### Camera
**Before**: Side-scrolling follow
**After**: Isometric angle follow (same follow logic, different perspective)

## Migration Steps

### Step 1: Archive Platformer POC ✅
```powershell
# Create archive folder
mkdir _archived/platformer_poc
mv scenes/levels/level_01.tscn _archived/platformer_poc/
# Keep player scene, will modify it
```

### Step 2: Update Player Script 🔄 NEXT
File: `scripts/player/player_movement.gd`

**Remove**:
- `JUMP_VELOCITY` constant
- `gravity` variable
- `is_on_floor()` checks
- Jump input handling

**Add**:
- 8-directional input (up, down, left, right)
- Input normalization for diagonals
- Depth sorting in `_process()`

**Keep**:
- `SPEED`, `ACCELERATION`, `FRICTION`
- `move_and_slide()` for collision
- Smooth movement physics

### Step 3: Update Input Map
**Add New Actions**:
```
move_up: W, Up Arrow
move_down: S, Down Arrow
move_left: A, Left Arrow (already exists)
move_right: D, Right Arrow (already exists)
```

**Remove**:
- Jump action (ui_accept) - no longer needed

### Step 4: Create Isometric Tileset
Using Blender MCP:
1. Model basic cave floor tile
2. Model basic cave wall tile
3. Set isometric camera angle
4. Render tiles to sprites
5. Import into Godot

### Step 5: Build Test Level
1. Create new scene: `scenes/levels/iso_test_01.tscn`
2. Add TileMap node with isometric tiles
3. Paint simple cave room
4. Add player spawn point
5. Test movement and depth sorting

## Code Changes Required

### Updated Player Movement Script
```gdscript
extends CharacterBody2D

const SPEED = 150.0
const ACCELERATION = 600.0
const FRICTION = 800.0

func _physics_process(delta):
    # Get 8-directional input
    var input_vector = Vector2.ZERO
    input_vector.x = Input.get_axis("move_left", "move_right")
    input_vector.y = Input.get_axis("move_up", "move_down")
    
    # Normalize diagonal movement
    input_vector = input_vector.normalized()
    
    # Apply movement with acceleration/friction
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
    # Depth sorting for isometric layering
    z_index = int(global_position.y)

func _ready():
    print("Isometric player ready!")
```

### Input Configuration (project.godot)
```ini
[input]

move_up={
"deadzone": 0.5,
"events": [InputEventKey(keycode=W), InputEventKey(keycode=UP)]
}

move_down={
"deadzone": 0.5,
"events": [InputEventKey(keycode=S), InputEventKey(keycode=DOWN)]
}

move_left={
"deadzone": 0.5,
"events": [InputEventKey(keycode=A), InputEventKey(keycode=LEFT)]
}

move_right={
"deadzone": 0.5,
"events": [InputEventKey(keycode=D), InputEventKey(keycode=RIGHT)]
}
```

## Testing Checklist

### Isometric Movement Test
- [ ] W key moves player up-left (isometric "north")
- [ ] S key moves player down-right (isometric "south")
- [ ] A key moves player down-left (isometric "west")
- [ ] D key moves player up-right (isometric "east")
- [ ] W+D moves player straight up
- [ ] S+A moves player straight down
- [ ] W+A moves player straight left
- [ ] S+D moves player straight right
- [ ] Diagonal movement speed equals cardinal movement

### Depth Sorting Test
- [ ] Player appears in front of objects with lower Y
- [ ] Player appears behind objects with higher Y
- [ ] No visual glitches when moving

### Collision Test
- [ ] Player collides with walls
- [ ] Player can navigate corridors
- [ ] No getting stuck in corners

## Timeline

**Estimated Time**: 2-4 hours for basic isometric conversion

1. **Hour 1**: Update player script and input (30 min) + testing (30 min)
2. **Hour 2**: Create basic isometric tiles in Blender
3. **Hour 3**: Build test level and configure tilemap
4. **Hour 4**: Testing, tweaking, polish

## Success Criteria
✅ Player moves smoothly in 8 directions
✅ Depth sorting works correctly
✅ Tiles render with proper isometric perspective
✅ Camera follows player
✅ Collision works
✅ No major bugs

---

**Current Status**: Ready to begin isometric conversion
**Next Action**: Update player movement script
**Reference**: See `ISOMETRIC_IMPLEMENTATION_PLAN.md` for full details

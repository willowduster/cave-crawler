# Cave Crawler - Project Constitution & Development Plan

## 🎯 Project Overview

**Cave Crawler** is an **isometric cave exploration game** (Diablo 2 style) built with Godot 4.5.1, utilizing AI-powered Model Context Protocol (MCP) servers for accelerated development.

**Game Style**: Isometric action RPG with dungeon crawling, exploration, and combat in procedurally generated or hand-crafted cave systems.

## 🛠️ Technology Stack

### Core Engine
- **Godot Engine**: 4.5.1 (stable)
- **Language**: GDScript
- **Rendering**: Forward+ (2D optimized)

### Development Tools
- **AI Assistant**: Claude Desktop or Cursor with MCP integration
- **Version Control**: Git
- **Asset Creation**: Blender 4.5 (for 3D-rendered 2D sprites)
- **Image Editing**: Manual tools (GIMP, Photoshop, or online editors)

### MCP Servers (Fully Operational)
1. **Godot MCP** ✅
   - Launch and control Godot editor
   - Create and manage scenes
   - Add nodes and configure properties
   - Run and debug projects
   
2. **Blender MCP** ✅
   - Create 3D models
   - Generate textures and materials
   - Render 2D sprites from 3D models
   - Export assets for Godot

3. **Filesystem MCP** ✅
   - File operations
   - Project structure management

4. **Git MCP** ✅
   - Version control
   - Commit and branch management

## 📋 Development Workflow

### Phase 1: Core Systems ✅ COMPLETE
- [x] Set up development environment
- [x] Install and configure Godot 4.5.1
- [x] Install and test MCP servers
- [x] Create project structure
- [x] Initialize Git repository
- [x] Create test scene (verified working)
- [x] Platformer proof-of-concept tested (pivoting to isometric)

### Phase 2: Isometric Foundation 🔄 IN PROGRESS
**Priority**: Isometric Core Mechanics

**Design Pivot**: After successful platformer proof-of-concept, pivoting to **Diablo 2-style isometric gameplay** for better cave exploration experience.

1. **Isometric Player Character**
   - ✅ Basic movement working (proof-of-concept)
   - 🔄 Convert to 8-directional isometric movement
   - ❌ Remove jumping/gravity (not needed in isometric)
   - ✅ Keep smooth acceleration/deceleration
   - 🔄 Implement depth sorting (Y-sorting)
   - 🔜 Add 8-directional animations (idle, walk)

2. **Isometric Camera System**
   - ✅ Camera follow working
   - 🔄 Adjust for isometric perspective
   - 🔜 Fixed isometric angle (~26.565°)
   - 🔜 Proper zoom level for visibility

3. **Isometric Cave Environment**
   - 🔜 Create isometric tileset (64x32 base tiles)
   - 🔜 Cave floor tiles (stone, dirt, gravel)
   - 🔜 Cave wall tiles (with vertical height)
   - 🔜 Implement isometric TileMap
   - 🔜 Add collision for walls
   - 🔜 Test depth sorting with objects

### Phase 3: Isometric Gameplay
**Priority**: Core Isometric Features

1. **Movement & Physics**
   - 8-directional movement (WASD)
   - Click-to-move (optional, like Diablo)
   - Collision with walls and obstacles
   - Smooth pathfinding
   - Running/walking toggle

2. **Combat System**
   - Click-to-attack or hotkey abilities
   - Melee attack range and targeting
   - Ranged attacks (if applicable)
   - Damage and health system
   - Enemy AI and pathfinding

3. **Level Design**
   - Interconnected cave rooms
   - Corridors and passages
   - Doors and transitions
   - Hidden areas and secrets
   - Proper depth layering

### Phase 4: Exploration & Content
**Priority**: Game World

1. **Cave Generation**
   - Hand-crafted cave layouts (or procedural)
   - Room variety (small, large, multi-level)
   - Environmental storytelling
   - Loot placement
   - Enemy spawns

2. **Environmental Features**
   - Interactive objects (chests, doors)
   - Stalactites and stalagmites
   - Crystal formations
   - Lighting sources (torches, crystals)
   - Ambient darkness with local lights

3. **Items & Pickups**
   - Health potions
   - Equipment/weapons
   - Collectibles
   - Quest items
   - Inventory system

### Phase 5: Polish & Systems
**Priority**: Game Feel

1. **Visual Polish**
   - Particle effects (dust, sparkles)
   - Screen effects (damage flash, darkness)
   - Smooth animations
   - Proper shadows
   - Lighting system

2. **UI/UX**
   - Health/mana bars
   - Inventory interface
   - Character stats
   - Minimap (optional)
   - Menu system

3. **Audio**
   - Ambient cave sounds
   - Footstep sounds
   - Combat sounds
   - Music (atmospheric cave theme)
   - UI feedback sounds

### Phase 6: Testing & Release
**Priority**: Quality & Deployment

1. **Playtesting**
   - Balance adjustments
   - Bug fixes
   - Performance optimization
   - Difficulty tuning

2. **Packaging**
   - Build for target platforms
   - Create installer/packaging
   - Documentation

## 🎨 Isometric Asset Creation Strategy

### Isometric Tiles (Using Blender MCP)
- **Tile Dimensions**: 64x32 pixels (2:1 ratio)
- **Wall Height**: 64-96 pixels (includes vertical component)
- **Perspective**: 26.565° isometric angle
- **Lighting**: Consistent directional light
- **Style**: Dark cave aesthetic with depth

**Process**:
1. Model tile in Blender (floor, wall sections)
2. Set up isometric camera in Blender
3. Render to sprite sheet
4. Import into Godot as tileset
5. Configure collision shapes

### Character Sprites
- **Directions**: 8 directions (or 4 with horizontal flip)
- **Animations**: Idle, walk, attack, hurt, death
- **Resolution**: Match tile scale (approx 64x64 base)
- **Style**: Visible against dark cave backgrounds

**Method 1**: Blender 3D → 2D render
  - Create 3D character model
  - Render from 8 isometric angles
  - Export animation frames
  
**Method 2**: Manual pixel art/sprites
  - Create in 2D image editor
  - Ensure consistent perspective
  - Export animation sequences

### Asset Organization
  - OpenGameArt.org
  - itch.io
  - Kenney.nl (free assets)

### Tilesets
- Design modular cave tiles
- Create variations for visual diversity
- Organize in Godot's TileMap system

### UI Elements
- Minimalist design
- Cave/exploration theme
- High contrast for visibility

## 🔧 MCP-Assisted Development Patterns

### Creating New Scenes (via Godot MCP)
```
"Create a new scene called PlayerCharacter with a CharacterBody2D root node"
"Add a Sprite2D and CollisionShape2D as children"
"Set the collision shape to a capsule"
```

### Generating Assets (via Blender MCP)
```
"Create a simple character model for a cave explorer"
"Add a headlamp to the model"
"Render the character from a 45-degree angle"
```

### Managing Project (via Filesystem/Git MCP)
```
"Create a new folder structure: scenes/player, scenes/enemies, scenes/levels"
"Commit current changes with message: 'Add player movement system'"
```

## 📁 Project Structure

```
cave-crawler/
├── assets/
│   ├── sprites/          # Character and object sprites
│   ├── tilesets/         # Cave environment tiles
│   ├── audio/            # Music and sound effects
│   └── fonts/            # UI fonts
├── scenes/
│   ├── player/           # Player-related scenes
│   ├── enemies/          # Enemy types
│   ├── levels/           # Level scenes
│   ├── ui/               # UI components
│   └── test_scene.tscn   # ✅ Initial test scene
├── scripts/
│   ├── player/           # Player scripts
│   ├── enemies/          # Enemy AI scripts
│   └── systems/          # Game systems (camera, generation, etc.)
├── bin/                  # Godot engine
├── project.godot         # ✅ Project configuration
└── Documentation/
    ├── MCP_SERVERS_SUMMARY.md
    ├── BLENDER_MCP_SETUP.md
    └── This file
```

## 🎮 Core Game Loop

1. Player spawns in cave entrance
2. Explore cave rooms
3. Avoid hazards and enemies
4. Collect items and upgrades
5. Unlock new areas with abilities
6. Reach cave depths / boss
7. Escape back to surface

## 🚀 Immediate Next Steps

1. **Design Player Sprite**
   - Sketch basic character design
   - Create in Blender or 2D tool
   - Export to `assets/sprites/player.png`

2. **Implement Player Movement**
   - Open `test_scene.tscn` in Godot
   - Add CharacterBody2D for player
   - Write movement script
   - Test and iterate

3. **Create Cave Tileset**
   - Design modular cave tiles
   - Create variations (corners, platforms, etc.)
   - Import into Godot TileMap

4. **Build First Test Level**
   - Use TileMap to create small cave area
   - Add player spawn point
   - Test movement and collisions

## 🎯 Success Metrics

- ✅ MCP servers operational (Godot, Blender, Git, Filesystem)
- ✅ Test scene created and verified
- ⏭️ Player character moving smoothly
- ⏭️ Cave environment rendered
- ⏭️ Basic game loop functional
- ⏭️ First playable level complete

## 🔄 Development Approach

### Use MCP For:
- Creating scenes and nodes
- Generating 3D assets in Blender
- Managing project files
- Version control operations
- Rapid prototyping

### Handle Manually:
- Fine-tuning gameplay feel
- Art direction decisions
- Level design creativity
- Playtesting feedback
- Final polishing touches

## 📝 Notes

- **Architecture**: Keep scenes modular for reusability
- **Performance**: Profile regularly, optimize early
- **Scope**: Start small, iterate quickly
- **Feedback**: Playtest often, adjust based on feel
- **Assets**: Prioritize programmer art initially, polish later

---

**Status**: Ready to begin Phase 2 - Game Foundation
**Last Updated**: October 27, 2025
**Branch**: 001-mcp-dev-tools

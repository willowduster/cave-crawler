# Cave Crawler - Project Constitution & Development Plan

## 🎯 Project Overview

**Cave Crawler** is a 2D cave exploration game built with Godot 4.5.1, utilizing AI-powered Model Context Protocol (MCP) servers for accelerated development.

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

### Phase 2: Game Foundation 🔄 NEXT
**Priority**: Core Mechanics

1. **Player Character**
   - Create player sprite/model
   - Implement basic movement (WASD/arrows)
   - Add physics (gravity, collision)
   - Implement jump mechanics
   - Add animation states (idle, walk, jump, fall)

2. **Camera System**
   - Follow player smoothly
   - Set boundaries
   - Add screen shake for impacts

3. **Basic Cave Environment**
   - Create tilemap system
   - Design cave tiles (walls, floors, platforms)
   - Implement collision layers
   - Add background parallax layers

### Phase 3: Cave Generation
**Priority**: Procedural Systems

1. **Level Structure**
   - Cave layout generation (procedural or hand-crafted)
   - Room connections
   - Vertical and horizontal navigation
   - Safe spawn points

2. **Environmental Hazards**
   - Spikes
   - Falling rocks
   - Water/lava pools
   - Darkness/lighting system

### Phase 4: Exploration Mechanics
**Priority**: Gameplay Feel

1. **Player Abilities**
   - Double jump / dash
   - Wall climbing
   - Grappling hook
   - Light source (torch/lantern)

2. **Items & Pickups**
   - Health restoration
   - Ability upgrades
   - Collectibles
   - Keys/access items

### Phase 5: Content & Polish
**Priority**: Game Loop

1. **Enemies & Obstacles**
   - Basic enemy AI
   - Enemy types and behaviors
   - Damage system
   - Death and respawn

2. **UI/UX**
   - Health display
   - Inventory system
   - Minimap
   - Menu system

3. **Audio**
   - Background music
   - Sound effects
   - Ambient cave sounds

### Phase 6: Testing & Release
**Priority**: Quality & Deployment

1. **Playtesting**
   - Balance adjustments
   - Bug fixes
   - Performance optimization

2. **Packaging**
   - Build for target platforms
   - Create installer/packaging
   - Documentation

## 🎨 Asset Creation Strategy

### 2D Sprites
- **Method 1**: Create in Blender, render to sprites
  - Use Blender MCP to generate 3D models
  - Render from fixed camera angle
  - Export as PNG sequences
  
- **Method 2**: Manual creation
  - Use any 2D image editor
  - Save to `assets/` folder
  - Import into Godot via Godot MCP

- **Method 3**: Asset stores
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

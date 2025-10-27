<!--
Sync Impact Report:
Version: 1.1.0 → 1.2.0
Added critical gameplay systems for complete Diablo II-style experience
New principles added:
  - XI. Inventory & Storage Systems
  - XII. Enemy AI & Elite Modifiers
  - XIII. Death & Penalty Systems
  - XIV. Procedural Generation
  - XV. Economy & Trading
Expanded sections:
  - RPG Design Pillars now includes: Inventory Management, AI Behavior, 
    Death Mechanics, World Generation, Economy Systems
Templates requiring updates: ⚠ pending alignment with expanded gameplay systems
-->

# Cave Crawler Constitution

## Core Principles

### I. Scene-Component Architecture (NON-NEGOTIABLE)
**All game entities MUST follow Godot's scene-component pattern.**

- Each game entity (player, enemy, item, etc.) is a reusable scene
- Scenes compose smaller components via inheritance or composition
- No monolithic god-objects; prefer small, focused scripts
- Scenes MUST be independently testable and instantiable

**Rationale**: Maintains Godot best practices, enables parallel development, and ensures 
reusability across single-player and multiplayer modes.

### II. Network Authority First
**Multiplayer architecture MUST establish clear authority for all synchronized state.**

- Every networked entity declares authority (server/client)
- Server is authoritative for game logic, combat, and world state
- Client authority only for local prediction and cosmetic effects
- Input validation MUST occur server-side
- No trust-the-client for gameplay-critical decisions

**Rationale**: Prevents cheating, ensures consistent game state, and simplifies 
conflict resolution in multiplayer scenarios.

### III. Separation of Game Logic and Presentation
**Game logic MUST be decoupled from visual/audio presentation.**

- Core game systems (combat, inventory, progression) are independent scripts
- Rendering, particles, sounds react to game state changes via signals
- Headless server mode MUST be possible without graphics/audio nodes
- Game state serializable for save/load and network sync

**Rationale**: Enables automated testing, dedicated servers, and easier balancing 
without touching presentation code.

### IV. Test-Driven Development
**Critical systems MUST have automated tests before implementation.**

- Write GUT (Godot Unit Test) tests for game logic first
- Combat calculations, inventory systems, progression mechanics require tests
- Integration tests for multiplayer synchronization
- Visual-only features may skip tests, but logic never

**Rationale**: Game bugs are costly and break player experience; tests catch 
regressions early and document expected behavior.

### V. Performance Budget Compliance
**All features MUST respect performance budgets for target platforms.**

- Target: 60 FPS on mid-range hardware (2019+)
- Network tick rate: 20Hz minimum, 30Hz target
- Max network bandwidth: 128 kbps per client
- Scene load times: <2 seconds for dungeon levels
- Profile before optimizing, but design with constraints in mind

**Rationale**: Multiplayer games are performance-sensitive; maintaining smooth 
gameplay is critical for player retention.

### VI. Data-Driven Design
**Game content MUST be data-driven, not hardcoded.**

- Use Godot Resources for items, enemies, abilities, levels
- JSON or custom resources for configuration
- No magic numbers in code; use constants or config files
- Mod-friendly: external data should be easily adjustable
- Version control friendly formats (text-based when possible)

**Rationale**: Enables rapid iteration, modding support, and allows designers 
to work independently of programmers.

### VII. Graceful Degradation
**Systems MUST handle network failures and edge cases gracefully.**

- Timeout detection and reconnection logic required
- Clear error messages for players (no silent failures)
- Save player progress locally; sync when connection restored
- Offline mode with bot teammates where applicable
- No crashes from network errors

**Rationale**: Internet connections drop; the game should recover gracefully 
rather than frustrate players with lost progress.

### VIII. Character Progression (Diablo II-style)
**Character advancement MUST follow deterministic, build-focused progression.**

- Multiple character classes with distinct playstyles and skill trees
- Level-based progression (experience points for kills/quests)
- Skill points allocated manually (1 point per level)
- Skill trees with prerequisites and synergies
- Stat points distributed manually (strength, dexterity, vitality, energy)
- Permanent choices: no free respecs (respec tokens rare/expensive)
- Level cap defined (99 in D2, adjust as needed)

**Rationale**: Meaningful character building decisions create replayability and 
distinct character identities; permanence adds weight to choices.

### IX. Loot System Design
**Item drops MUST create excitement through randomization and rarity tiers.**

- Rarity tiers: Normal (white), Magic (blue), Rare (yellow), Set (green), 
  Unique (gold), Runewords (orange/custom)
- Randomized item generation with affixes (prefixes/suffixes)
- Server-authoritative loot generation and validation
- Personal loot per player (no kill-stealing loot)
- Smart loot: increased chance for class-appropriate items
- Unique items with fixed stats and special properties
- Set items that grant bonuses when worn together
- Runeword system: socketable items + rune combinations = powerful effects
- Item level (ilvl) determines possible affixes
- Gambling/crafting systems for deterministic progression

**Rationale**: Diablo II's loot psychology drives engagement; randomization creates 
"just one more run" gameplay loop while maintaining fairness in multiplayer.

### X. Combat Mechanics
**Combat MUST be fast-paced, skill-based, and rewarding.**

- Action combat with hitbox-based damage (no tab-targeting)
- Attack rating vs. defense for hit chance calculation
- Damage types: Physical, Fire, Cold, Lightning, Poison, Magic
- Elemental resistances cap at 75% (or similar balance point)
- Life and mana as primary resources
- Potion system: instant healing but limited inventory slots
- Crowd control effects: slow, stun, freeze, knockback
- Monster immunities to force build diversity
- Attack speed and cast speed breakpoints (frame-based)
- Life/mana leech mechanics for sustain
- Critical strikes and crushing blow for burst damage
- Movement speed affects combat mobility and farming efficiency

**Rationale**: Diablo II's combat is tested and beloved; fast feedback loops and 
build variety keep combat engaging over hundreds of hours.

### XI. Inventory & Storage Systems
**Inventory MUST use grid-based Tetris-style management with meaningful constraints.**

- Grid-based inventory (e.g., 10x4 character inventory)
- Items occupy multiple grid cells based on size (1x2 sword, 2x3 armor, etc.)
- Inventory tetris creates strategic decisions on what to keep
- Personal stash (expandable via tabs or gold investment)
- Shared stash across characters on same account
- Town portals return to exact dungeon location (one-time use)
- Gold has weight/stacks (encourages banking)
- Potion belt for quick access (4-6 slots)
- Item pickup: manual click (no auto-pickup spam)
- Item comparison tooltips show stat differences

**Rationale**: Grid inventory creates engaging mini-game and prevents unlimited 
hoarding; shared stash enables twinking and account progression.

### XII. Enemy AI & Elite Modifiers
**Enemy behavior MUST scale from simple to complex, with modifiers creating variety.**

- Basic AI: pathfinding, aggro range, simple attack patterns
- Elite/Champion monsters spawn with random modifiers
- Modifier pool: Extra Strong, Extra Fast, Cursed, Fire Enchanted, Lightning 
  Enchanted, Cold Enchanted, Mana Burn, Spectral Hit, Stone Skin, Multiple Shot
- Bosses have unique mechanics and attack patterns
- Monster packs have social behavior (buff allies, coordinated attacks)
- Immunities on Hell difficulty (force build diversity)
- AI difficulty scales by game difficulty (more aggressive in Hell)
- Monster telegraphing for dodgeable attacks

**Rationale**: Diablo II's modifier system creates endless variety from limited 
monster types; elite packs are memorable challenges.

### XIII. Death & Penalty Systems
**Death MUST have consequences but not be punishing enough to quit.**

- Softcore mode: lose 10% experience (cannot de-level), corpse run to retrieve items
- Hardcore mode: permadeath, character moves to "graveyard" (cannot play again)
- Corpse mechanics: body remains at death location with all equipped items
- Multiple deaths: new corpse, previous corpse items drop on ground
- Town resurrect: safe spawn, must retrieve body from dungeon
- Resurrection in party: ally can resurrect at their location
- Experience debt: no negative exp, but harder to level after multiple deaths
- Hardcore death consequences: character name displayed in Hall of Fallen Heroes

**Rationale**: D2's corpse run creates tension without excessive frustration; 
hardcore mode offers ultimate stakes for skilled players.

### XIV. Procedural Generation
**Dungeon layouts MUST balance randomization with hand-crafted quality.**

- Seed-based generation for reproducibility (within same game session)
- Tileset-based assembly with hand-crafted chunks
- Guaranteed critical path (entrance → exit always connected)
- Randomized side rooms and optional areas (20-40% of dungeon)
- Fixed room types: boss arenas, treasure rooms, event rooms
- Monster density formulas based on room size and difficulty
- Exit/entrance placement with minimum distance requirement
- Waypoints in fixed zones but slightly randomized position
- Item placement: predetermined loot points + random containers
- Each dungeon level has visual theme variety (3-5 tileset variants)

**Rationale**: Pure random is chaotic; curated chunks maintain quality while 
procedural generation ensures replayability.

### XV. Economy & Trading
**Economy MUST support player trading while preventing exploitation.**

- Gold is primary currency (drops from enemies, vendors)
- Gold has no level requirement but has weight (bank storage needed)
- Item trading: player-to-player direct trade window
- Trade window: both players confirm, no bait-and-switch
- No auction house (encourages social interaction like D2)
- Vendor prices scale with character level and item quality
- Vendor buyback: last 8-10 items sold retrievable
- Gambling: pay fixed price for random identified item
- Gold sinks: respecs, crafting materials, stash tabs, gambling
- Economy balance: high-end items retain value through rarity
- Bound items: quest rewards are account-bound (prevent twinking exploits)

**Rationale**: D2's organic trading creates vibrant economy; scarcity and 
trust-based trading builds community.

## RPG Design Pillars

### Character Classes and Skills
**Implementation Requirements:**
- Minimum 3 character classes at launch (expand to 5-7 over time)
- Each class has 3 skill trees with 8-10 skills each
- Skill point maximum: 20 points per skill
- Skill synergies MUST be documented and balanced
- Skills scale with: skill level, character stats, +skills equipment
- No auto-attack spam: every attack costs mana or resource
- Cooldowns minimal or absent (resource management primary limiter)

**Data Structure:**
- Skills defined as Godot Resources
- JSON schema for skill trees and dependencies
- Formula system for damage/effect scaling
- Tooltips auto-generate from skill data

### Loot Generation System
**Implementation Requirements:**
- Loot table system with weighted randomization
- Affix pool per item type and ilvl
- Magic find (MF%) stat increases rare drop chance
- Boss-specific unique drop tables
- Ladder-only items for seasonal content
- Trade economy considerations (items tradeable by default)
- Item filter/highlighting for quality-of-life

**Drop Rate Philosophy:**
- Normal items: 60% of drops
- Magic items: 30% of drops
- Rare items: 8% of drops
- Set/Unique items: 2% of drops (adjust for endgame)
- Build-defining uniques: extremely rare (<0.1%)

**Data Structure:**
- Item base types as Resources (weapons, armor, accessories)
- Affix database with stat ranges
- Unique/Set items as individual Resources with lore
- Rune system with combination lookup table

### Combat Formulas
**Damage Calculation (server-authoritative):**
```
Hit Chance = AttackRating / (AttackRating + DefenseRating * 2) * 100
Physical Damage = Base * (1 + EnhancedDamage%) * (1 - EnemyPhysicalResist%)
Elemental Damage = Base * (1 + ElementalDamage%) * (1 - EnemyElementalResist%)
Final Damage = (Physical + Elemental) * CritMultiplier
```

**Resource Management:**
- Mana regeneration: base + mana-per-second gear
- Life leech: % of physical damage dealt
- Potion cooldown: 0.5 seconds between uses
- Instant healing: no heal-over-time (keeps combat fast)

**Balance Targets:**
- Early game (levels 1-20): 5-10 enemies per pull
- Mid game (levels 21-50): 10-20 enemies per pull
- Endgame (levels 51+): 20-40 enemies per pull
- Boss fights: 30-90 seconds for balanced builds

### Progression Milestones
**Level Tiers:**
- Normal difficulty: levels 1-30
- Nightmare difficulty: levels 30-60
- Hell difficulty: levels 60-99

**Itemization Tiers:**
- Early (1-20): Normal items with basic affixes
- Mid (21-50): Magic/Rare items, first Set pieces
- Late (51-75): Rare/Set items, Runewords
- Endgame (76-99): Unique hunting, perfect rolls, PvP builds

### Inventory Management
**Implementation Requirements:**
- Grid system: 2D array data structure (width × height cells)
- Item dimensions stored in ItemResource (1x1 to 2x4 max)
- Drag-and-drop with rotation support (right-click rotates)
- Auto-stacking for stackable items (potions, runes, gems)
- Visual feedback: valid placement (green), invalid (red)
- Quick-move functionality (Ctrl+Click to stash/inventory swap)
- Gold auto-pickup when inventory has space
- Item comparison on hover (current equipped vs. potential)

**Stash Design:**
- Shared stash: 3 tabs minimum (expandable to 5-7)
- Each tab: 10x10 grid (larger than inventory)
- Character-specific stash: 1 tab (8x8 grid) for HC/SC separation
- Stash search/filter functionality for large collections
- Tab naming for organization

**Data Structure:**
- InventoryGrid Resource with 2D boolean occupancy array
- ItemStack class: item reference + position + rotation
- Serialization for save/load and network sync

### Enemy AI & Behavior
**Implementation Requirements:**
- State machine AI: Idle → Patrol → Chase → Attack → Flee (if low HP)
- Pathfinding: Godot Navigation2D/3D for dungeon traversal
- Aggro system: vision cone + noise detection + proximity
- Attack patterns: melee (3 variants), ranged (2 variants), caster (5+ spells)
- Elite modifier application: stats multipliers + special abilities
- Boss phases: 3 phases minimum for endgame bosses

**Elite Modifier Effects:**
- Extra Strong: +50% physical damage
- Extra Fast: +50% movement and attack speed
- Fire/Cold/Lightning Enchanted: +50% elemental damage, death explosion
- Mana Burn: drains mana on hit, dangerous for casters
- Spectral Hit: 50% chance attacks ignore defense
- Stone Skin: +80% physical resistance
- Multiple Shot: ranged attacks split into 3 projectiles

**AI Complexity Tiers:**
- Tier 1 (Trash mobs): Simple chase and attack
- Tier 2 (Elites): Modifiers + flanking behavior
- Tier 3 (Bosses): Unique mechanics, summoning, area denial

**Data Structure:**
- EnemyResource: base stats, AI tier, available modifiers
- ModifierResource: stat changes, visual effects, special abilities
- Boss phase scripts with custom attack sequences

### Death Mechanics
**Implementation Requirements:**
- Death event triggers: HP reaches 0
- Softcore: create corpse entity at death location with all items
- Hardcore: character locked, display death screen with stats
- Experience penalty calculation: current_exp * 0.10 (capped at current level)
- Corpse persistence: remains until retrieved or new death
- Multiple corpses: previous corpse items drop as ground loot
- Resurrection timer: 5 second respawn delay in town
- Death statistics: track per character (total deaths, hardcore deaths)

**Corpse Retrieval:**
- Corpse location marked on map
- Player spawns naked in town (no equipped items)
- Portal available to return to death location
- Corpse interaction: instant equipment retrieval
- Multiplayer: corpse can be protected by allies

**Hardcore Mode:**
- Character creation flag: hardcore = true (irreversible)
- Death triggers: save to "fallen heroes" list
- Fallen heroes display: name, level, class, time played, cause of death
- Character viewable but not playable
- Items non-transferable (prevent death farming)

**Data Structure:**
- Corpse scene: stores ItemStack array, player appearance, location
- DeathEvent: timestamp, location, killer, exp lost
- HardcoreStats: death leaderboard data

### Procedural Generation System
**Implementation Requirements:**
- Dungeon builder: chunk-based assembly algorithm
- Chunk library: 20-30 hand-crafted rooms per tileset
- Chunk types: entrance, exit, hallway, large room, treasure room, boss arena
- Connection rules: chunk entrances/exits must align
- Generation constraints:
  - Minimum path length: entrance to exit (15-25 rooms)
  - Maximum dead ends: 30% of total rooms
  - Treasure room frequency: 1 per 10 rooms
  - Elite pack density: 2-3 per main path

**Seed System:**
- Seed generated on dungeon entry (or preset for testing)
- Seed determines: layout, monster spawns, chest locations
- Seed does NOT determine: item rolls (separate RNG)
- Seed shared in multiplayer (host generates, clients sync)

**Tileset Themes:**
- Catacombs: stone walls, torches, crypts
- Caves: natural rock, water pools, stalagmites
- Ruins: ancient architecture, vines, collapsed sections
- Hell: lava, demonic decorations, fire effects

**Monster Placement:**
- Pack spawners: defined points in chunks (3-5 per room)
- Pack size: 4-8 monsters for trash, 1 elite + 2-4 minions
- Boss spawns: center of boss arena chunks
- Roaming spawns: 10% of monsters patrol between rooms

**Data Structure:**
- DungeonChunk Resource: tile layout, spawn points, connections
- ChunkConnection: north/south/east/west exit definitions
- GenerationRules: constraints, weights, theme mappings
- DungeonSeed: integer seed + generation parameters

### Economy & Trading Systems
**Implementation Requirements:**
- Gold system: stored as integer (max: 9,999,999 or similar cap)
- Gold weight: every 10,000 gold = 1 inventory slot (encourages banking)
- Vendor stock: random refreshing inventory (changes per visit or timer)
- Vendor pricing formula:
  ```
  Buy_Price = Base_Value * Quality_Multiplier * (1 + Player_Level * 0.05)
  Sell_Price = Buy_Price * 0.10 (vendors pay 10% of value)
  ```

**Trading Interface:**
- Trade request: player initiates, target accepts
- Trade window: 2 panels (your items + their items + gold fields)
- Lock-in mechanism: both click "Accept" then "Confirm" (prevents scams)
- Trade history: log last 20 trades (item, partner, timestamp)
- Trade chat channel: dedicated for trading requests

**Gambling System:**
- Gambler NPC in town: sells unidentified items
- Fixed prices by item type: 5,000g ring, 50,000g armor, etc.
- Gambling results: weighted toward normal/magic, rare chance
- Gambling can yield uniques (very rare, <0.1%)
- Gambling ilvl = player level (determines possible affixes)

**Gold Sinks:**
- Respec token: 100,000 gold + rare materials
- Stash tab expansion: 50,000g per tab (max 7 tabs)
- Crafting attempts: 10,000-50,000g per craft
- Gambling: primary gold sink for endgame
- Vendor repairs: item durability costs gold (if implemented)

**Trade Economy Balance:**
- High runes: ultra-rare, become de facto currency
- Perfect rolled items: retain value through scarcity
- Common uniques: quickly lose value (prevent inflation)
- Ladder resets: seasonal economy wipes for fresh starts

**Anti-Exploit Measures:**
- Trade value logging: detect suspicious trades (1 gold for unique)
- Item duplication detection: unique item IDs, server-side validation
- Gold drop caps: prevent infinite gold exploits
- Trading level requirement: must be level 10+ to trade

**Data Structure:**
- TradeSession: two player references, item arrays, gold amounts, lock states
- VendorStock: generated inventory, prices, refresh timer
- GoldTransaction: log for economy monitoring
- ItemValue calculation: base value + affix values

## Technical Standards

### Technology Stack
- **Engine**: Godot 4.x (latest stable)
- **Language**: GDScript for gameplay, C# for performance-critical systems (optional)
- **Networking**: Godot's High-Level Multiplayer API with ENet
- **Testing**: GUT (Godot Unit Test) framework
- **Version Control**: Git with LFS for binary assets

### Code Quality Requirements
- All scripts MUST have typed GDScript (static typing enforced)
- Public functions/classes MUST have documentation comments
- Maximum function length: 50 lines (extract helpers if longer)
- Maximum script length: 300 lines (split into components if longer)
- Follow Godot GDScript style guide naming conventions

### Asset Standards
- Sprites: PNG format, power-of-2 dimensions preferred
- Audio: OGG Vorbis format for music, WAV for short SFX
- 3D Models: GLTF 2.0 format (if applicable)
- All assets MUST include attribution in `CREDITS.md`
- Asset size limit: 5MB per file (use compression/atlases)

## Multiplayer Architecture

### Network Synchronization
- Use Godot's RPC system for actions, MultiplayerSynchronizer for state
- Synchronize only essential state (position, health, inventory changes)
- Client-side prediction for player movement with server reconciliation
- Snapshot interpolation for smooth remote player movement
- Delta compression for bandwidth optimization

### Security Requirements
- Never trust client input for gameplay logic
- Validate all RPCs on the server
- Rate-limit client requests to prevent spam/DoS
- Encrypt authentication tokens
- No client-side storage of sensitive data (passwords, payment info)

### Scalability Design
- Support 4-8 players per dungeon instance (initial target)
- Lobby system for matchmaking and party formation
- Instanced dungeons (no shared world initially)
- Prepared for horizontal scaling (multiple server instances)

## Development Workflow

### Feature Development Process
1. **Specification**: Write feature spec in `.specify/specs/`
2. **Design**: Create scene structure and architecture plan
3. **Test**: Write GUT tests for game logic components
4. **Implement**: Build feature following TDD red-green-refactor
5. **Playtest**: Manual testing in both single and multiplayer modes
6. **Review**: Code review focusing on performance and multiplayer sync
7. **Document**: Update relevant docs and tutorial content

### Quality Gates
- All tests MUST pass before merging
- No performance regressions (profiling required for systems changes)
- Multiplayer testing required for networked features
- Code review approval from at least one other developer
- Documentation updated for player-facing features

### Branch Strategy
- `main`: Stable, playable builds only
- `develop`: Integration branch for features
- `feature/*`: Individual feature branches
- `hotfix/*`: Critical bug fixes

## Governance

### Amendment Process
This constitution can be amended through:
1. Proposal documented in a GitHub issue with rationale
2. Discussion period (minimum 3 days for major changes)
3. Approval from project maintainers
4. Version increment and update of dependent templates
5. Migration plan if changes affect existing code

### Compliance and Review
- All pull requests MUST be reviewed against these principles
- Monthly architecture reviews to ensure alignment
- Performance budgets checked in CI/CD pipeline
- Multiplayer sync issues are treated as critical bugs

### Versioning Policy
- **MAJOR**: Breaking changes to architecture or core principles
- **MINOR**: New principles added or significant expansions
- **PATCH**: Clarifications, typo fixes, minor refinements

### Conflict Resolution
When principles conflict (e.g., performance vs. code clarity):
1. Prioritize principles in order: Network Authority > Performance Budget > others
2. Document the tradeoff decision in code comments or ADR
3. Revisit in next architecture review if pattern emerges

### Gameplay Balance Philosophy
When balancing RPG systems:
1. **Player agency over RNG**: deterministic systems preferred where possible
2. **Build diversity**: no single "best build" (buff weak, nerf outliers sparingly)
3. **Respect player time**: drop rates frustrating but not insulting
4. **Multiplayer fairness**: no pay-to-win, cosmetics only for monetization
5. **Diablo II as North Star**: when uncertain, reference D2 design decisions

### System Interaction Priorities
When systems conflict in design:
1. **Network Authority** > everything (no client trust for gameplay)
2. **Performance** > visual fidelity (smooth gameplay essential)
3. **Player progression** > perfect balance (fun > mathematically optimal)
4. **Replayability** > first-time experience (design for 100+ hours)
5. **Social features** > solo optimization (multiplayer is core)

**Version**: 1.2.0 | **Ratified**: 2025-10-26 | **Last Amended**: 2025-10-26

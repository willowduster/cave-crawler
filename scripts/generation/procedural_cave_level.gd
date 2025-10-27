extends Node2D

## Procedurally generated cave level
## Uses CaveGenerator to create layout, then builds the scene

const CaveGenerator = preload("res://scripts/generation/cave_generator.gd")
const DebugConsole = preload("res://scripts/ui/debug_console.gd")
const AStarPathfinder = preload("res://scripts/pathfinding/astar_pathfinder.gd")

@onready var cave_generator = CaveGenerator.new()
@onready var debug_console: DebugConsole = null
@onready var pathfinder: AStarPathfinder = AStarPathfinder.new()

const TILE_SIZE = 64  # SNES-style higher resolution tiles

# Texture paths - will be loaded at runtime
var texture_paths = {
	"floor": "res://assets/textures/cave_floor_tile.png",
	"floor_moss": "res://assets/textures/cave_floor_moss.png",
	"floor_wet": "res://assets/textures/cave_floor_wet.png",
	"water": "res://assets/textures/water_tile.png",
	"lava": "res://assets/textures/lava_tile.png",
}

var prop_texture_paths = {
	"campfire": "res://assets/textures/campfire.png",
	"crystal_blue": "res://assets/textures/crystal_blue.png",
	"crystal_purple": "res://assets/textures/crystal_purple.png",
	"crystal_green": "res://assets/textures/crystal_green.png",
	"treasure": "res://assets/textures/treasure_chest.png",
	"rock": "res://assets/textures/rock_pile.png",
	"mushrooms": "res://assets/textures/mushrooms.png",
	"stalagmite": "res://assets/textures/stalagmite.png",
	"bones": "res://assets/textures/bones.png",
	"torch": "res://assets/textures/torch.png",
}

var textures = {}
var prop_textures = {}

var cave_data: Dictionary
var floor_rects: Array = []
var wall_bodies: Array = []
var obstacles: Array = []

func _init() -> void:
	# Load textures at runtime
	for key in texture_paths:
		textures[key] = load(texture_paths[key])
	for key in prop_texture_paths:
		prop_textures[key] = load(prop_texture_paths[key])

func _ready() -> void:
	# Add generator as child
	add_child(cave_generator)
	cave_generator.generation_complete.connect(_on_generation_complete)
	
	# Configure generator - more structured cave-like generation
	cave_generator.width = 150
	cave_generator.height = 120
	cave_generator.fill_probability = 0.48  # More walls for tighter spaces
	cave_generator.smoothing_iterations = 4  # Less smoothing for more irregular caves
	
	# Generate the cave
	print("Generating procedural cave...")
	cave_data = cave_generator.generate_cave()
	
	# Setup pathfinder with cave grid
	print("Setting up pathfinding...")
	pathfinder.setup(cave_data.grid, cave_data.width, cave_data.height)
	
	# Build the visual scene
	_build_cave_visuals()
	
	# Position player at spawn
	await get_tree().process_frame
	_spawn_player()
	
	# Connect pathfinder to player
	await get_tree().process_frame
	_connect_player_pathfinder()
	
	# Setup debug console
	await get_tree().process_frame
	_setup_debug_console()
	
	# Update stats
	_update_stats()

func _setup_debug_console() -> void:
	var console_node = get_node_or_null("DebugConsole")
	if console_node:
		debug_console = console_node as DebugConsole
		print("Debug console found!")
	else:
		print("Warning: Debug console not found")

func _process(_delta: float) -> void:
	if debug_console:
		_update_debug_info()

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_Q:
			# Quit on Q key
			get_tree().quit()
		elif event.keycode == KEY_R or event.is_action_pressed("ui_accept"):
			# Regenerate cave
			regenerate_cave()
		elif event.keycode == KEY_ESCAPE:
			# Quit on ESC
			get_tree().quit()

func regenerate_cave() -> void:
	print("\n=== REGENERATING CAVE ===")
	cave_data = cave_generator.generate_cave()
	_build_cave_visuals()
	_spawn_player()
	_update_stats()
	
	if debug_console:
		debug_console.add_section("regen_notice", "Cave regenerated!", Color.YELLOW)
		await get_tree().create_timer(2.0).timeout
		debug_console.remove_section("regen_notice")

func _spawn_player() -> void:
	var player = get_node_or_null("Player")
	if player:
		var spawn_pos = get_spawn_position()
		player.global_position = spawn_pos
		print("Player spawned at: ", spawn_pos)

func _connect_player_pathfinder() -> void:
	var player = get_node_or_null("Player")
	if player and player.has_method("set_pathfinder"):
		player.set_pathfinder(pathfinder)
		print("Pathfinder connected to player")
	else:
		print("Warning: Could not connect pathfinder to player")

func _update_stats() -> void:
	if not debug_console:
		return
	
	var rooms = cave_data.rooms
	var total_floor_tiles = 0
	for room in rooms:
		total_floor_tiles += room.size()
	
	var stats_text = """Generation Stats:
• Grid: %dx%d
• Rooms: %d
• Floor tiles: %d
• Obstacles: %d
• Visual elements: %d""" % [
		cave_data.width,
		cave_data.height,
		rooms.size(),
		total_floor_tiles,
		obstacles.size(),
		floor_rects.size() + wall_bodies.size()
	]
	
	debug_console.set_stats(stats_text)

func _update_debug_info() -> void:
	var fps = Engine.get_frames_per_second()
	var debug_text = "FPS: %d" % fps
	debug_console.set_debug(debug_text)

func _on_generation_complete(data: Dictionary) -> void:
	print("Generation complete signal received!")

func _build_cave_visuals() -> void:
	print("Building cave visuals...")
	
	# Clear existing visuals
	for rect in floor_rects:
		if is_instance_valid(rect):
			rect.queue_free()
	for wall in wall_bodies:
		if is_instance_valid(wall):
			wall.queue_free()
	for obs in obstacles:
		if is_instance_valid(obs):
			obs.queue_free()
	
	floor_rects.clear()
	wall_bodies.clear()
	obstacles.clear()
	
	# Build floor tiles
	_build_floor_tiles()
	
	# Build wall collisions
	_build_wall_collisions()
	
	# Place obstacles
	_place_obstacles()
	
	print("Cave visuals complete!")
	print("  Floor rects: %d" % floor_rects.size())
	print("  Wall bodies: %d" % wall_bodies.size())
	print("  Obstacles: %d" % obstacles.size())

func _build_floor_tiles() -> void:
	var grid = cave_data.grid
	var width = cave_data.width
	var height = cave_data.height
	
	# Group adjacent floor tiles into larger rectangles for performance
	var visited = []
	visited.resize(height)
	for y in range(height):
		visited[y] = []
		visited[y].resize(width)
		visited[y].fill(false)
	
	for y in range(height):
		for x in range(width):
			if not grid[y][x] and not visited[y][x]:
				# Found unvisited floor tile, try to expand into rectangle
				var rect_width = 1
				var rect_height = 1
				
				# Expand horizontally
				while x + rect_width < width and not grid[y][x + rect_width] and not visited[y][x + rect_width]:
					rect_width += 1
				
				# Expand vertically
				var can_expand = true
				while can_expand and y + rect_height < height:
					for dx in range(rect_width):
						if grid[y + rect_height][x + dx] or visited[y + rect_height][x + dx]:
							can_expand = false
							break
					if can_expand:
						rect_height += 1
				
				# Mark as visited
				for dy in range(rect_height):
					for dx in range(rect_width):
						visited[y + dy][x + dx] = true
				
				# Create floor rect
				_create_floor_rect(x, y, rect_width, rect_height)

func _create_floor_rect(grid_x: int, grid_y: int, grid_width: int, grid_height: int) -> void:
	# Use individual tiles for small areas
	if grid_width <= 2 and grid_height <= 2:
		for dy in range(grid_height):
			for dx in range(grid_width):
				_create_floor_tile(grid_x + dx, grid_y + dy)
	else:
		# For larger areas, create a tiled background
		var tile_bg = Sprite2D.new()
		tile_bg.texture = textures["floor"]
		tile_bg.centered = false
		tile_bg.position = Vector2(grid_x * TILE_SIZE, grid_y * TILE_SIZE)
		
		# Create texture repeat using region
		tile_bg.region_enabled = true
		tile_bg.region_rect = Rect2(0, 0, grid_width * TILE_SIZE, grid_height * TILE_SIZE)
		tile_bg.texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
		
		tile_bg.z_index = -50
		add_child(tile_bg)
		floor_rects.append(tile_bg)

func _create_floor_tile(grid_x: int, grid_y: int) -> void:
	var sprite = Sprite2D.new()
	
	# Randomly choose floor texture (70% normal, 15% moss, 10% wet, 5% other)
	var rand = randf()
	if rand < 0.70:
		sprite.texture = textures["floor"]
	elif rand < 0.85:
		sprite.texture = textures["floor_moss"]
	elif rand < 0.95:
		sprite.texture = textures["floor_wet"]
	else:
		sprite.texture = textures["floor"]
	
	sprite.centered = false
	sprite.position = Vector2(grid_x * TILE_SIZE, grid_y * TILE_SIZE)
	sprite.z_index = -50
	
	add_child(sprite)
	floor_rects.append(sprite)

func _build_wall_collisions() -> void:
	var grid = cave_data.grid
	var width = cave_data.width
	var height = cave_data.height
	
	# Create collision shapes for walls
	# Group adjacent walls for better performance
	var visited = []
	visited.resize(height)
	for y in range(height):
		visited[y] = []
		visited[y].resize(width)
		visited[y].fill(false)
	
	for y in range(height):
		for x in range(width):
			if grid[y][x] and not visited[y][x]:
				# Found wall, expand into rectangle
				var rect_width = 1
				var rect_height = 1
				
				# Expand horizontally
				while x + rect_width < width and grid[y][x + rect_width] and not visited[y][x + rect_width]:
					rect_width += 1
				
				# Expand vertically
				var can_expand = true
				while can_expand and y + rect_height < height:
					for dx in range(rect_width):
						if not grid[y + rect_height][x + dx] or visited[y + rect_height][x + dx]:
							can_expand = false
							break
					if can_expand:
						rect_height += 1
				
				# Mark as visited
				for dy in range(rect_height):
					for dx in range(rect_width):
						visited[y + dy][x + dx] = true
				
				# Create wall collision
				_create_wall_collision(x, y, rect_width, rect_height)

func _create_wall_collision(grid_x: int, grid_y: int, grid_width: int, grid_height: int) -> void:
	var wall = StaticBody2D.new()
	wall.position = Vector2(grid_x * TILE_SIZE, grid_y * TILE_SIZE)
	
	# Collision shape
	var shape = RectangleShape2D.new()
	shape.size = Vector2(grid_width * TILE_SIZE, grid_height * TILE_SIZE)
	
	var collision = CollisionShape2D.new()
	collision.shape = shape
	collision.position = Vector2(grid_width * TILE_SIZE / 2, grid_height * TILE_SIZE / 2)
	wall.add_child(collision)
	
	# Visual rect
	var visual = ColorRect.new()
	visual.size = Vector2(grid_width * TILE_SIZE, grid_height * TILE_SIZE)
	visual.color = Color(0.3, 0.25, 0.2, 1.0)
	wall.add_child(visual)
	
	add_child(wall)
	wall_bodies.append(wall)

func _place_obstacles() -> void:
	# Place random rocks and props on floor tiles
	var rooms = cave_data.rooms
	if rooms.is_empty():
		return
	
	# Place obstacles in each room
	for room in rooms:
		var obstacle_count = max(1, room.size() / 100)  # ~1 per 100 tiles
		
		for i in range(obstacle_count):
			if room.is_empty():
				continue
			
			var tile = room[randi() % room.size()]
			_create_obstacle(tile.x, tile.y)

func _create_obstacle(grid_x: int, grid_y: int) -> void:
	# Choose a random prop texture
	var prop_keys = prop_textures.keys()
	var prop_key = prop_keys[randi() % prop_keys.size()]
	var texture = prop_textures[prop_key]
	
	# Randomize size (0.7x to 1.3x scale)
	var scale_factor = 0.7 + randf() * 0.6
	
	# Create sprite
	var sprite = Sprite2D.new()
	sprite.texture = texture
	sprite.scale = Vector2(scale_factor, scale_factor)
	sprite.position = Vector2(
		grid_x * TILE_SIZE + TILE_SIZE / 2,
		grid_y * TILE_SIZE + TILE_SIZE / 2
	)
	sprite.z_index = 10
	
	# Create collision if it's a solid prop (not decorative)
	var solid_props = ["rock", "stalagmite", "treasure", "campfire"]
	if prop_key in solid_props:
		var obstacle = StaticBody2D.new()
		obstacle.position = sprite.position
		
		# Collision shape - scaled based on sprite
		var collision = CollisionShape2D.new()
		var shape = CircleShape2D.new()
		shape.radius = 20 * scale_factor  # Proportional collision radius
		collision.shape = shape
		
		obstacle.add_child(collision)
		add_child(obstacle)
		obstacles.append(obstacle)
	
	add_child(sprite)
	floor_rects.append(sprite)  # Track for cleanup

func get_spawn_position() -> Vector2:
	var spawn_tile = cave_generator.get_random_floor_position()
	return Vector2(
		spawn_tile.x * TILE_SIZE + TILE_SIZE / 2,
		spawn_tile.y * TILE_SIZE + TILE_SIZE / 2
	)

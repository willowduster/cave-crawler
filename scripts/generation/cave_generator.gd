extends Node
class_name CaveGenerator

## Procedural cave generator using cellular automata
## Generates organic cave layouts with guaranteed connectivity

signal generation_complete(cave_data: Dictionary)

## Grid dimensions
var width: int = 80
var height: int = 60

## Generation parameters
var fill_probability: float = 0.45  # Initial random fill %
var smoothing_iterations: int = 5
var wall_threshold: int = 4  # Neighbors needed to become wall

## Minimum room size (smaller isolated areas are removed)
var min_room_size: int = 20

## Cave data
var grid: Array = []  # 2D array: true = wall, false = floor
var rooms: Array = []  # Connected regions

func _ready() -> void:
	pass

## Generate a new cave
func generate_cave(seed_value: int = -1) -> Dictionary:
	if seed_value != -1:
		seed(seed_value)
	
	print("Starting cave generation...")
	
	# Step 1: Initialize grid with random noise
	_initialize_grid()
	
	# Step 2: Smooth using cellular automata
	for i in range(smoothing_iterations):
		_smooth_iteration()
	
	# Step 3: Identify rooms (connected floor regions)
	_identify_rooms()
	
	# Step 4: Remove small isolated rooms
	_remove_small_rooms()
	
	# Step 5: Connect all remaining rooms
	_connect_rooms()
	
	# Step 6: Final cleanup smoothing
	_smooth_iteration()
	
	print("Cave generation complete!")
	print("  Grid size: %dx%d" % [width, height])
	print("  Rooms found: %d" % rooms.size())
	
	var cave_data = {
		"grid": grid,
		"rooms": rooms,
		"width": width,
		"height": height
	}
	
	generation_complete.emit(cave_data)
	return cave_data

## Initialize grid with random noise
func _initialize_grid() -> void:
	grid.clear()
	grid.resize(height)
	
	for y in range(height):
		grid[y] = []
		grid[y].resize(width)
		
		for x in range(width):
			# Edges are always walls
			if x == 0 or x == width - 1 or y == 0 or y == height - 1:
				grid[y][x] = true
			else:
				# Random fill based on probability
				grid[y][x] = randf() < fill_probability

## Cellular automata smoothing iteration
func _smooth_iteration() -> void:
	var new_grid = []
	new_grid.resize(height)
	
	for y in range(height):
		new_grid[y] = []
		new_grid[y].resize(width)
		
		for x in range(width):
			# Edges remain walls
			if x == 0 or x == width - 1 or y == 0 or y == height - 1:
				new_grid[y][x] = true
				continue
			
			# Count neighboring walls
			var wall_count = _count_walls_around(x, y)
			
			# Apply cellular automata rules
			new_grid[y][x] = wall_count >= wall_threshold
	
	grid = new_grid

## Count walls in 3x3 area around position
func _count_walls_around(x: int, y: int, range_check: int = 1) -> int:
	var count = 0
	
	for dy in range(-range_check, range_check + 1):
		for dx in range(-range_check, range_check + 1):
			# Skip center tile for more organic shapes
			if dx == 0 and dy == 0:
				continue
				
			var nx = x + dx
			var ny = y + dy
			
			# Out of bounds counts as wall
			if nx < 0 or nx >= width or ny < 0 or ny >= height:
				count += 1
			elif grid[ny][nx]:
				count += 1
	
	return count

## Flood fill to identify connected floor regions (rooms)
func _identify_rooms() -> void:
	rooms.clear()
	var visited = []
	visited.resize(height)
	
	for y in range(height):
		visited[y] = []
		visited[y].resize(width)
		visited[y].fill(false)
	
	# Find all connected floor regions
	for y in range(height):
		for x in range(width):
			if not grid[y][x] and not visited[y][x]:
				var room_tiles = _flood_fill(x, y, visited)
				if room_tiles.size() > 0:
					rooms.append(room_tiles)

## Flood fill from starting position
func _flood_fill(start_x: int, start_y: int, visited: Array) -> Array:
	var tiles = []
	var queue = [Vector2i(start_x, start_y)]
	
	while queue.size() > 0:
		var pos = queue.pop_front()
		var x = pos.x
		var y = pos.y
		
		# Bounds check
		if x < 0 or x >= width or y < 0 or y >= height:
			continue
		
		# Already visited or is a wall
		if visited[y][x] or grid[y][x]:
			continue
		
		# Mark as visited and add to room
		visited[y][x] = true
		tiles.append(pos)
		
		# Add neighbors to queue
		queue.append(Vector2i(x + 1, y))
		queue.append(Vector2i(x - 1, y))
		queue.append(Vector2i(x, y + 1))
		queue.append(Vector2i(x, y - 1))
	
	return tiles

## Remove rooms smaller than minimum size
func _remove_small_rooms() -> void:
	for room in rooms:
		if room.size() < min_room_size:
			# Fill small rooms with walls
			for tile in room:
				grid[tile.y][tile.x] = true
	
	# Re-identify rooms after removal
	_identify_rooms()

## Connect all rooms with corridors
func _connect_rooms() -> void:
	if rooms.size() <= 1:
		return
	
	# Sort rooms by size (largest first)
	rooms.sort_custom(func(a, b): return a.size() > b.size())
	
	# Connect each room to the next largest
	for i in range(rooms.size() - 1):
		var room_a = rooms[i]
		var room_b = rooms[i + 1]
		
		# Find closest tiles between rooms
		var closest_a = room_a[0]
		var closest_b = room_b[0]
		var min_dist = INF
		
		for tile_a in room_a:
			for tile_b in room_b:
				var dist = tile_a.distance_to(tile_b)
				if dist < min_dist:
					min_dist = dist
					closest_a = tile_a
					closest_b = tile_b
		
		# Carve corridor between closest tiles
		_carve_corridor(closest_a, closest_b)

## Carve a corridor between two points
func _carve_corridor(start: Vector2i, end: Vector2i) -> void:
	var current = start
	var corridor_width = 3  # Make corridors 3 tiles wide for better flow
	
	# Horizontal then vertical path
	while current.x != end.x:
		_carve_tile(current, corridor_width)
		current.x += 1 if current.x < end.x else -1
	
	while current.y != end.y:
		_carve_tile(current, corridor_width)
		current.y += 1 if current.y < end.y else -1
	
	_carve_tile(current, corridor_width)

## Carve out a tile and surrounding area
func _carve_tile(pos: Vector2i, radius: int = 1) -> void:
	for dy in range(-radius + 1, radius):
		for dx in range(-radius + 1, radius):
			var x = pos.x + dx
			var y = pos.y + dy
			
			if x > 0 and x < width - 1 and y > 0 and y < height - 1:
				grid[y][x] = false

## Get a random floor position (for spawning)
func get_random_floor_position() -> Vector2i:
	if rooms.is_empty():
		return Vector2i(width / 2, height / 2)
	
	# Pick largest room
	var largest_room = rooms[0]
	var tile = largest_room[randi() % largest_room.size()]
	return tile

## Get all floor positions in largest room
func get_spawn_room_tiles() -> Array:
	if rooms.is_empty():
		return []
	return rooms[0]

## Check if position is floor
func is_floor(x: int, y: int) -> bool:
	if x < 0 or x >= width or y < 0 or y >= height:
		return false
	return not grid[y][x]

## Check if position is wall
func is_wall(x: int, y: int) -> bool:
	if x < 0 or x >= width or y < 0 or y >= height:
		return true
	return grid[y][x]

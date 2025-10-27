extends Node
class_name AStarPathfinder

## A* pathfinding for grid-based navigation
## Finds optimal path around obstacles

## Pathfinding grid
var grid: Array = []  # 2D array: true = wall, false = walkable
var width: int = 0
var height: int = 0

## AStar2D node for efficient pathfinding
var astar: AStar2D = null

## Initialize pathfinder with grid data
func setup(cave_grid: Array, grid_width: int, grid_height: int) -> void:
	grid = cave_grid
	width = grid_width
	height = grid_height
	
	# Create AStar2D graph
	astar = AStar2D.new()
	
	print("Setting up pathfinding grid (%dx%d)..." % [width, height])
	
	# Add all walkable tiles as points
	for y in range(height):
		for x in range(width):
			if not grid[y][x]:  # If not a wall
				var point_id = _get_point_id(x, y)
				var position = Vector2(x, y)
				astar.add_point(point_id, position)
	
	# Connect adjacent walkable tiles
	for y in range(height):
		for x in range(width):
			if not grid[y][x]:
				_connect_neighbors(x, y)
	
	print("Pathfinding setup complete! Points: %d" % astar.get_point_count())

## Convert grid coordinates to unique point ID
func _get_point_id(x: int, y: int) -> int:
	return y * width + x

## Convert point ID back to grid coordinates
func _get_grid_pos(point_id: int) -> Vector2i:
	return Vector2i(point_id % width, point_id / width)

## Connect a tile to its walkable neighbors
func _connect_neighbors(x: int, y: int) -> void:
	var point_id = _get_point_id(x, y)
	
	# Check 4 cardinal directions
	var directions = [
		Vector2i(1, 0),   # Right
		Vector2i(-1, 0),  # Left
		Vector2i(0, 1),   # Down
		Vector2i(0, -1)   # Up
	]
	
	for dir in directions:
		var nx = x + dir.x
		var ny = y + dir.y
		
		# Check bounds
		if nx >= 0 and nx < width and ny >= 0 and ny < height:
			# If neighbor is walkable
			if not grid[ny][nx]:
				var neighbor_id = _get_point_id(nx, ny)
				# Connect bidirectionally with cost of 1.0
				astar.connect_points(point_id, neighbor_id, true)

## Find path from start to end (world positions)
## Returns array of Vector2 world positions, or empty array if no path
func find_path(start_pos: Vector2, end_pos: Vector2, tile_size: int = 64) -> Array:
	if astar == null:
		push_error("Pathfinder not initialized! Call setup() first.")
		return []
	
	# Convert world positions to grid coordinates
	var start_grid = world_to_grid(start_pos, tile_size)
	var end_grid = world_to_grid(end_pos, tile_size)
	
	# Validate positions are in bounds
	if not _is_valid_pos(start_grid.x, start_grid.y):
		push_warning("Start position out of bounds: %s" % start_grid)
		return []
	
	if not _is_valid_pos(end_grid.x, end_grid.y):
		push_warning("End position out of bounds: %s" % end_grid)
		return []
	
	# Check if positions are walkable
	if grid[start_grid.y][start_grid.x]:
		push_warning("Start position is a wall: %s" % start_grid)
		return []
	
	if grid[end_grid.y][end_grid.x]:
		push_warning("End position is a wall: %s" % end_grid)
		return []
	
	# Get point IDs
	var start_id = _get_point_id(start_grid.x, start_grid.y)
	var end_id = _get_point_id(end_grid.x, end_grid.y)
	
	# Find path using A*
	var path_points = astar.get_point_path(start_id, end_id)
	
	# Convert grid positions back to world positions
	var world_path = []
	for point in path_points:
		var world_pos = grid_to_world(Vector2i(int(point.x), int(point.y)), tile_size)
		world_path.append(world_pos)
	
	return world_path

## Convert world position to grid coordinates
func world_to_grid(world_pos: Vector2, tile_size: int) -> Vector2i:
	return Vector2i(
		int(world_pos.x / tile_size),
		int(world_pos.y / tile_size)
	)

## Convert grid coordinates to world position (center of tile)
func grid_to_world(grid_pos: Vector2i, tile_size: int) -> Vector2:
	return Vector2(
		grid_pos.x * tile_size + tile_size / 2.0,
		grid_pos.y * tile_size + tile_size / 2.0
	)

## Check if grid position is valid and walkable
func _is_valid_pos(x: int, y: int) -> bool:
	return x >= 0 and x < width and y >= 0 and y < height

## Check if a world position is walkable
func is_walkable(world_pos: Vector2, tile_size: int = 64) -> bool:
	var grid_pos = world_to_grid(world_pos, tile_size)
	if not _is_valid_pos(grid_pos.x, grid_pos.y):
		return false
	return not grid[grid_pos.y][grid_pos.x]

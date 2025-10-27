extends Node2D

# This script builds the isometric cave level on ready
var tilemap: TileMapLayer

func _ready():
	tilemap = $TileMapLayer
	print("Building cave room...")
	build_cave_room()
	print("Cave room complete!")

func build_cave_room():
	# Build a 20x12 cave room with walls
	var floor_count = 0
	var wall_count = 0
	
	# Floor tiles (source_id 0 for floor)
	for x in range(-10, 11):
		for y in range(-6, 7):
			# Use floor tile (source 0, atlas coords 0,0, alternative 0)
			tilemap.set_cell(Vector2i(x, y), 0, Vector2i(0, 0))
			floor_count += 1
	
	# Wall tiles (source_id 1 for walls) around the perimeter
	# Top wall
	for x in range(-10, 11):
		tilemap.set_cell(Vector2i(x, -7), 1, Vector2i(0, 0))
		wall_count += 1
	
	# Bottom wall
	for x in range(-10, 11):
		tilemap.set_cell(Vector2i(x, 7), 1, Vector2i(0, 0))
		wall_count += 1
	
	# Left wall
	for y in range(-6, 7):
		tilemap.set_cell(Vector2i(-11, y), 1, Vector2i(0, 0))
		wall_count += 1
	
	# Right wall
	for y in range(-6, 7):
		tilemap.set_cell(Vector2i(11, y), 1, Vector2i(0, 0))
		wall_count += 1
	
	# Add some internal obstacles
	# Rock cluster 1
	tilemap.set_cell(Vector2i(-5, -2), 1, Vector2i(0, 0))
	tilemap.set_cell(Vector2i(-5, -1), 1, Vector2i(0, 0))
	wall_count += 2
	
	# Rock cluster 2
	tilemap.set_cell(Vector2i(6, 3), 1, Vector2i(0, 0))
	tilemap.set_cell(Vector2i(7, 3), 1, Vector2i(0, 0))
	tilemap.set_cell(Vector2i(6, 4), 1, Vector2i(0, 0))
	wall_count += 3
	
	print("Cave room built: %d floor tiles, %d wall tiles" % [floor_count, wall_count])
	print("TileMap position: ", tilemap.position)
	print("TileSet tile size: ", tilemap.tile_set.tile_size)

extends CharacterBody2D

# Isometric click-to-move player controller with A* pathfinding

# Movement constants
const SPEED = 150.0
const ACCELERATION = 600.0
const FRICTION = 800.0
const ARRIVAL_DISTANCE = 5.0  # How close to target before stopping
const WAYPOINT_THRESHOLD = 32.0  # Distance to consider waypoint reached (larger = smoother)
const LOOK_AHEAD_DISTANCE = 80.0  # How far ahead to look for smoother turns
const TILE_SIZE = 64  # Tile size for pathfinding

# Movement state
var target_position: Vector2 = Vector2.ZERO
var has_target: bool = false
var is_attacking: bool = false
var mouse_held: bool = false  # Track if left mouse button is held

# Pathfinding
var path: Array = []  # Array of Vector2 waypoints
var current_waypoint_index: int = 0
var pathfinder = null  # AStarPathfinder instance

# Direction facing (in radians, 0 = right)
var facing_angle: float = 0.0

func _ready():
	print("Isometric player with A* pathfinding ready - Click or hold to move!")

## Set the pathfinder reference
func set_pathfinder(pf) -> void:
	pathfinder = pf
	print("Pathfinder connected to player!")

func _input(event):
	# Left click to move
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				# Mouse button pressed - start following
				mouse_held = true
				_set_move_target(get_global_mouse_position())
			else:
				# Mouse button released - stop following cursor
				mouse_held = false
		
		# Right click to attack (placeholder)
		elif event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
			var attack_target = get_global_mouse_position()
			print("Attack at: ", attack_target)
			is_attacking = true
			mouse_held = false
			has_target = false
			path.clear()
			# TODO: Implement attack logic

## Set a new movement target and calculate path
func _set_move_target(pos: Vector2) -> void:
	if pathfinder == null:
		# Fallback to direct movement if no pathfinder
		target_position = pos
		has_target = true
		is_attacking = false
		path.clear()
		print("Moving directly to: ", pos)
		return
	
	# Calculate path using A*
	path = pathfinder.find_path(global_position, pos, TILE_SIZE)
	
	if path.size() > 0:
		current_waypoint_index = 0
		has_target = true
		is_attacking = false
		# Set first waypoint as target
		target_position = path[current_waypoint_index]
		print("Path found with %d waypoints to: %s" % [path.size(), pos])
	else:
		# No path found - try direct movement
		target_position = pos
		has_target = true
		is_attacking = false
		path.clear()
		print("No path found, moving directly to: ", pos)

func _physics_process(delta):
	# If mouse is held, continuously update target to cursor position
	if mouse_held:
		_set_move_target(get_global_mouse_position())
	
	if has_target and not is_attacking:
		# If following a path, check if we've reached current waypoint
		if path.size() > 0 and current_waypoint_index < path.size():
			var waypoint_distance = global_position.distance_to(target_position)
			
			# If we've reached the current waypoint, move to next
			if waypoint_distance <= WAYPOINT_THRESHOLD:
				current_waypoint_index += 1
				
				if current_waypoint_index < path.size():
					# Move to next waypoint
					target_position = path[current_waypoint_index]
				else:
					# Reached end of path
					if not mouse_held:
						has_target = false
						path.clear()
		
		# Calculate movement target with look-ahead for smoother turns
		var move_target = target_position
		
		# If there's a next waypoint, blend towards it for smoother curves
		if path.size() > 0 and current_waypoint_index < path.size() - 1:
			var next_waypoint = path[current_waypoint_index + 1]
			var dist_to_current = global_position.distance_to(target_position)
			
			# As we get closer to current waypoint, start moving towards next one
			if dist_to_current < LOOK_AHEAD_DISTANCE:
				var blend_factor = 1.0 - (dist_to_current / LOOK_AHEAD_DISTANCE)
				blend_factor = clamp(blend_factor * 0.5, 0.0, 0.5)  # Max 50% blend
				move_target = target_position.lerp(next_waypoint, blend_factor)
		
		# Calculate direction to move target
		var direction = (move_target - global_position).normalized()
		var distance = global_position.distance_to(target_position)
		
		# Check if we've arrived at final destination
		if distance <= ARRIVAL_DISTANCE and not mouse_held:
			has_target = false
			path.clear()
			# Stop moving
			velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
		else:
			# Move toward target with smooth acceleration
			var target_velocity = direction * SPEED
			velocity = velocity.move_toward(target_velocity, ACCELERATION * delta)
			
			# Update facing direction smoothly
			if velocity.length() > 10.0:  # Only update facing when actually moving
				facing_angle = velocity.angle()
	else:
		# Apply friction when no target
		velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
	
	# Apply movement
	move_and_slide()

func _process(_delta):
	# Depth sorting for isometric layering
	# Objects with higher Y position appear in front
	# Normalize to reasonable z-index range (0-100)
	z_index = int(global_position.y / 64.0)
	
	# Rotate sprite to face movement direction (optional visual)
	# For now just store the angle, we'll use it for animation direction later
	rotation = facing_angle

func get_facing_direction() -> int:
	# Get 8-directional facing for animations
	# Returns 0-7 representing N, NE, E, SE, S, SW, W, NW
	var angle_deg = rad_to_deg(facing_angle)
	if angle_deg < 0:
		angle_deg += 360
	
	# Divide 360 degrees into 8 sections (45 degrees each)
	var direction = int((angle_deg + 22.5) / 45.0) % 8
	return direction

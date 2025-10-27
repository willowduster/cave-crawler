extends CharacterBody2D

# Isometric click-to-move player controller (Diablo 2 style)

# Movement constants
const SPEED = 150.0
const ACCELERATION = 600.0
const FRICTION = 800.0
const ARRIVAL_DISTANCE = 5.0  # How close to target before stopping

# Movement state
var target_position: Vector2 = Vector2.ZERO
var has_target: bool = false
var is_attacking: bool = false
var mouse_held: bool = false  # Track if left mouse button is held

# Direction facing (in radians, 0 = right)
var facing_angle: float = 0.0

func _ready():
	print("Isometric player ready - Click or hold to move!")

func _input(event):
	# Left click to move
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				# Mouse button pressed - start following
				mouse_held = true
				target_position = get_global_mouse_position()
				has_target = true
				is_attacking = false
				print("Moving to: ", target_position)
			else:
				# Mouse button released - stop following cursor
				mouse_held = false
		
		# Right click to attack (placeholder)
		elif event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
			var attack_target = get_global_mouse_position()
			print("Attack at: ", attack_target)
			is_attacking = true
			mouse_held = false
			# TODO: Implement attack logic

func _physics_process(delta):
	# If mouse is held, continuously update target to cursor position
	if mouse_held:
		target_position = get_global_mouse_position()
		has_target = true
		is_attacking = false
	
	if has_target and not is_attacking:
		# Calculate direction to target
		var direction = (target_position - global_position).normalized()
		var distance = global_position.distance_to(target_position)
		
		# Check if we've arrived (only stop if mouse not held)
		if distance <= ARRIVAL_DISTANCE and not mouse_held:
			has_target = false
			# Stop moving
			velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
		else:
			# Move toward target
			velocity = velocity.move_toward(direction * SPEED, ACCELERATION * delta)
			
			# Update facing direction
			facing_angle = direction.angle()
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

extends CharacterBody2D

# Enemy AI with wandering behavior
# Uses pathfinding to navigate around obstacles

enum State {
	IDLE,
	WANDER,
	CHASE,
	ATTACK,
	DEAD
}

const SPEED = 80.0
const WANDER_RADIUS = 200.0
const IDLE_TIME_MIN = 1.0
const IDLE_TIME_MAX = 3.0
const WANDER_TIME_MIN = 2.0
const WANDER_TIME_MAX = 5.0
const WAYPOINT_THRESHOLD = 32.0
const DETECTION_RADIUS = 300.0
const ATTACK_RANGE = 50.0

var state = State.IDLE
var pathfinder = null
var current_path = []
var current_waypoint_index = 0
var state_timer = 0.0
var spawn_position = Vector2.ZERO
var animated_sprite = null

func _ready():
	spawn_position = global_position
	animated_sprite = $AnimatedSprite2D
	
	# Setup sprite frames
	_setup_sprite_frames()
	
	# Start in idle state
	change_state(State.IDLE)
	
	# Connect to level's pathfinder when ready
	call_deferred("_connect_to_pathfinder")

func _setup_sprite_frames():
	# Create sprite frames resource
	var sprite_frames = SpriteFrames.new()
	
	# Load idle animation (4 frames)
	sprite_frames.add_animation("idle")
	sprite_frames.set_animation_loop("idle", true)
	sprite_frames.set_animation_speed("idle", 8.0)
	for i in range(4):
		var texture = load("res://assets/enemies/slime/idle/frame_%04d.png" % i)
		sprite_frames.add_frame("idle", texture)
	
	# Load walk animation (8 frames)
	sprite_frames.add_animation("walk")
	sprite_frames.set_animation_loop("walk", true)
	sprite_frames.set_animation_speed("walk", 12.0)
	for i in range(8):
		var texture = load("res://assets/enemies/slime/walk/frame_%04d.png" % i)
		sprite_frames.add_frame("walk", texture)
	
	# Load attack animation (6 frames)
	sprite_frames.add_animation("attack")
	sprite_frames.set_animation_loop("attack", false)
	sprite_frames.set_animation_speed("attack", 10.0)
	for i in range(6):
		var texture = load("res://assets/enemies/slime/attack/frame_%04d.png" % i)
		sprite_frames.add_frame("attack", texture)
	
	# Load death animation (8 frames)
	sprite_frames.add_animation("death")
	sprite_frames.set_animation_loop("death", false)
	sprite_frames.set_animation_speed("death", 8.0)
	for i in range(8):
		var texture = load("res://assets/enemies/slime/death/frame_%04d.png" % i)
		sprite_frames.add_frame("death", texture)
	
	# Apply to sprite
	animated_sprite.sprite_frames = sprite_frames
	animated_sprite.play("idle")

func _connect_to_pathfinder():
	# Find the level generator in the scene tree
	var level = get_tree().get_root().get_node_or_null("ProceduralCaveLevel")
	if level and level.has_method("get_pathfinder"):
		pathfinder = level.get_pathfinder()

func _physics_process(delta):
	if state == State.DEAD:
		return
	
	state_timer -= delta
	
	match state:
		State.IDLE:
			_process_idle(delta)
		State.WANDER:
			_process_wander(delta)
		State.CHASE:
			_process_chase(delta)
		State.ATTACK:
			_process_attack(delta)

func _process_idle(delta):
	# Play idle animation
	if animated_sprite.animation != "idle":
		animated_sprite.play("idle")
	
	# Stop moving
	velocity = Vector2.ZERO
	move_and_slide()
	
	# When timer expires, start wandering
	if state_timer <= 0:
		change_state(State.WANDER)

func _process_wander(delta):
	# If we don't have a pathfinder yet, just wait
	if not pathfinder:
		return
	
	# Play walk animation
	if animated_sprite.animation != "walk":
		animated_sprite.play("walk")
	
	# If we don't have a path or timer expired, pick a new wander destination
	if current_path.is_empty() or state_timer <= 0:
		_pick_wander_destination()
		return
	
	# Follow the current path
	if current_waypoint_index < current_path.size():
		var target_position = current_path[current_waypoint_index]
		var distance_to_waypoint = global_position.distance_to(target_position)
		
		# Check if we reached the current waypoint
		if distance_to_waypoint < WAYPOINT_THRESHOLD:
			current_waypoint_index += 1
			
			# If we reached the end of the path, go back to idle
			if current_waypoint_index >= current_path.size():
				change_state(State.IDLE)
				return
		else:
			# Move toward the waypoint
			var direction = (target_position - global_position).normalized()
			velocity = direction * SPEED
			
			# Flip sprite based on movement direction
			if velocity.length() > 10:
				animated_sprite.flip_h = velocity.x < 0
			
			move_and_slide()
	else:
		# No more waypoints, go back to idle
		change_state(State.IDLE)

func _process_chase(delta):
	# TODO: Implement chase behavior when combat is added
	# For now, just wander
	change_state(State.WANDER)

func _process_attack(delta):
	# TODO: Implement attack behavior when combat is added
	pass

func _pick_wander_destination():
	if not pathfinder:
		return
	
	# Pick a random point within wander radius
	var angle = randf() * TAU
	var distance = randf_range(WANDER_RADIUS * 0.5, WANDER_RADIUS)
	var target = spawn_position + Vector2(cos(angle), sin(angle)) * distance
	
	# Get path to target
	var path = pathfinder.find_path(global_position, target)
	
	if path.size() > 0:
		current_path = path
		current_waypoint_index = 0
		# Reset wander timer
		state_timer = randf_range(WANDER_TIME_MIN, WANDER_TIME_MAX)
	else:
		# Couldn't find a path, try again soon
		change_state(State.IDLE)

func change_state(new_state: State):
	state = new_state
	
	match state:
		State.IDLE:
			state_timer = randf_range(IDLE_TIME_MIN, IDLE_TIME_MAX)
			current_path.clear()
			current_waypoint_index = 0
		State.WANDER:
			state_timer = randf_range(WANDER_TIME_MIN, WANDER_TIME_MAX)
			_pick_wander_destination()
		State.CHASE:
			pass
		State.ATTACK:
			pass
		State.DEAD:
			animated_sprite.play("death")
			# TODO: Remove enemy after death animation

func take_damage(amount: int):
	# TODO: Implement health system
	change_state(State.DEAD)

func die():
	change_state(State.DEAD)

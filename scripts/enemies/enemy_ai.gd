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

@export var speed: float = 80.0
@export var wander_radius: float = 300.0  # Max distance from spawn the enemy will roam
@export var idle_time_min: float = 1.0
@export var idle_time_max: float = 3.0
@export var wander_time_min: float = 2.0
@export var wander_time_max: float = 5.0
@export var waypoint_threshold: float = 32.0
@export var detection_radius: float = 300.0
@export var attack_range: float = 50.0

@export var enemy_name := "slime"
var state = State.IDLE
var pathfinder = null
var current_path = []
var current_waypoint_index = 0
var state_timer = 0.0
var spawn_position = Vector2.ZERO
var animated_sprite = null
@export var debug_markers: bool = true
@export var debug_update_interval: float = 0.5 # seconds between debug console updates per enemy
var last_wander_target: Vector2 = Vector2.ZERO
var player_node = null
var chase_target: Vector2 = Vector2.ZERO
var _spawn_marker = null
var _target_marker = null
var debug_console = null
var _debug_update_timer: float = 0.0
@export var debug_visible_radius: float = 1024.0 # only report enemies within this distance to player
@export var show_labels: bool = true
@export var name_label_offset: Vector2 = Vector2(0, -32)
@export var state_label_offset: Vector2 = Vector2(0, 28)
var _name_label = null
var _state_label = null
var _leak_tracker = null
var label_font = null

func _state_to_string(s: State) -> String:
	match s:
		State.IDLE:
			return "IDLE"
		State.WANDER:
			return "WANDER"
		State.CHASE:
			return "CHASE"
		State.ATTACK:
			return "ATTACK"
		State.DEAD:
			return "DEAD"
	return str(s)

func _is_on_camera_frustum() -> bool:
	# Prefer camera-frustum check if a Camera2D is active
	var vp = get_viewport()
	if vp:
		var cam = vp.get_camera_2d()
		if cam != null:
			var cam_pos = cam.global_position
			var vp_size = vp.get_visible_rect().size
			if vp_size == Vector2.ZERO:
				vp_size = Vector2(1280, 720)
			# Account for camera zoom
			var zoom = cam.zoom if cam.has_method("get_zoom") else cam.zoom
			var half = vp_size * 0.5 * zoom
			var rel = global_position - cam_pos
			return abs(rel.x) <= half.x and abs(rel.y) <= half.y

	# Fallback: approximate camera by centering on player (previous behavior)
	if player_node == null:
		return false
	var vp_rect = vp.get_visible_rect()
	var vp_size2 = vp_rect.size
	if vp_size2 == Vector2.ZERO:
		vp_size2 = Vector2(1280, 720)
	var half2 = vp_size2 * 0.5
	var rel2 = global_position - player_node.global_position
	return abs(rel2.x) <= half2.x and abs(rel2.y) <= half2.y
@export var look_ahead_distance: float = 80.0

@export var max_health: int = 10
var health: int = max_health

@export var attack_damage: int = 1
@export var attack_cooldown: float = 1.0
var _last_attack_time: float = -999.0

func _ready():
	spawn_position = global_position
	animated_sprite = $AnimatedSprite2D

	# Try to auto-load a bundled font from res://assets/fonts if present.
	# Prefer bundled fonts to avoid platform-specific system font loads.
	# Wire local Label2D nodes (if present) so we can update text directly.
	if has_node("NameLabel"):
		_name_label = $NameLabel
	if has_node("StateLabel"):
		_state_label = $StateLabel

	# Initialize labels immediately for visibility/debugging
	if _name_label != null:
		_name_label.text = str(enemy_name)
		_name_label.visible = show_labels
		print("Enemy label wired for %s" % name)
	if _state_label != null:
		_state_label.text = _state_to_string(state)
		_state_label.visible = show_labels
	
	# Setup sprite frames
	_setup_sprite_frames()
	
	# Start in idle state
	change_state(State.IDLE)

	# Connect to level's pathfinder when ready
	call_deferred("_connect_to_pathfinder")

	# Create debug markers (simple Sprite2D with generated texture)
	if debug_markers:
		_spawn_marker = _make_marker(Color(0, 1, 0, 0.8))
		if _spawn_marker == null:
			_spawn_marker = Node2D.new()
		add_child(_spawn_marker)
		# Position the spawn marker in world coordinates
		_spawn_marker.global_position = spawn_position

		_target_marker = _make_marker(Color(1, 0, 0, 0.8))
		if _target_marker == null:
			_target_marker = Node2D.new()
		add_child(_target_marker)
		_target_marker.visible = false

		# Ensure a runtime leak tracker exists at root and register our markers
		_ensure_leak_tracker()
		var current_scene = get_tree().get_current_scene()
		var lt = null
		if current_scene != null:
			lt = current_scene.get_node_or_null("LeakTracker")
		if lt != null and lt.has_method("register"):
			lt.register(_spawn_marker, "spawn_marker_%s" % name)
			lt.register(_target_marker, "target_marker_%s" % name)
			_leak_tracker = lt
		# Register markers with the leak tracker for debugging
		if _spawn_marker and has_method("_register_leak"):
			pass
		# attempt to register with LeakTracker if available (best-effort)
		# Emit a short debug trace so we can find where CanvasItems are created
		print("LEAK-DEBUG: created spawn marker for %s" % name)

		# Update marker colors based on initial state
		_update_markers_for_state()

func _ensure_leak_tracker() -> void:
	var root = get_tree().get_root()
	if root.has_node("LeakTracker"):
		return
	var path = "res://scripts/debug/leak_tracker.gd"
	if ResourceLoader.exists(path):
		var script = load(path)
		var node = Node.new()
		node.name = "LeakTracker"
		node.set_script(script)
		root.add_child(node)
	else:
		# best-effort: try to load, but don't fail if missing
		# this file was added dynamically during debugging
		pass

func _ensure_label_hud() -> void:
	# HUD migration removed — keep function stub for compatibility
	return

func _migrate_labels_to_hud() -> void:
	# Migration removed — keep stub for compatibility
	return

func _update_labels_position() -> void:
	# Position updates removed — labels are updated in _update_markers_for_state on interval
	return

func _setup_sprite_frames():
	# Create sprite frames resource
	var sprite_frames = SpriteFrames.new()
	
	# Load idle animation (4 frames: 0000-0003)
	sprite_frames.add_animation("idle")
	sprite_frames.set_animation_loop("idle", true)
	sprite_frames.set_animation_speed("idle", 8.0)
	for i in range(4):
		var path = "res://assets/enemies/%s/idle/frame_%04d.png" % [enemy_name, i]
		var texture = load(path)
		if texture:
			sprite_frames.add_frame("idle", texture)
		else:
			push_error("Failed to load idle frame: " + path)
	
	# Load walk animation (8 frames: 0000-0007)
	sprite_frames.add_animation("walk")
	sprite_frames.set_animation_loop("walk", true)
	sprite_frames.set_animation_speed("walk", 12.0)
	for i in range(8):
		var path = "res://assets/enemies/%s/walk/frame_%04d.png" % [enemy_name, i]
		var texture = load(path)
		if texture:
			sprite_frames.add_frame("walk", texture)
		else:
			push_error("Failed to load walk frame: " + path)
	
	# Load attack animation (6 frames: 0000-0005)
	sprite_frames.add_animation("attack")
	sprite_frames.set_animation_loop("attack", false)
	sprite_frames.set_animation_speed("attack", 10.0)
	for i in range(6):
		var path = "res://assets/enemies/%s/attack/frame_%04d.png" % [enemy_name, i]
		var texture = load(path)
		if texture:
			sprite_frames.add_frame("attack", texture)
		else:
			push_error("Failed to load attack frame: " + path)
	
	# Load death animation (8 frames: 0000-0007)
	sprite_frames.add_animation("death")
	sprite_frames.set_animation_loop("death", false)
	sprite_frames.set_animation_speed("death", 8.0)
	for i in range(8):
		var path = "res://assets/enemies/%s/death/frame_%04d.png" % [enemy_name, i]
		var texture = load(path)
		if texture:
			sprite_frames.add_frame("death", texture)
		else:
			push_error("Failed to load death frame: " + path)
	
	# Apply to sprite
	animated_sprite.sprite_frames = sprite_frames
	animated_sprite.play("idle")

func _connect_to_pathfinder():
	# Robustly find a node that exposes get_pathfinder() (ProceduralCave is the scene root)
	var root = get_tree().get_root()
	pathfinder = null

	# Depth-first search for any node that has get_pathfinder()
	var stack = []
	for child in root.get_children():
		stack.append(child)

	while stack.size() > 0:
		var node = stack.pop_back()
		if node == null:
			continue
		if node.has_method("get_pathfinder"):
			pathfinder = node.get_pathfinder()
			break
		for c in node.get_children():
			stack.append(c)

	if pathfinder:
		# Optionally inform for debugging
		#print("Pathfinder connected for enemy: %s" % [name])
		pass
	else:
		# Try again later in case the level hasn't finished ready
		call_deferred("_connect_to_pathfinder")

	# Also try to connect to debug console for state updates
	call_deferred("_connect_to_debug_console")

func _connect_to_debug_console():
	var root = get_tree().get_root()
	debug_console = null
	var stack = []
	for child in root.get_children():
		stack.append(child)
	while stack.size() > 0:
		var node = stack.pop_back()
		if node == null:
			continue
		if node.has_method("update_section") and node.has_method("add_section"):
			debug_console = node
			break
		for c in node.get_children():
			stack.append(c)

		# If we found a debug console, try to auto-assign a label font from its themed controls
		if debug_console != null and label_font == null:
			# Breadth-first search for a Control with a Theme-provided font
			var q = []
			q.append(debug_console)
			while q.size() > 0 and label_font == null:
				var n = q.pop_back()
				# enqueue children
				for ch in n.get_children():
					q.append(ch)
				# If this node is a Control, try to pull a font from its Theme
				if n is Control:
					var theme = n.get_theme()
					if theme != null:
						# try common font keys
						var candidate = theme.get_font("font", n.get_class())
						if candidate != null:
							label_font = candidate
							break
						candidate = theme.get_font("normal_font", n.get_class())
						if candidate != null:
							label_font = candidate
							break

		# If no themed font found, leave label_font null (labels will be skipped).

func _physics_process(delta):
	if state == State.DEAD:
		return
	
	state_timer -= delta

	# Throttle debug-console updates per enemy
	_debug_update_timer = max(0.0, _debug_update_timer - delta)

	# Attempt to find the player node if not already cached
	if player_node == null:
		var players = get_tree().get_nodes_in_group("player")
		if players.size() > 0:
			player_node = players[0]

	# Simple detection: if player is within detection_radius, enter CHASE
	if player_node and state != State.CHASE and state != State.ATTACK:
		var dist_to_player = global_position.distance_to(player_node.global_position)
		if dist_to_player <= detection_radius:
			change_state(State.CHASE)

	# No per-frame HUD updates here; labels are child nodes and updated on debug interval
	
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
	# If we don't have a pathfinder yet, try to connect and wait
	if not pathfinder:
		_connect_to_pathfinder()
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
		if distance_to_waypoint < waypoint_threshold:
			current_waypoint_index += 1

			# If we reached the end of the path, go back to idle
			if current_waypoint_index >= current_path.size():
				change_state(State.IDLE)
				return
		else:
				# Move toward the waypoint with look-ahead blending for smoother turns
				var move_target = target_position
				if current_waypoint_index < current_path.size() - 1:
					var next_waypoint = current_path[current_waypoint_index + 1]
					var dist_to_current = global_position.distance_to(target_position)
					if dist_to_current < look_ahead_distance:
						var blend_factor = 1.0 - (dist_to_current / look_ahead_distance)
						blend_factor = clamp(blend_factor * 0.5, 0.0, 0.5)
						move_target = target_position.lerp(next_waypoint, blend_factor)

				var direction = (move_target - global_position).normalized()
				velocity = direction * speed

				# Flip sprite based on movement direction
				if velocity.length() > 10:
					animated_sprite.flip_h = velocity.x < 0

				move_and_slide()
	else:
		# No more waypoints, go back to idle
		change_state(State.IDLE)

	# (no per-frame update needed; markers are Sprite2D nodes)

func _process_chase(delta):
	# Basic chase behavior: follow player using pathfinder
	if not pathfinder:
		return

	if player_node == null:
		return

	# If player moved, update chase target and path
	chase_target = player_node.global_position
	var path = pathfinder.find_path(global_position, chase_target)

	if path.size() == 0:
		# Can't reach player, fallback to wander
		change_state(State.WANDER)
		return

	# Follow the path (reuse same logic as wander following)
	current_path = path
	current_waypoint_index = 0
	# Play walk animation
	if animated_sprite.animation != "walk":
		animated_sprite.play("walk")

	# Use look-ahead blending while following path for smoother turns
	if current_waypoint_index < current_path.size():
		var target_position = current_path[current_waypoint_index]
		var move_target = target_position
		if current_waypoint_index < current_path.size() - 1:
			var next_waypoint = current_path[current_waypoint_index + 1]
			var dist_to_current = global_position.distance_to(target_position)
			if dist_to_current < look_ahead_distance:
				var blend_factor = 1.0 - (dist_to_current / look_ahead_distance)
				blend_factor = clamp(blend_factor * 0.5, 0.0, 0.5)
				move_target = target_position.lerp(next_waypoint, blend_factor)

		var direction = (move_target - global_position).normalized()
		velocity = direction * speed
		if velocity.length() > 10:
			animated_sprite.flip_h = velocity.x < 0
		move_and_slide()

	# If close enough, enter attack
	var dist = global_position.distance_to(player_node.global_position)
	if dist <= attack_range:
		change_state(State.ATTACK)

func _process_attack(delta):
	# Attack behavior: apply damage with cooldown, play animation
	if animated_sprite.animation != "attack":
		animated_sprite.play("attack")

	# Attack: perform damage then wait for cooldown period (handled by state_timer)
	if not animated_sprite.animation == "attack":
		animated_sprite.play("attack")

	# Apply damage immediately on attack start
	if player_node and player_node.has_method("take_damage"):
		player_node.take_damage(attack_damage)
	else:
		# fallback debug
		#print("Enemy %s would attack for %d" % [name, attack_damage])
		pass

	# Use state_timer (set in change_state) to wait before returning to WANDER
	# If state_timer <= 0, start the cooldown
	if state_timer <= 0:
		state_timer = attack_cooldown

func _pick_wander_destination():
	if not pathfinder:
		return
	# Pick a random point within wander radius (confined to spawn area)
	var attempts = 0
	var found = false
	var chosen_path = []

	while attempts < 8 and not found:
		var angle = randf() * TAU
		var distance = randf_range(wander_radius * 0.3, wander_radius)
		var target = spawn_position + Vector2(cos(angle), sin(angle)) * distance
		# Ensure target tile is walkable before asking pathfinder
		if not pathfinder.is_walkable(target):
			attempts += 1
			continue
		var path = pathfinder.find_path(global_position, target)
		if path.size() > 0:
			chosen_path = path
			found = true
			break
		attempts += 1

	if found:
		current_path = chosen_path
		current_waypoint_index = 0
		# Reset wander timer
		state_timer = randf_range(wander_time_min, wander_time_max)
		# Store chosen final target for debug markers
		if current_path.size() > 0:
			last_wander_target = current_path[current_path.size() - 1]
			if _target_marker:
				_target_marker.global_position = last_wander_target
				_target_marker.visible = true
	else:
		# Couldn't find a valid wander target; back to idle briefly
		change_state(State.IDLE)

func change_state(new_state: State):
	state = new_state
	
	match state:
		State.IDLE:
			state_timer = randf_range(idle_time_min, idle_time_max)
			current_path.clear()
			current_waypoint_index = 0
		State.WANDER:
			state_timer = randf_range(wander_time_min, wander_time_max)
			_pick_wander_destination()
			if _target_marker:
				_target_marker.visible = true
			# Update marker colors by state
			_update_markers_for_state()
		State.CHASE:
			# No timer; chase until close/fallback
			current_path.clear()
			current_waypoint_index = 0
			_update_markers_for_state()
		State.ATTACK:
			# Attack handled by _process_attack
			current_path.clear()
			current_waypoint_index = 0
			state_timer = attack_cooldown
			# perform initial attack when entering state
			if player_node and player_node.has_method("take_damage"):
				player_node.take_damage(attack_damage)
			_update_markers_for_state()
			_update_markers_for_state()
		State.DEAD:
			animated_sprite.play("death")
			# TODO: Remove enemy after death animation

func take_damage(amount: int):
	# Reduce health and die when reaching zero
	health -= amount
	#print("Enemy %s took %d damage, hp=%d" % [name, amount, health])
	if health <= 0:
		change_state(State.DEAD)

func die():
	change_state(State.DEAD)

func _make_marker(col: Color):
	# Return a small Label2D as a lightweight visible marker (avoids texture generation)
	var poly = Polygon2D.new()
	poly.polygon = [Vector2(-4, -4), Vector2(4, -4), Vector2(0, 4)]
	poly.color = col
	poly.z_index = 1000
	return poly

func _exit_tree() -> void:
	# Ensure markers are unregistered and freed to avoid leaks
	# Log freeing markers to help track lifetime in logs
	if _spawn_marker != null:
		print("LEAK-DEBUG: exiting, freeing spawn marker for %s" % name)
		if is_instance_valid(_spawn_marker):
			var p = _spawn_marker.get_parent()
			if p != null:
				p.remove_child(_spawn_marker)
				# ensure it's not visible and free immediately
				_spawn_marker.visible = false
				# unregister from leak tracker if present
				if _leak_tracker != null and _leak_tracker.has_method("unregister"):
					_leak_tracker.unregister(_spawn_marker)
				_spawn_marker.queue_free()
		_spawn_marker = null
	if _target_marker != null:
		print("LEAK-DEBUG: exiting, freeing target marker for %s" % name)
		if is_instance_valid(_target_marker):
			var p2 = _target_marker.get_parent()
			if p2 != null:
				p2.remove_child(_target_marker)
				_target_marker.visible = false
				# unregister from leak tracker if present
				if _leak_tracker != null and _leak_tracker.has_method("unregister"):
					_leak_tracker.unregister(_target_marker)
				_target_marker.queue_free()
		_target_marker = null


func _update_markers_for_state():
	if not debug_markers:
		return
	var col = Color(0, 1, 0, 0.8) # idle = green
	match state:
		State.IDLE:
			col = Color(0, 1, 0, 0.8)
		State.WANDER:
			col = Color(1, 1, 0, 0.9)
		State.CHASE:
			col = Color(1, 0.5, 0, 0.95)
		State.ATTACK:
			col = Color(1, 0, 0, 1.0)
		State.DEAD:
			col = Color(0.2, 0.2, 0.2, 0.6)

	if _spawn_marker and _spawn_marker is Polygon2D:
		_spawn_marker.color = col
	if _target_marker and _target_marker is Polygon2D:
		_target_marker.color = col

	# Update on-screen labels (name above, state below) if requested
	# Use the Label2D nodes we added to the enemy scene for world-space text
	if show_labels and _debug_update_timer <= 0.0:
		if _is_on_camera_frustum():
			if _name_label != null:
				_name_label.text = str(enemy_name)
				_name_label.position = name_label_offset
				_name_label.visible = true
			if _state_label != null:
				_state_label.text = _state_to_string(state)
				_state_label.position = state_label_offset
				_state_label.visible = true
		else:
			if _name_label != null:
				_name_label.visible = false
			if _state_label != null:
				_state_label.visible = false
		_debug_update_timer = debug_update_interval

func _draw() -> void:
	# No-op: Label2D nodes now handle in-world labels. Kept for compatibility.
	return

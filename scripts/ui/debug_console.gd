extends CanvasLayer
class_name DebugConsole

## Unified debug console for displaying game info, stats, and instructions

@onready var console_panel: PanelContainer = $ConsolePanel
@onready var text_label: RichTextLabel = $ConsolePanel/MarginContainer/TextLabel
@onready var toggle_button: Button = $ToggleButton

var sections: Dictionary = {}
var update_interval: float = 0.5
var time_since_update: float = 0.0
var _dirty: bool = true
var is_visible: bool = true
@export var log_to_file: bool = false
@export var log_file_path: String = "logs/debug_console_live.log"
@export var max_enemy_sections: int = 20

func _ready() -> void:
	# Initialize default sections
	add_section("title", "CAVE CRAWLER", Color.YELLOW)
	add_section("separator1", "─────────────────────", Color.DARK_GRAY)
	add_section("stats", "", Color.CYAN)
	add_section("player", "", Color.GREEN_YELLOW)
	add_section("debug", "", Color.LIGHT_GRAY)
	
	# Connect toggle button
	if toggle_button:
		toggle_button.pressed.connect(_on_toggle_pressed)
	
	_update_display()

func _input(event: InputEvent) -> void:
	# Toggle with F1 key
	if event.is_action_pressed("ui_text_backspace"):  # F1 equivalent
		toggle_visibility()

func _process(delta: float) -> void:
	time_since_update += delta
	if time_since_update >= update_interval:
		time_since_update = 0.0
		_update_dynamic_sections()
		# Only redraw the display when something changed to avoid per-tick work
		if _dirty:
			_update_display()
			_dirty = false

func add_section(id: String, text: String, color: Color = Color.WHITE) -> void:
	sections[id] = {
		"text": text,
		"color": color,
		"order": sections.size()
	}
	_dirty = true

func update_section(id: String, text: String) -> void:
	if sections.has(id):
		# Only update if the text actually changed to avoid redundant redraws
		if sections[id]["text"] != text:
			sections[id]["text"] = text
			_dirty = true

func remove_section(id: String) -> void:
	sections.erase(id)
	_dirty = true

func _update_dynamic_sections() -> void:
	# Update player info
	var player = get_tree().get_first_node_in_group("player")
	if player:
		var player_info = "Player: %.0f, %.0f | Rotation: %.1f°" % [
			player.global_position.x,
			player.global_position.y,
			rad_to_deg(player.rotation)
		]
		update_section("player", player_info)

func _update_display() -> void:
	if not text_label:
		return
	
	# Sort sections by order
	var all_keys = sections.keys()
	all_keys.sort_custom(func(a, b): return sections[a]["order"] < sections[b]["order"])

	# If there are many enemy sections, limit to the nearest N using stored positions
	var enemy_keys := []
	var other_keys := []
	for k in all_keys:
		if k.begins_with("enemy_state_"):
			enemy_keys.append(k)
		else:
			other_keys.append(k)

	var selected_enemy_keys := []
	if enemy_keys.size() > 0:
		# Determine camera/player center for distance sorting
		var vp = get_viewport()
		var center = Vector2.ZERO
		var cam = vp.get_camera_2d()
		if cam != null:
			center = cam.global_position
		else:
			var player = get_tree().get_first_node_in_group("player")
			if player:
				center = player.global_position

		# Build list of (key, dist) for keys that have a pos entry
		var keyed = []
		for k in enemy_keys:
			var dist = 1e9
			if sections[k].has("pos"):
				dist = sections[k]["pos"].distance_to(center)
			keyed.append({"key": k, "dist": dist})

		keyed.sort_custom(func(a, b): return a["dist"] < b["dist"])

		var limit = clamp(max_enemy_sections, 0, keyed.size())
		for i in range(limit):
			selected_enemy_keys.append(keyed[i]["key"])

	var sorted_keys = other_keys + selected_enemy_keys
	
	# Build BBCode text
	text_label.clear()
	var built_text := ""
	for key in sorted_keys:
		var section = sections[key]
		var color_hex = section["color"].to_html(false)
		var line = "[color=#%s]%s[/color]\n" % [color_hex, section["text"]]
		text_label.append_text(line)
		built_text += line

	# Optionally write the built console snapshot to a file (throttled by _dirty/update interval)
	if log_to_file:
		# Use FileAccess to append to file (Godot 4 API)
		var f = FileAccess.open(log_file_path, FileAccess.WRITE_READ)
		if f != null:
			# Seek to end to append
			f.seek_end()
			f.store_line("--- DebugConsole snapshot ---")
			for key in sorted_keys:
				var section = sections[key]
				f.store_line("%s: %s" % [key, str(section["text"])])
			f.store_line("")
			f.close()
		else:
			# If file open failed, ignore to avoid noisy errors during profiling
			pass

func set_stats(stats_text: String) -> void:
	update_section("stats", stats_text)

func set_debug(debug_text: String) -> void:
	update_section("debug", debug_text)

func _on_toggle_pressed() -> void:
	toggle_visibility()

func toggle_visibility() -> void:
	is_visible = not is_visible
	console_panel.visible = is_visible
	
	# Update button text
	if toggle_button:
		toggle_button.text = "▼" if is_visible else "▲"

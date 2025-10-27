extends CanvasLayer
class_name DebugConsole

## Unified debug console for displaying game info, stats, and instructions

@onready var console_panel: PanelContainer = $ConsolePanel
@onready var text_label: RichTextLabel = $ConsolePanel/MarginContainer/TextLabel
@onready var toggle_button: Button = $ToggleButton

var sections: Dictionary = {}
var update_interval: float = 0.1
var time_since_update: float = 0.0
var is_visible: bool = true

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
		_update_display()

func add_section(id: String, text: String, color: Color = Color.WHITE) -> void:
	sections[id] = {
		"text": text,
		"color": color,
		"order": sections.size()
	}

func update_section(id: String, text: String) -> void:
	if sections.has(id):
		sections[id]["text"] = text

func remove_section(id: String) -> void:
	sections.erase(id)

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
	var sorted_keys = sections.keys()
	sorted_keys.sort_custom(func(a, b): return sections[a]["order"] < sections[b]["order"])
	
	# Build BBCode text
	text_label.clear()
	for key in sorted_keys:
		var section = sections[key]
		var color_hex = section["color"].to_html(false)
		text_label.append_text("[color=#%s]%s[/color]\n" % [color_hex, section["text"]])

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

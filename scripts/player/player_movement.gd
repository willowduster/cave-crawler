extends CharacterBody2D

# Player movement constants
const SPEED = 200.0
const JUMP_VELOCITY = -400.0
const ACCELERATION = 800.0
const FRICTION = 1000.0

# Get the gravity from the project settings
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _physics_process(delta):
	# Add gravity
	if not is_on_floor():
		velocity.y += gravity * delta

	# Handle jump
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Get input direction
	var direction = Input.get_axis("ui_left", "ui_right")
	
	# Apply acceleration or friction
	if direction != 0:
		velocity.x = move_toward(velocity.x, direction * SPEED, ACCELERATION * delta)
	else:
		velocity.x = move_toward(velocity.x, 0, FRICTION * delta)

	move_and_slide()

func _ready():
	print("Player ready!")

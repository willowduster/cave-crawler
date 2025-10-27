tool
extends EditorScript

/*
Simple EditorScript to assign a bundled font to enemy scenes under
`res://scenes/enemies`. It finds the first font in
`res://assets/fonts` (or a common filename) and sets the exported
`label_font` property on each PackedScene root.

Run from the Godot editor via Project -> Tools -> Run Editor Script,
or from command line with: godot --editor --script res://tools/editor/set_enemy_label_font.gd
*/

func _find_bundled_font():
    var candidates = [
        "res://assets/fonts/DejaVuSans.ttf",
        "res://assets/fonts/Roboto-Regular.ttf",
        "res://assets/fonts/NotoSans-Regular.ttf",
        "res://assets/fonts/Inter-Regular.ttf",
    ]
    # Also scan the folder for any ttf/otf
    var dir = DirAccess.open("res://assets/fonts")
    if dir:
        dir.list_dir_begin()
        var name = dir.get_next()
        while name != "":
            if not dir.current_is_dir():
                var lower = name.to_lower()
                if lower.ends_with(".ttf") or lower.ends_with(".otf"):
                    var p = "res://assets/fonts/" + name
                    if ResourceLoader.exists(p):
                        return load(p)
            name = dir.get_next()
        dir.list_dir_end()

    for p in candidates:
        if ResourceLoader.exists(p):
            return load(p)
    return null

func _patch_scene(scene_path: String, font: Resource) -> void:
    var res = ResourceLoader.load(scene_path)
    if res == null:
        printerr("Failed to load scene: %s" % scene_path)
        return
    if not res is PackedScene:
        printerr("Not a PackedScene: %s" % scene_path)
        return

    var inst = res.instantiate()
    if inst == null:
        printerr("Failed to instantiate scene: %s" % scene_path)
        return

    # Try setting the exported property; do best-effort.
    var did_set = false
    try:
        inst.set("label_font", font)
        did_set = true
    except:
        did_set = false

    if not did_set:
        printerr("Scene %s does not expose 'label_font' on root; skipping" % scene_path)
        return

    var packed = PackedScene.new()
    var err = packed.pack(inst)
    if err != OK:
        printerr("Failed to pack scene %s: %s" % [scene_path, err])
        return

    var save_err = ResourceSaver.save(scene_path, packed)
    if save_err != OK:
        printerr("Failed to save scene %s: %s" % [scene_path, save_err])
    else:
        print("Patched scene: %s -> label_font assigned" % scene_path)

func _run():
    print("Running set_enemy_label_font EditorScript...")
    var font = _find_bundled_font()
    if font == null:
        printerr("No bundled font found in res://assets/fonts. Drop a TTF/OTF into that folder and re-run.")
        return

    # Target directory
    var target_dir = "res://scenes/enemies"
    var dir = DirAccess.open(target_dir)
    if dir == null:
        printerr("Could not open directory: %s" % target_dir)
        return

    dir.list_dir_begin()
    var name = dir.get_next()
    var patched = 0
    while name != "":
        if not dir.current_is_dir() and name.to_lower().ends_with(".tscn"):
            var path = "%s/%s" % [target_dir, name]
            _patch_scene(path, font)
            patched += 1
        name = dir.get_next()
    dir.list_dir_end()

    print("set_enemy_label_font: completed. Scenes inspected: %d" % patched)

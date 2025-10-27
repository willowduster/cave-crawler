extends Node
class_name LeakTracker

# Simple runtime leak tracker for CanvasItems and Nodes.
# Create a root-level node named "LeakTracker" by instantiating this script at runtime.

var tracked := []

func register(obj: Object, tag: String = "") -> void:
    if obj == null:
        return
    tracked.append({"ref": obj, "tag": tag})

func unregister(obj: Object) -> void:
    for i in range(tracked.size() - 1, -1, -1):
        var entry = tracked[i]
        if entry["ref"] == obj:
            tracked.remove_at(i)

func _exit_tree() -> void:
    # Called when scene tree is exiting; report any remaining tracked objects
    var remaining = []
    for entry in tracked:
        var o = entry["ref"]
        if is_instance_valid(o):
            remaining.append(entry)

    if remaining.size() > 0:
        print("LEAK-TRACKER: Remaining tracked objects at exit: %d" % remaining.size())
        for e in remaining:
            var o = e["ref"]
            var tag = e.get("tag", "")
            print("LEAK-TRACKER: - %s (valid=%s) tag=%s" % [str(o), str(is_instance_valid(o)), tag])
    else:
        print("LEAK-TRACKER: No tracked objects remain at exit.")

func report_tracked() -> void:
    # Call explicitly after freeing resources to report any remaining tracked objects
    var remaining := []
    for entry in tracked:
        var o = entry["ref"]
        if is_instance_valid(o):
            remaining.append(entry)
    if remaining.size() > 0:
        print("LEAK-TRACKER: Remaining tracked objects: %d" % remaining.size())
        for e in remaining:
            var o = e["ref"]
            var tag = e.get("tag", "")
            print("LEAK-TRACKER: - %s (valid=%s) tag=%s" % [str(o), str(is_instance_valid(o)), tag])
    else:
        print("LEAK-TRACKER: No tracked objects remain.")

Repository Constitution
=======================

This repository follows a few small, explicit rules so contributors know where to expect build/runtime artifacts and how to run the project locally.

Rules
-----
- Godot editor/runtime binary: always placed in the repository root under `./bin/`.
  - The standard filename used by the run scripts is `Godot_v4.5.1-stable_win64.exe`.
- Use the project's run helper for consistent logging and arguments: `./scripts/run_godot_logged.ps1` (PowerShell) and any equivalent wrapper for other shells.
- When updating the Godot binary path or filename, update `scripts/run_godot_logged.ps1` and this document.

Why
---
Keeping a consistent convention for the runtime binary and the run helper reduces friction when running tests, capturing logs, or debugging locally and on CI.

How to run (Windows PowerShell)
--------------------------------
From the repository root:

```powershell
.\scripts\run_godot_logged.ps1 --path . scenes/levels/procedural_cave.tscn
```

If the binary is in a different location, update `scripts/run_godot_logged.ps1` to point to the correct path.

Additions
---------
If you'd like this rule changed (for example, to reference a symbolic link, environment variable, or a CI-installed binary), propose the change in a PR and update this document and the run helper together.

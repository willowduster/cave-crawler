Place an open-source TTF/OTF font in this folder to enable in-world enemy labels.

Recommended fonts (permissive/open-source):
- DejaVu Sans (https://dejavu-fonts.github.io/)
- Roboto (https://fonts.google.com/specimen/Roboto)
- Noto Sans (https://www.google.com/get/noto/)
- Inter (https://rsms.me/inter/)

Usage:
- Add a TTF file to this folder, e.g. `DejaVuSans.ttf`.
- The enemy label system will automatically detect common filenames and use the first one it finds.

If you prefer a specific font, edit `res://scripts/enemies/enemy_ai.gd` and change the `font_candidates` list or assign `label_font` directly in the enemy scene.

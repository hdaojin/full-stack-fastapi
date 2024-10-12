from pathlib import Path

# Path to the base directory of the app
BASE_DIR = Path(__file__).resolve().parents[2]  # src/ssr/core/path_config.py

# Path to ssr directory
SSR_DIR = BASE_DIR / "ssr"

# Path to the templates directory for SSR
TEMPLATES_DIR = SSR_DIR / "templates"

# Path to the static directory for SSR
STATIC_DIR = SSR_DIR / "static"




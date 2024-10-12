from pathlib import Path

# Path to the base directory of the app
BASE_DIR = Path(__file__).resolve().parents[2]  # src/app/core/path_config.py

# Path to the app directory
APP_DIR = BASE_DIR / "app"

# Path to the uploads directory
UPLOADS_DIR = BASE_DIR.parent / "uploads"






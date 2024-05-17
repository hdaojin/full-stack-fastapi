from pathlib import Path

# Path to the root directory of the project including the backend and frontend directories
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent  # full-stack-fastapi/backend/app/core/path_config.py

# Path to the root directory of the backend
ROOT_DIR = PROJECT_DIR / "backend"

# Path to the alembic directory
ALEMBIC_DIR = ROOT_DIR / "alembic"

# Path to the logs directory
LOGS_DIR = ROOT_DIR / "logs"

# Path to the uploads directory
UPLOADS_DIR = ROOT_DIR / "uploads"

# Path to the root directory of the frontend
FRONTEND_DIR = PROJECT_DIR / "frontend"

# Path to the templates directory
TEMPLATES_DIR = FRONTEND_DIR / "templates"

# Path to the STATIC directory
STATIC_DIR = FRONTEND_DIR / "static"

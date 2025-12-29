from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads" / "original"
OUTPUT_EXTRACT_DIR = DATA_DIR / "outputs" / "extract"
OUTPUT_TRYON_DIR = DATA_DIR / "outputs" / "tryon"
ASSETS_DIR = DATA_DIR / "assets"
PRESETS_DIR = DATA_DIR / "presets"

SQLITE_PATH = os.getenv("NAILART_DB", str(BASE_DIR / "app.db"))
SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_PATH}"

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_NAME = os.getenv("RQ_QUEUE", "nail_jobs")

STATIC_URL_PREFIX = "/static"

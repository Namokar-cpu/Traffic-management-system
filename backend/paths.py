from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = PROJECT_ROOT / "assets"
MODEL_PATH = ASSETS_DIR / "models" / "yolov8n.pt"
VIDEO_DIR = ASSETS_DIR / "videos"

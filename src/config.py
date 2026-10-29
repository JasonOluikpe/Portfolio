from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / 'assets'
MEDIA_DIR = ASSETS_DIR / 'media'
STYLES_FILE = Path(__file__).resolve().parent / 'styles.css'

STATIC_URL = '/static'

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_DIR = PROJECT_ROOT / "input"
REFERENCE_DIR = INPUT_DIR / "reference"
DEFECTIVE_DIR = INPUT_DIR / "defective"

OUTPUT_DIR = PROJECT_ROOT / "output"
ANNOTATED_DIR = OUTPUT_DIR / "annotated"
MASKS_DIR = OUTPUT_DIR / "masks"
HEATMAPS_DIR = OUTPUT_DIR / "heatmaps"
CROPS_DIR = OUTPUT_DIR / "crops"
REPORTS_DIR = OUTPUT_DIR / "reports"

VALID_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

MAX_DIM = 1600
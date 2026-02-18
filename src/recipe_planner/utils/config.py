"""Application-wide configuration settings."""

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = os.environ.get("RECIPE_DB_PATH", str(DATA_DIR / "recipe_planner.db"))
PDF_OUTPUT_DIR = os.environ.get("RECIPE_PDF_DIR", str(DATA_DIR / "exports"))
OCR_LANGUAGE = os.environ.get("RECIPE_OCR_LANG", "eng")
DEFAULT_SERVINGS = int(os.environ.get("RECIPE_DEFAULT_SERVINGS", "4"))

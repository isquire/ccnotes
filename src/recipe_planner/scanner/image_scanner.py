"""Extract recipe data from images using local OCR (pytesseract)."""

from __future__ import annotations

from pathlib import Path

from recipe_planner.models.recipe import Recipe
from recipe_planner.scanner.normalizer import normalize_ocr_text
from recipe_planner.scanner.text_scanner import extract_recipe_from_text
from recipe_planner.utils.config import OCR_LANGUAGE


def extract_recipe_from_image(image_path: str) -> Recipe:
    """Run local OCR on an image and extract recipe data.

    Requires pytesseract and Pillow to be installed, plus the
    tesseract-ocr system package.
    """
    try:
        import pytesseract
        from PIL import Image
    except ImportError as e:
        raise ImportError(
            "Image scanning requires pytesseract and Pillow. "
            "Install with: pip install pytesseract Pillow\n"
            "Also install tesseract-ocr: apt-get install tesseract-ocr"
        ) from e

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(path)
    raw_text = pytesseract.image_to_string(image, lang=OCR_LANGUAGE)
    cleaned_text = normalize_ocr_text(raw_text)
    recipe = extract_recipe_from_text(cleaned_text)

    recipe.confidence_notes.insert(
        0, f"Extracted via OCR from image: {path.name}"
    )

    return recipe

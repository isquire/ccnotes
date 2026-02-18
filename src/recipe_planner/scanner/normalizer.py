"""Post-OCR text normalization for recipe extraction."""

from __future__ import annotations

import re


def normalize_ocr_text(text: str) -> str:
    """Clean up common OCR artifacts in recipe text."""
    # Fix broken lines (rejoin words split across lines)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Normalize unicode fractions
    unicode_fracs = {
        "\u00bc": "1/4", "\u00bd": "1/2", "\u00be": "3/4",
        "\u2153": "1/3", "\u2154": "2/3",
        "\u2155": "1/5", "\u2156": "2/5", "\u2157": "3/5", "\u2158": "4/5",
        "\u2159": "1/6", "\u215a": "5/6",
        "\u215b": "1/8", "\u215c": "3/8", "\u215d": "5/8", "\u215e": "7/8",
    }
    for uf, af in unicode_fracs.items():
        text = text.replace(uf, af)

    # Fix common OCR fraction errors
    text = re.sub(r"(\d)\s*/\s*(\d)", r"\1/\2", text)  # "1/ 2" -> "1/2"

    # Normalize unit abbreviations
    unit_fixes = {
        r"\btbsps?\b": "tbsp",
        r"\bTbsps?\b": "tbsp",
        r"\bTBSPs?\b": "tbsp",
        r"\btablespoons?\b": "tbsp",
        r"\btsps?\b": "tsp",
        r"\bteaspoons?\b": "tsp",
        r"\bozs?\b": "oz",
        r"\blbs?\b": "lb",
    }
    for pattern, replacement in unit_fixes.items():
        text = re.sub(pattern, replacement, text)

    # Remove stray non-printable characters
    text = re.sub(r"[^\S\n ]+", " ", text)

    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

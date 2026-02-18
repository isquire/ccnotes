"""Shared PDF rendering primitives using fpdf2."""

from __future__ import annotations

import os
from pathlib import Path

from recipe_planner.utils.config import PDF_OUTPUT_DIR


def _ensure_output_dir() -> str:
    os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
    return PDF_OUTPUT_DIR


def get_pdf():
    """Create and return a configured FPDF instance."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    return pdf


def add_title(pdf, text: str) -> None:
    """Add a large title to the PDF."""
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)


def add_subtitle(pdf, text: str) -> None:
    """Add a subtitle/section header."""
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def add_body_text(pdf, text: str) -> None:
    """Add normal body text."""
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, text)
    pdf.ln(2)


def add_list_item(pdf, text: str, bullet: str = "-") -> None:
    """Add a bulleted list item."""
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(8)
    pdf.cell(0, 6, f"{bullet}  {text}", new_x="LMARGIN", new_y="NEXT")


def add_numbered_item(pdf, number: int, text: str) -> None:
    """Add a numbered list item."""
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(8)
    pdf.multi_cell(0, 6, f"{number}. {text}")
    pdf.ln(1)


def add_metadata_line(pdf, label: str, value: str) -> None:
    """Add a label: value metadata line."""
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(35, 6, f"{label}:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, value, new_x="LMARGIN", new_y="NEXT")


def add_horizontal_rule(pdf) -> None:
    """Add a horizontal line."""
    y = pdf.get_y()
    pdf.line(10, y, 200, y)
    pdf.ln(4)


def save_pdf(pdf, filename: str) -> str:
    """Save the PDF to the output directory. Returns the full path."""
    output_dir = _ensure_output_dir()
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)
    return filepath

"""CLI commands for scanning recipes from text or images."""

from __future__ import annotations

import json
import sys

import click

from recipe_planner.db.connection import get_connection
from recipe_planner.db.repositories.recipe_repo import save_recipe
from recipe_planner.scanner.text_scanner import extract_recipe_from_text
from recipe_planner.scanner.image_scanner import extract_recipe_from_image
from recipe_planner.categorizer.keyword_engine import classify_cuisine


@click.group()
def scan():
    """Scan and extract recipes from text or images."""
    pass


@scan.command("text")
@click.option("--file", "file_path", default=None, help="Path to text file (or use stdin)")
@click.option("--save/--no-save", default=True, help="Save the extracted recipe to the database")
@click.pass_context
def scan_text(ctx, file_path, save):
    """Extract a recipe from plain text."""
    if file_path:
        with open(file_path) as f:
            text = f.read()
    else:
        click.echo("Paste recipe text (Ctrl+D when done):")
        text = sys.stdin.read()

    if not text.strip():
        click.echo("No text provided.")
        return

    recipe = extract_recipe_from_text(text)

    # Auto-classify cuisine
    if not recipe.cuisine:
        recipe.cuisine = classify_cuisine(recipe)

    recipe.initialize_original_values()
    recipe.add_version_history_entry(["Scanned from text"])

    click.echo(json.dumps(recipe.to_dict(), indent=2))

    if save:
        db_path = ctx.obj.get("db_path")
        conn = get_connection(db_path)
        try:
            save_recipe(conn, recipe)
            conn.commit()
            click.echo(f"\nSaved recipe: {recipe.title} [{recipe.id[:8]}]")
        finally:
            conn.close()


@scan.command("image")
@click.argument("image_path")
@click.option("--save/--no-save", default=True, help="Save the extracted recipe to the database")
@click.pass_context
def scan_image(ctx, image_path, save):
    """Extract a recipe from an image using local OCR."""
    try:
        recipe = extract_recipe_from_image(image_path)
    except ImportError as e:
        click.echo(f"Error: {e}")
        return
    except FileNotFoundError as e:
        click.echo(f"Error: {e}")
        return

    # Auto-classify cuisine
    if not recipe.cuisine:
        recipe.cuisine = classify_cuisine(recipe)

    recipe.initialize_original_values()
    recipe.add_version_history_entry(["Scanned from image"])

    click.echo(json.dumps(recipe.to_dict(), indent=2))

    if save:
        db_path = ctx.obj.get("db_path")
        conn = get_connection(db_path)
        try:
            save_recipe(conn, recipe)
            conn.commit()
            click.echo(f"\nSaved recipe: {recipe.title} [{recipe.id[:8]}]")
        finally:
            conn.close()

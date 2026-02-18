"""CLI commands for recipe CRUD, version history, undo/redo."""

from __future__ import annotations

import json

import click

from recipe_planner.db.connection import get_connection
from recipe_planner.db.repositories.recipe_repo import (
    delete_recipe,
    get_recipe,
    list_recipes,
    save_recipe,
    search_recipes,
)
from recipe_planner.editor.version_manager import (
    apply_edit,
    jump_to_version,
    restore_all,
    restore_field,
)
from recipe_planner.editor.undo_redo import undo, redo, track_recipe
from recipe_planner.categorizer.keyword_engine import classify_cuisine
from recipe_planner.models.ingredient import Ingredient
from recipe_planner.models.recipe import Recipe


@click.group()
def recipe():
    """Manage recipes (add, edit, list, show, delete, history, undo, redo)."""
    pass


@recipe.command("add")
@click.option("--title", required=True, prompt=True, help="Recipe title")
@click.option("--cuisine", default="", help="Cuisine type")
@click.option("--prep-time", default=None, help="Prep time")
@click.option("--cook-time", default=None, help="Cook time")
@click.option("--tags", default="", help="Comma-separated tags")
@click.option("--ingredients", "ingredients_str", default="",
              help="Semicolon-separated ingredients (e.g., '2 cups flour; 1 tsp salt')")
@click.option("--instructions", "instructions_str", default="",
              help="Semicolon-separated instructions")
@click.option("--auto-classify/--no-auto-classify", default=True,
              help="Auto-classify cuisine")
@click.pass_context
def add(ctx, title, cuisine, prep_time, cook_time, tags, ingredients_str,
        instructions_str, auto_classify):
    """Add a new recipe."""
    from recipe_planner.utils.text_helpers import parse_ingredient_string

    ingredients = []
    if ingredients_str:
        for part in ingredients_str.split(";"):
            part = part.strip()
            if part:
                parsed = parse_ingredient_string(part)
                ingredients.append(Ingredient(
                    name=parsed["name"],
                    quantity=parsed["quantity"],
                    unit=parsed["unit"],
                ))

    instructions = []
    if instructions_str:
        instructions = [s.strip() for s in instructions_str.split(";") if s.strip()]

    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    new_recipe = Recipe(
        title=title,
        cuisine=cuisine,
        ingredients=ingredients,
        instructions=instructions,
        prep_time=prep_time,
        cook_time=cook_time,
        tags=tag_list,
    )

    # Auto-classify if no cuisine specified
    if auto_classify and not cuisine:
        new_recipe.cuisine = classify_cuisine(new_recipe)

    # Initialize original values and version history
    new_recipe.initialize_original_values()
    new_recipe.add_version_history_entry(["Initial creation"])

    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        save_recipe(conn, new_recipe)
        conn.commit()
        click.echo(json.dumps(new_recipe.to_dict(), indent=2))
    finally:
        conn.close()


@recipe.command("list")
@click.option("--cuisine", default=None, help="Filter by cuisine")
@click.option("--tag", default=None, help="Filter by tag")
@click.option("--order", default="date_added",
              type=click.Choice(["date_added", "date_modified", "title", "last_used", "times_used"]),
              help="Sort order")
@click.pass_context
def list_cmd(ctx, cuisine, tag, order):
    """List all recipes."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        recipes = list_recipes(conn, cuisine=cuisine, tag=tag, order_by=order)
        if not recipes:
            click.echo("No recipes found.")
            return
        for r in recipes:
            tags = ", ".join(r.tags) if r.tags else ""
            click.echo(f"  [{r.id[:8]}] {r.title} ({r.cuisine}) {tags}")
    finally:
        conn.close()


@recipe.command("show")
@click.argument("recipe_id")
@click.pass_context
def show(ctx, recipe_id):
    """Show full recipe details by ID (prefix match supported)."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        r = _find_recipe(conn, recipe_id)
        if not r:
            click.echo(f"Recipe not found: {recipe_id}")
            return
        click.echo(json.dumps(r.to_dict(), indent=2))
    finally:
        conn.close()


@recipe.command("edit")
@click.argument("recipe_id")
@click.option("--title", default=None, help="New title")
@click.option("--cuisine", default=None, help="New cuisine")
@click.option("--prep-time", default=None, help="New prep time")
@click.option("--cook-time", default=None, help="New cook time")
@click.option("--tags", default=None, help="New comma-separated tags")
@click.option("--ingredients", "ingredients_str", default=None,
              help="New semicolon-separated ingredients")
@click.option("--instructions", "instructions_str", default=None,
              help="New semicolon-separated instructions")
@click.pass_context
def edit(ctx, recipe_id, title, cuisine, prep_time, cook_time, tags,
         ingredients_str, instructions_str):
    """Edit a recipe field."""
    from recipe_planner.utils.text_helpers import parse_ingredient_string

    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        r = _find_recipe(conn, recipe_id)
        if not r:
            click.echo(f"Recipe not found: {recipe_id}")
            return

        changes = {}
        if title is not None:
            changes["title"] = title
        if cuisine is not None:
            changes["cuisine"] = cuisine
        if prep_time is not None:
            changes["prep_time"] = prep_time
        if cook_time is not None:
            changes["cook_time"] = cook_time
        if tags is not None:
            changes["tags"] = [t.strip() for t in tags.split(",") if t.strip()]
        if ingredients_str is not None:
            new_ings = []
            for part in ingredients_str.split(";"):
                part = part.strip()
                if part:
                    parsed = parse_ingredient_string(part)
                    new_ings.append({
                        "name": parsed["name"],
                        "quantity": parsed["quantity"],
                        "unit": parsed["unit"],
                    })
            changes["ingredients"] = new_ings
        if instructions_str is not None:
            changes["instructions"] = [
                s.strip() for s in instructions_str.split(";") if s.strip()
            ]

        if not changes:
            click.echo("No changes specified.")
            return

        r = apply_edit(r, changes)
        save_recipe(conn, r)
        conn.commit()
        click.echo(json.dumps(r.to_dict(), indent=2))
    finally:
        conn.close()


@recipe.command("delete")
@click.argument("recipe_id")
@click.confirmation_option(prompt="Are you sure you want to delete this recipe?")
@click.pass_context
def delete(ctx, recipe_id):
    """Delete a recipe by ID."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        r = _find_recipe(conn, recipe_id)
        if not r:
            click.echo(f"Recipe not found: {recipe_id}")
            return
        delete_recipe(conn, r.id)
        conn.commit()
        click.echo(f"Deleted recipe: {r.title}")
    finally:
        conn.close()


@recipe.command("history")
@click.argument("recipe_id")
@click.pass_context
def history(ctx, recipe_id):
    """Show version history for a recipe."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        r = _find_recipe(conn, recipe_id)
        if not r:
            click.echo(f"Recipe not found: {recipe_id}")
            return
        click.echo(f"Version history for: {r.title}")
        for entry in r.version_history:
            changes_str = ", ".join(entry.changes) if entry.changes else "No changes"
            click.echo(f"  v{entry.version} ({entry.timestamp}): {changes_str}")
    finally:
        conn.close()


@recipe.command("undo")
@click.argument("recipe_id")
@click.pass_context
def undo_cmd(ctx, recipe_id):
    """Undo the last edit on a recipe."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        r = _find_recipe(conn, recipe_id)
        if not r:
            click.echo(f"Recipe not found: {recipe_id}")
            return
        track_recipe(r)
        r = undo(r)
        save_recipe(conn, r)
        conn.commit()
        click.echo(json.dumps(r.to_dict(), indent=2))
    finally:
        conn.close()


@recipe.command("redo")
@click.argument("recipe_id")
@click.pass_context
def redo_cmd(ctx, recipe_id):
    """Redo the last undone edit on a recipe."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        r = _find_recipe(conn, recipe_id)
        if not r:
            click.echo(f"Recipe not found: {recipe_id}")
            return
        track_recipe(r)
        r = redo(r)
        save_recipe(conn, r)
        conn.commit()
        click.echo(json.dumps(r.to_dict(), indent=2))
    finally:
        conn.close()


@recipe.command("restore")
@click.argument("recipe_id")
@click.option("--field", default=None, help="Specific field to restore (or 'all')")
@click.option("--version", "version_num", default=None, type=int,
              help="Jump to specific version number")
@click.pass_context
def restore(ctx, recipe_id, field, version_num):
    """Restore a recipe field to original or jump to a version."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        r = _find_recipe(conn, recipe_id)
        if not r:
            click.echo(f"Recipe not found: {recipe_id}")
            return

        if version_num is not None:
            r = jump_to_version(r, version_num)
        elif field == "all":
            r = restore_all(r)
        elif field:
            r = restore_field(r, field)
        else:
            click.echo("Specify --field or --version")
            return

        save_recipe(conn, r)
        conn.commit()
        click.echo(json.dumps(r.to_dict(), indent=2))
    finally:
        conn.close()


@recipe.command("search")
@click.argument("query")
@click.pass_context
def search_cmd(ctx, query):
    """Search recipes by title or ingredient."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        results = search_recipes(conn, query)
        if not results:
            click.echo("No recipes found.")
            return
        for r in results:
            click.echo(f"  [{r.id[:8]}] {r.title} ({r.cuisine})")
    finally:
        conn.close()


def _find_recipe(conn, recipe_id: str):
    """Find a recipe by full or prefix ID."""
    r = get_recipe(conn, recipe_id)
    if r:
        return r
    # Try prefix match
    all_recipes = list_recipes(conn)
    for recipe in all_recipes:
        if recipe.id.startswith(recipe_id):
            return recipe
    return None

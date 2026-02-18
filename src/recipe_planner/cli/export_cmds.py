"""CLI commands for exporting to PDF."""

from __future__ import annotations

import click

from recipe_planner.db.connection import get_connection
from recipe_planner.db.repositories.recipe_repo import get_recipe, list_recipes
from recipe_planner.db.repositories.meal_plan_repo import get_meal_plan, list_meal_plans
from recipe_planner.db.repositories.shopping_list_repo import (
    get_shopping_list,
    list_shopping_lists,
)


@click.group()
def export():
    """Export recipes, meal plans, and shopping lists to PDF."""
    pass


@export.command("recipe")
@click.argument("recipe_id")
@click.option("--output", "-o", default=None, help="Output filename")
@click.pass_context
def export_recipe(ctx, recipe_id, output):
    """Export a recipe to PDF."""
    from recipe_planner.export.recipe_pdf import render_recipe_pdf

    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        r = _find_recipe(conn, recipe_id)
        if not r:
            click.echo(f"Recipe not found: {recipe_id}")
            return
        filepath = render_recipe_pdf(r, filename=output)
        click.echo(f"Recipe PDF saved to: {filepath}")
    finally:
        conn.close()


@export.command("plan")
@click.argument("plan_id")
@click.option("--output", "-o", default=None, help="Output filename")
@click.pass_context
def export_plan(ctx, plan_id, output):
    """Export a meal plan to PDF."""
    from recipe_planner.export.plan_pdf import render_plan_pdf

    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        mp = _find_plan(conn, plan_id)
        if not mp:
            click.echo(f"Meal plan not found: {plan_id}")
            return
        filepath = render_plan_pdf(mp, filename=output)
        click.echo(f"Meal plan PDF saved to: {filepath}")
    finally:
        conn.close()


@export.command("shoplist")
@click.argument("list_id")
@click.option("--output", "-o", default=None, help="Output filename")
@click.pass_context
def export_shoplist(ctx, list_id, output):
    """Export a shopping list to PDF."""
    from recipe_planner.export.shoplist_pdf import render_shopping_list_pdf

    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        sl = _find_list(conn, list_id)
        if not sl:
            click.echo(f"Shopping list not found: {list_id}")
            return
        filepath = render_shopping_list_pdf(sl, filename=output)
        click.echo(f"Shopping list PDF saved to: {filepath}")
    finally:
        conn.close()


def _find_recipe(conn, recipe_id):
    r = get_recipe(conn, recipe_id)
    if r:
        return r
    for recipe in list_recipes(conn):
        if recipe.id.startswith(recipe_id):
            return recipe
    return None


def _find_plan(conn, plan_id):
    mp = get_meal_plan(conn, plan_id)
    if mp:
        return mp
    for p in list_meal_plans(conn):
        if p.id.startswith(plan_id):
            return p
    return None


def _find_list(conn, list_id):
    sl = get_shopping_list(conn, list_id)
    if sl:
        return sl
    for s in list_shopping_lists(conn):
        if s.id.startswith(list_id):
            return s
    return None

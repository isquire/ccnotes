"""CLI commands for shopping list generation."""

from __future__ import annotations

import json

import click

from recipe_planner.db.connection import get_connection
from recipe_planner.db.repositories.meal_plan_repo import get_meal_plan, list_meal_plans
from recipe_planner.db.repositories.shopping_list_repo import (
    get_shopping_list,
    list_shopping_lists,
    save_shopping_list,
)
from recipe_planner.shopping.list_builder import collect_ingredients, collect_recipe_titles
from recipe_planner.shopping.merger import merge_ingredients
from recipe_planner.shopping.category_grouper import group_ingredients


@click.group()
def shoplist():
    """Generate and manage shopping lists."""
    pass


@shoplist.command("generate")
@click.argument("plan_id")
@click.pass_context
def generate(ctx, plan_id):
    """Generate a shopping list from a meal plan."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        # Find the meal plan
        mp = _find_plan(conn, plan_id)
        if not mp:
            click.echo(f"Meal plan not found: {plan_id}")
            return

        # Collect and merge ingredients
        raw_ingredients = collect_ingredients(mp, conn)
        if not raw_ingredients:
            click.echo("No ingredients found in the meal plan recipes.")
            return

        merged = merge_ingredients(raw_ingredients)
        shopping_list = group_ingredients(merged)

        # Add metadata
        shopping_list.metadata["recipes_included"] = collect_recipe_titles(mp)
        shopping_list.metadata["meal_plan_id"] = mp.id

        # Save
        save_shopping_list(conn, shopping_list, meal_plan_id=mp.id)
        conn.commit()

        click.echo(json.dumps(shopping_list.to_dict(), indent=2))
        click.echo(f"\nShopping list saved [{shopping_list.id[:8]}]")
    finally:
        conn.close()


@shoplist.command("show")
@click.argument("list_id")
@click.pass_context
def show(ctx, list_id):
    """Show a shopping list by ID."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        sl = _find_list(conn, list_id)
        if not sl:
            click.echo(f"Shopping list not found: {list_id}")
            return
        click.echo(json.dumps(sl.to_dict(), indent=2))
    finally:
        conn.close()


@shoplist.command("list")
@click.pass_context
def list_cmd(ctx):
    """List all shopping lists."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        lists = list_shopping_lists(conn)
        if not lists:
            click.echo("No shopping lists found.")
            return
        for sl in lists:
            num_items = len(sl.raw_items)
            gen_date = sl.metadata.get("generated_on", "unknown")
            click.echo(f"  [{sl.id[:8]}] {gen_date} ({num_items} items)")
    finally:
        conn.close()


def _find_plan(conn, plan_id):
    from recipe_planner.db.repositories.meal_plan_repo import get_meal_plan, list_meal_plans
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

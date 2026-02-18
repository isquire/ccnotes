"""CLI commands for meal plan generation and management."""

from __future__ import annotations

import json

import click

from recipe_planner.db.connection import get_connection
from recipe_planner.db.repositories.meal_plan_repo import (
    delete_meal_plan,
    get_meal_plan,
    list_meal_plans,
    save_meal_plan,
)
from recipe_planner.db.repositories.recipe_repo import list_recipes, save_recipe
from recipe_planner.planner.meal_planner import generate_meal_plan


@click.group()
def plan():
    """Generate and manage weekly meal plans."""
    pass


@plan.command("generate")
@click.option("--start-date", default=None, help="Start date YYYY-MM-DD (defaults to next Saturday)")
@click.option("--cuisine", default=None, help="Filter recipes by cuisine")
@click.pass_context
def generate(ctx, start_date, cuisine):
    """Generate a new 8-day meal plan (Saturday to Sunday)."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        recipes = list_recipes(conn, cuisine=cuisine)
        if not recipes:
            click.echo("No recipes available. Add some recipes first.")
            return

        meal_plan = generate_meal_plan(recipes, start_date=start_date)

        # Update recipe usage stats
        for recipe_title in meal_plan.recipes_used:
            for r in recipes:
                if r.title == recipe_title:
                    r.last_used_in_meal_plan = meal_plan.metadata.get("generated_on", "")
                    r.times_used += 1
                    save_recipe(conn, r)
                    break

        save_meal_plan(conn, meal_plan)
        conn.commit()

        click.echo(json.dumps(meal_plan.to_dict(), indent=2))
        click.echo(f"\nMeal plan saved [{meal_plan.id[:8]}]")
    finally:
        conn.close()


@plan.command("show")
@click.argument("plan_id")
@click.pass_context
def show(ctx, plan_id):
    """Show a meal plan by ID."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        mp = _find_plan(conn, plan_id)
        if not mp:
            click.echo(f"Meal plan not found: {plan_id}")
            return
        click.echo(json.dumps(mp.to_dict(), indent=2))
    finally:
        conn.close()


@plan.command("list")
@click.pass_context
def list_cmd(ctx):
    """List all meal plans."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        plans = list_meal_plans(conn)
        if not plans:
            click.echo("No meal plans found.")
            return
        for mp in plans:
            num_recipes = len(mp.recipes_used)
            click.echo(
                f"  [{mp.id[:8]}] {mp.start_date} to {mp.end_date} "
                f"({num_recipes} recipes)"
            )
    finally:
        conn.close()


@plan.command("delete")
@click.argument("plan_id")
@click.confirmation_option(prompt="Are you sure?")
@click.pass_context
def delete(ctx, plan_id):
    """Delete a meal plan."""
    db_path = ctx.obj.get("db_path")
    conn = get_connection(db_path)
    try:
        mp = _find_plan(conn, plan_id)
        if not mp:
            click.echo(f"Meal plan not found: {plan_id}")
            return
        delete_meal_plan(conn, mp.id)
        conn.commit()
        click.echo(f"Deleted meal plan: {mp.start_date} to {mp.end_date}")
    finally:
        conn.close()


def _find_plan(conn, plan_id: str):
    """Find a meal plan by full or prefix ID."""
    mp = get_meal_plan(conn, plan_id)
    if mp:
        return mp
    all_plans = list_meal_plans(conn)
    for p in all_plans:
        if p.id.startswith(plan_id):
            return p
    return None

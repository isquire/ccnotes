"""Main CLI entry point for the Recipe Planner."""

from __future__ import annotations

import click

from recipe_planner.db.connection import init_db


@click.group()
@click.option("--db-path", envvar="RECIPE_DB_PATH", default=None,
              help="Path to the SQLite database.")
@click.pass_context
def main(ctx, db_path):
    """Local Recipe Scanner, Meal Planner & Editing Engine."""
    ctx.ensure_object(dict)
    ctx.obj["db_path"] = db_path
    init_db(db_path)


# Import and register subcommand groups
from recipe_planner.cli.recipe_cmds import recipe  # noqa: E402
from recipe_planner.cli.scan_cmds import scan  # noqa: E402
from recipe_planner.cli.plan_cmds import plan  # noqa: E402
from recipe_planner.cli.shoplist_cmds import shoplist  # noqa: E402
from recipe_planner.cli.export_cmds import export  # noqa: E402

main.add_command(recipe)
main.add_command(scan)
main.add_command(plan)
main.add_command(shoplist)
main.add_command(export)


if __name__ == "__main__":
    main()

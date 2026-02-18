"""Tests for recipe repository CRUD operations."""

from recipe_planner.db.repositories.recipe_repo import (
    delete_recipe,
    get_recipe,
    get_recipe_by_title,
    list_recipes,
    save_recipe,
    search_recipes,
)


def test_save_and_get_recipe(conn, sample_recipe):
    save_recipe(conn, sample_recipe)
    conn.commit()

    loaded = get_recipe(conn, sample_recipe.id)
    assert loaded is not None
    assert loaded.title == "Classic Spaghetti Bolognese"
    assert loaded.cuisine == "Italian"
    assert len(loaded.ingredients) == 9
    assert len(loaded.instructions) == 7
    assert loaded.version == 1


def test_get_recipe_by_title(conn, sample_recipe):
    save_recipe(conn, sample_recipe)
    conn.commit()

    loaded = get_recipe_by_title(conn, "classic spaghetti bolognese")
    assert loaded is not None
    assert loaded.id == sample_recipe.id


def test_list_recipes_no_filter(conn, sample_recipes):
    for r in sample_recipes:
        save_recipe(conn, r)
    conn.commit()

    results = list_recipes(conn)
    assert len(results) == 5


def test_list_recipes_filter_cuisine(conn, sample_recipes):
    for r in sample_recipes:
        save_recipe(conn, r)
    conn.commit()

    results = list_recipes(conn, cuisine="Italian")
    assert all(r.cuisine == "Italian" for r in results)


def test_search_recipes(conn, sample_recipe):
    save_recipe(conn, sample_recipe)
    conn.commit()

    results = search_recipes(conn, "spaghetti")
    assert len(results) >= 1
    assert any("Spaghetti" in r.title for r in results)


def test_delete_recipe(conn, sample_recipe):
    save_recipe(conn, sample_recipe)
    conn.commit()

    assert delete_recipe(conn, sample_recipe.id) is True
    conn.commit()

    assert get_recipe(conn, sample_recipe.id) is None


def test_version_history_persists(conn, sample_recipe):
    save_recipe(conn, sample_recipe)
    conn.commit()

    loaded = get_recipe(conn, sample_recipe.id)
    assert len(loaded.version_history) == 1
    assert loaded.version_history[0].version == 1


def test_original_values_persist(conn, sample_recipe):
    save_recipe(conn, sample_recipe)
    conn.commit()

    loaded = get_recipe(conn, sample_recipe.id)
    assert loaded.original_values["title"] == "Classic Spaghetti Bolognese"
    assert len(loaded.original_values["ingredients"]) == 9

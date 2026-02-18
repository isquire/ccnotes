"""Shared test fixtures."""

import pytest
import sqlite3

from recipe_planner.db.connection import init_db, get_connection
from recipe_planner.models.ingredient import Ingredient
from recipe_planner.models.recipe import Recipe


@pytest.fixture
def db_path(tmp_path):
    """Provide a temporary database path."""
    path = str(tmp_path / "test.db")
    init_db(path)
    return path


@pytest.fixture
def conn(db_path):
    """Provide a database connection to a test database."""
    connection = get_connection(db_path)
    yield connection
    connection.close()


@pytest.fixture
def sample_recipe():
    """Create a sample recipe for testing."""
    recipe = Recipe(
        title="Classic Spaghetti Bolognese",
        cuisine="Italian",
        ingredients=[
            Ingredient(name="spaghetti", quantity="1", unit="lb"),
            Ingredient(name="ground beef", quantity="1", unit="lb"),
            Ingredient(name="tomato sauce", quantity="2", unit="cup"),
            Ingredient(name="onion", quantity="1", unit=None),
            Ingredient(name="garlic", quantity="3", unit="clove"),
            Ingredient(name="olive oil", quantity="2", unit="tbsp"),
            Ingredient(name="salt", quantity="1", unit="tsp"),
            Ingredient(name="pepper", quantity="0.5", unit="tsp"),
            Ingredient(name="oregano", quantity="1", unit="tsp"),
        ],
        instructions=[
            "Boil water and cook spaghetti according to package directions.",
            "In a large skillet, heat olive oil over medium heat.",
            "Add onion and garlic, sauté until softened.",
            "Add ground beef and cook until browned.",
            "Add tomato sauce, salt, pepper, and oregano.",
            "Simmer for 20 minutes.",
            "Serve sauce over spaghetti.",
        ],
        prep_time="10 minutes",
        cook_time="30 minutes",
        tags=["pasta", "dinner", "Italian"],
    )
    recipe.initialize_original_values()
    recipe.add_version_history_entry(["Initial creation"])
    return recipe


@pytest.fixture
def sample_recipes():
    """Create a list of sample recipes for testing meal plans."""
    recipes = []
    data = [
        ("Pancakes", "American", [
            Ingredient("flour", "2", "cup"),
            Ingredient("milk", "1.5", "cup"),
            Ingredient("egg", "2", None),
            Ingredient("butter", "2", "tbsp"),
        ], ["Mix dry ingredients", "Add wet ingredients", "Cook on griddle"]),
        ("Caesar Salad", "Mediterranean", [
            Ingredient("romaine lettuce", "1", "head"),
            Ingredient("parmesan", "0.5", "cup"),
            Ingredient("croutons", "1", "cup"),
        ], ["Chop lettuce", "Add dressing", "Top with croutons and parmesan"]),
        ("Chicken Curry", "Indian", [
            Ingredient("chicken breast", "2", "lb"),
            Ingredient("curry powder", "2", "tbsp"),
            Ingredient("coconut milk", "1", "can"),
            Ingredient("onion", "1", None),
            Ingredient("garlic", "4", "clove"),
        ], ["Sauté onion and garlic", "Add chicken", "Add curry and coconut milk", "Simmer 25 min"]),
        ("Tacos", "Mexican", [
            Ingredient("ground beef", "1", "lb"),
            Ingredient("tortilla", "8", None),
            Ingredient("salsa", "1", "cup"),
            Ingredient("cheese", "1", "cup"),
        ], ["Cook beef with seasoning", "Warm tortillas", "Assemble tacos"]),
        ("Stir Fry", "Asian", [
            Ingredient("tofu", "1", "lb"),
            Ingredient("soy sauce", "3", "tbsp"),
            Ingredient("broccoli", "2", "cup"),
            Ingredient("rice", "2", "cup"),
        ], ["Press tofu", "Stir fry vegetables", "Add sauce", "Serve over rice"]),
    ]

    for title, cuisine, ings, instructions in data:
        r = Recipe(
            title=title,
            cuisine=cuisine,
            ingredients=ings,
            instructions=instructions,
            tags=[cuisine.lower()],
        )
        r.initialize_original_values()
        r.add_version_history_entry(["Initial creation"])
        recipes.append(r)

    return recipes

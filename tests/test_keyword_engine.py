"""Tests for cuisine classification."""

from recipe_planner.categorizer.keyword_engine import classify_cuisine, get_cuisine_scores
from recipe_planner.models.ingredient import Ingredient
from recipe_planner.models.recipe import Recipe


def test_classify_italian():
    recipe = Recipe(
        title="Spaghetti Carbonara",
        ingredients=[
            Ingredient("spaghetti", "1", "lb"),
            Ingredient("pancetta", "6", "oz"),
            Ingredient("parmesan", "1", "cup"),
            Ingredient("egg", "4", None),
        ],
        instructions=["Cook pasta", "Make sauce with eggs and cheese"],
    )
    assert classify_cuisine(recipe) == "Italian"


def test_classify_mexican():
    recipe = Recipe(
        title="Chicken Tacos",
        ingredients=[
            Ingredient("tortilla", "8", None),
            Ingredient("salsa", "1", "cup"),
            Ingredient("avocado", "2", None),
            Ingredient("cilantro", "0.25", "cup"),
            Ingredient("lime", "2", None),
        ],
        instructions=["Cook chicken", "Assemble tacos"],
    )
    assert classify_cuisine(recipe) == "Mexican"


def test_classify_indian():
    recipe = Recipe(
        title="Chicken Tikka Masala",
        ingredients=[
            Ingredient("chicken", "2", "lb"),
            Ingredient("garam masala", "2", "tsp"),
            Ingredient("turmeric", "1", "tsp"),
            Ingredient("naan", "4", None),
        ],
        instructions=["Marinate chicken", "Cook in masala sauce"],
    )
    assert classify_cuisine(recipe) == "Indian"


def test_classify_unknown_returns_other():
    recipe = Recipe(
        title="Mystery Dish",
        ingredients=[Ingredient("mystery ingredient", "1", None)],
        instructions=["Do something"],
    )
    assert classify_cuisine(recipe) == "Other/Fusion"


def test_get_cuisine_scores_returns_ranked():
    recipe = Recipe(
        title="Pasta with Soy Sauce",
        ingredients=[
            Ingredient("pasta", "1", "lb"),
            Ingredient("soy sauce", "2", "tbsp"),
            Ingredient("parmesan", "0.5", "cup"),
        ],
        instructions=["Cook pasta", "Add soy sauce and cheese"],
    )
    scores = get_cuisine_scores(recipe)
    assert len(scores) >= 1
    # Should have both Italian and Asian scores
    cuisines = [s[0] for s in scores]
    assert "Italian" in cuisines
    assert "Asian" in cuisines

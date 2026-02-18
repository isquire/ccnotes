"""Tests for ingredient category grouping."""

from recipe_planner.models.ingredient import Ingredient
from recipe_planner.shopping.category_grouper import categorize_ingredient, group_ingredients


def test_categorize_produce():
    ing = Ingredient("tomato", "2", None)
    assert categorize_ingredient(ing) == "Produce"


def test_categorize_meat():
    ing = Ingredient("chicken breast", "2", "lb")
    assert categorize_ingredient(ing) == "Meat & Seafood"


def test_categorize_dairy():
    ing = Ingredient("butter", "2", "tbsp")
    assert categorize_ingredient(ing) == "Dairy"


def test_categorize_pantry():
    ing = Ingredient("flour", "2", "cup")
    assert categorize_ingredient(ing) == "Pantry"


def test_categorize_spice():
    ing = Ingredient("cumin", "1", "tsp")
    assert categorize_ingredient(ing) == "Spices"


def test_categorize_unknown():
    ing = Ingredient("dragon fruit extract", "1", "tsp")
    assert categorize_ingredient(ing) == "Other"


def test_categorize_with_preset_category():
    ing = Ingredient("special item", "1", None, category="Frozen")
    assert categorize_ingredient(ing) == "Frozen"


def test_group_ingredients():
    ingredients = [
        Ingredient("tomato", "2", None),
        Ingredient("chicken breast", "1", "lb"),
        Ingredient("butter", "2", "tbsp"),
        Ingredient("cumin", "1", "tsp"),
    ]
    shopping_list = group_ingredients(ingredients)
    assert "Produce" in shopping_list.categories
    assert "Meat & Seafood" in shopping_list.categories
    assert "Dairy" in shopping_list.categories
    assert "Spices" in shopping_list.categories
    assert len(shopping_list.raw_items) == 4

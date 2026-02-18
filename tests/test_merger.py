"""Tests for ingredient merging."""

from recipe_planner.models.ingredient import Ingredient
from recipe_planner.shopping.merger import merge_ingredients


def test_merge_same_ingredient_same_unit():
    ingredients = [
        Ingredient("flour", "2", "cup"),
        Ingredient("flour", "1", "cup"),
    ]
    merged = merge_ingredients(ingredients)
    assert len(merged) == 1
    assert merged[0].name == "flour"
    assert merged[0].quantity == "3"


def test_merge_different_ingredients():
    ingredients = [
        Ingredient("flour", "2", "cup"),
        Ingredient("sugar", "1", "cup"),
    ]
    merged = merge_ingredients(ingredients)
    assert len(merged) == 2


def test_merge_no_unit():
    ingredients = [
        Ingredient("egg", "2", None),
        Ingredient("egg", "3", None),
    ]
    merged = merge_ingredients(ingredients)
    assert len(merged) == 1
    assert merged[0].quantity == "5"


def test_merge_single_ingredient():
    ingredients = [Ingredient("salt", "1", "tsp")]
    merged = merge_ingredients(ingredients)
    assert len(merged) == 1
    assert merged[0].name == "salt"


def test_merge_case_insensitive():
    ingredients = [
        Ingredient("Flour", "2", "cup"),
        Ingredient("flour", "1", "cup"),
    ]
    merged = merge_ingredients(ingredients)
    assert len(merged) == 1

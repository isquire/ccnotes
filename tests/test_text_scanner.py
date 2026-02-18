"""Tests for text-based recipe extraction."""

from recipe_planner.scanner.text_scanner import extract_recipe_from_text


def test_extract_basic_recipe():
    text = """
    Classic Pancakes

    Ingredients:
    - 2 cups all-purpose flour
    - 2 eggs
    - 1 1/2 cups milk
    - 2 tbsp butter

    Instructions:
    1. Mix dry ingredients in a bowl
    2. Add wet ingredients and stir until combined
    3. Cook on a hot griddle until bubbles form
    4. Flip and cook other side

    Prep time: 5 minutes
    Cook time: 15 minutes
    """
    recipe = extract_recipe_from_text(text)

    assert recipe.title == "Classic Pancakes"
    assert len(recipe.ingredients) == 4
    assert len(recipe.instructions) == 4
    assert recipe.prep_time == "5 minutes"
    assert recipe.cook_time == "15 minutes"


def test_extract_recipe_with_markdown_headers():
    text = """
    # Garlic Bread

    ## Ingredients
    - 1 baguette
    - 4 cloves garlic
    - 3 tbsp butter

    ## Instructions
    1. Preheat oven to 375F
    2. Mix garlic and butter
    3. Spread on bread and bake 10 minutes
    """
    recipe = extract_recipe_from_text(text)

    assert recipe.title == "Garlic Bread"
    assert len(recipe.ingredients) == 3
    assert len(recipe.instructions) == 3


def test_extract_handles_empty_text():
    recipe = extract_recipe_from_text("")
    assert recipe.title == "Untitled Recipe"
    assert recipe.confidence_notes  # Should have notes about missing sections


def test_extract_ingredients_have_quantities():
    text = """
    Simple Salad

    Ingredients:
    - 2 cups lettuce
    - 1/2 cup cheese
    - 3 tbsp dressing

    Instructions:
    1. Toss everything together
    """
    recipe = extract_recipe_from_text(text)
    assert recipe.ingredients[0].quantity == "2"
    assert recipe.ingredients[0].unit == "cups"
    assert recipe.ingredients[0].name == "lettuce"

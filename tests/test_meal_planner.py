"""Tests for meal plan generation."""

from recipe_planner.planner.meal_planner import generate_meal_plan, DAY_ORDER


def test_generate_meal_plan(sample_recipes):
    plan = generate_meal_plan(sample_recipes, start_date="2026-02-21")
    assert plan.start_date == "2026-02-21"
    assert plan.end_date == "2026-02-28"
    assert len(plan.days) == 8  # 8 days: Sat -> next Sun
    assert len(plan.recipes_used) > 0


def test_plan_has_all_meal_types(sample_recipes):
    plan = generate_meal_plan(sample_recipes, start_date="2026-02-21")
    for day in DAY_ORDER:
        assert day in plan.days
        meals = plan.days[day]
        assert "breakfast" in meals
        assert "lunch" in meals
        assert "dinner" in meals


def test_plan_uses_recipe_titles(sample_recipes):
    plan = generate_meal_plan(sample_recipes, start_date="2026-02-21")
    recipe_titles = {r.title for r in sample_recipes}
    for recipe_used in plan.recipes_used:
        assert recipe_used in recipe_titles


def test_empty_recipes_raises():
    import pytest
    with pytest.raises(ValueError, match="no recipes"):
        generate_meal_plan([], start_date="2026-02-21")


def test_plan_metadata(sample_recipes):
    plan = generate_meal_plan(sample_recipes, start_date="2026-02-21")
    assert "generated_on" in plan.metadata
    assert "notes" in plan.metadata

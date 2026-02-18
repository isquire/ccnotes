"""Tests for unit conversion utilities."""

from recipe_planner.utils.unit_converter import (
    can_convert,
    convert,
    normalize_unit,
    parse_quantity,
)


def test_normalize_unit():
    assert normalize_unit("teaspoons") == "tsp"
    assert normalize_unit("tablespoon") == "tbsp"
    assert normalize_unit("cups") == "cup"
    assert normalize_unit("pounds") == "lb"
    assert normalize_unit("grams") == "g"
    assert normalize_unit(None) is None


def test_parse_quantity_integer():
    assert parse_quantity("2") == 2.0


def test_parse_quantity_fraction():
    assert parse_quantity("1/2") == 0.5


def test_parse_quantity_mixed_fraction():
    assert parse_quantity("1 1/2") == 1.5


def test_parse_quantity_empty():
    assert parse_quantity("") == 0.0


def test_can_convert_same_unit():
    assert can_convert("cup", "cup") is True


def test_can_convert_volume_units():
    assert can_convert("cup", "tbsp") is True
    assert can_convert("tsp", "ml") is True


def test_can_convert_weight_units():
    assert can_convert("lb", "oz") is True
    assert can_convert("g", "kg") is True


def test_cannot_convert_volume_to_weight():
    assert can_convert("cup", "lb") is False


def test_convert_tsp_to_tbsp():
    result = convert(3.0, "tsp", "tbsp")
    assert result is not None
    assert abs(result - 1.0) < 0.1


def test_convert_lb_to_oz():
    result = convert(1.0, "lb", "oz")
    assert result is not None
    assert abs(result - 16.0) < 0.1


def test_convert_same_unit():
    assert convert(5.0, "cup", "cup") == 5.0


def test_convert_incompatible_returns_none():
    assert convert(1.0, "cup", "lb") is None

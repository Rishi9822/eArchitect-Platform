from app.calculators.quantity_calculator import QuantityCalculator

import json
from pathlib import Path

from app.calculators.quantity_calculator import QuantityCalculator
from app.core.constants import FT_TO_M, IN_TO_M, DEFAULT_PLASTER_THICKNESS_M

def test_flooring_quantity_includes_wastage():
    calculator = QuantityCalculator()

    result = calculator.calculate_flooring_quantity(1500)

    assert result["base_quantity"] == 1500.0
    assert result["wastage_percent"] == 5.0
    assert result["wastage_quantity"] == 75.0
    assert result["total_quantity"] == 1575.0


def test_masonry_quantity_includes_wastage():
    calculator = QuantityCalculator()

    result = calculator.calculate_masonry_quantity(
        wall_length_ft=420,
        wall_height_ft=10,
        wall_thickness_in=9,
    )

    assert result["base_quantity"] == 89.198
    assert result["wastage_percent"] == 5.0
    assert result["wastage_quantity"] == 4.46
    assert result["total_quantity"] == 93.658


def test_bricks_inherit_masonry_wastage():
    calculator = QuantityCalculator()

    result = calculator.calculate_brick_quantity(93.658)

    assert result["brick_count"] == 46829
    assert result["wastage_included"] is True
    assert result["wastage_source"] == "masonry"


def test_mortar_quantity_includes_wastage():
    calculator = QuantityCalculator()

    result = calculator.calculate_mortar_quantity(
        masonry_volume_m3=93.658,
        brick_count=46829,
    )

    assert result["wastage_percent"] == 5.0
    assert result["wastage_quantity"] == 1.079
    assert result["total_quantity"] == 22.668


def test_plaster_quantity_includes_wastage():
    calculator = QuantityCalculator()

    result = calculator.calculate_plaster_quantity(
        wall_length_ft=420,
        wall_height_ft=10,
    )

    assert result["wastage_percent"] == 5.0
    assert result["wastage_quantity"] == 0.468
    assert result["total_quantity"] == 9.833


def test_concrete_quantity_includes_wastage():
    calculator = QuantityCalculator()

    base = calculator.calculate_concrete_volume(1500)

    result = calculator.calculate_concrete_materials(
        base["base_quantity"]
    )

    assert result["base_quantity"] == 52.5
    assert result["wastage_percent"] == 5.0
    assert result["wastage_quantity"] == 2.625
    assert result["total_quantity"] == 55.125


def test_steel_quantity_includes_wastage():
    calculator = QuantityCalculator()

    result = calculator.calculate_steel_quantity(1500)

    assert result["base_quantity"] == 6000.0
    assert result["wastage_percent"] == 5.0
    assert result["wastage_quantity"] == 300.0
    assert result["total_quantity"] == 6300.0
    assert result["quantity_tonnes"] == 6.3




def test_layout_quantity_uses_engine_measurements():
    fixture_path = (
        Path(__file__).parent
        / "fixtures"
        / "layout_candidate.json"
    )

    with open(fixture_path, "r", encoding="utf-8") as file:
        layout = json.load(file)

    project = {
        "built_up_area_sqft": 1500,
        "wall_length_ft": 420,
        "ceiling_height_ft": 10,
        "rooms": 3,
        "bathrooms": 2,
        "wall_thickness_in": 9,
        "flooring": "standard",
        "city": "Nagpur",
        "finish_tier": "standard",
    }

    calculator = QuantityCalculator()

    result = calculator.calculate_layout(project, layout)

    assert result["mode"] == "layout"
    assert len(result["materials"]) == 7
    flooring = result["materials"][0]

    assert flooring["material"] == "flooring"
    assert flooring["base_quantity"] == 1500.0
    assert flooring["total_quantity"] == 1575.0

    concrete = next(
        item
        for item in result["materials"]
        if item["material"] == "concrete"
    )

    steel = next(
        item
        for item in result["materials"]
        if item["material"] == "reinforcement_steel"
    )

    assert concrete["base_quantity"] == 52.5
    assert concrete["total_quantity"] == 55.125

    assert steel["base_quantity"] == 6000.0
    assert steel["total_quantity"] == 6300.0

    masonry = next(
        item
        for item in result["materials"]
        if item["material"] == "masonry"
    )

    expected_wall_length_ft = 80.0 / 0.3048

    expected_wall_length_m = 80.0

    expected_wall_height_m = (
        project["ceiling_height_ft"] * FT_TO_M
    )

    expected_wall_thickness_m = (
        project["wall_thickness_in"] * IN_TO_M
    )

    expected_wall_volume_m3 = (
        expected_wall_length_m
        * expected_wall_height_m
        * expected_wall_thickness_m
    )

    expected_wall_volume_with_wastage = (
        expected_wall_volume_m3 * 1.05
    )

    assert masonry["base_quantity"] == round(
        expected_wall_volume_m3,
        3,
    )

    assert masonry["total_quantity"] == round(
        expected_wall_volume_with_wastage,
        3,
    )

    bricks = next(
        item
        for item in result["materials"]
        if item["material"] == "bricks"
    )

    mortar = next(
        item
        for item in result["materials"]
        if item["material"] == "mortar"
    )

    assert bricks["brick_count"] > 0
    assert bricks["brick_unit"] == "pieces"
    assert bricks["wastage_included"] is True

    assert mortar["total_quantity"] >= mortar["base_quantity"]
    assert mortar["total_unit"] == "m3"
    assert mortar["mix_ratio"] == "1:6"

    plaster = next(
        item
        for item in result["materials"]
        if item["material"] == "plaster"
    )

    expected_wall_surface_area_sqm = (
        80.0
        * project["ceiling_height_ft"]
        * FT_TO_M
        * 2
    )

    expected_plaster_base_volume_m3 = (
        expected_wall_surface_area_sqm
        * DEFAULT_PLASTER_THICKNESS_M
    )

    expected_plaster_total_volume_m3 = (
        expected_plaster_base_volume_m3 * 1.05
    )

    assert plaster["base_quantity"] == round(
        expected_plaster_base_volume_m3,
        3,
    )

    assert plaster["total_quantity"] == round(
        expected_plaster_total_volume_m3,
        3,
    )

    assert plaster["mix_ratio"] == "1:4"
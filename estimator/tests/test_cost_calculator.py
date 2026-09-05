import json
from pathlib import Path

from app.calculators.cost_calculator import CostCalculator
from app.calculators.quantity_calculator import QuantityCalculator


def test_steel_cost_uses_total_quantity():
    calculator = CostCalculator()

    materials = [
        {
            "material": "reinforcement_steel",
            "base_quantity": 6000.0,
            "wastage_percent": 5.0,
            "wastage_quantity": 300.0,
            "total_quantity": 6300.0,
        }
    ]

    result = calculator.calculate_material_costs(
        materials=materials,
        city="Nagpur",
        finish_tier="standard",
    )

    assert len(result) == 1
    assert result[0]["quantity"] == 6300.0
    assert result[0]["rate"] == 65.0
    assert result[0]["total_cost"] == 409500.0


def test_concrete_components_are_priced():
    calculator = CostCalculator()

    materials = [
        {
            "material": "concrete",
            "base_quantity": 52.5,
            "wastage_percent": 5.0,
            "wastage_quantity": 2.625,
            "total_quantity": 55.125,
            "cement": {"quantity": 349.27},
            "sand": {"quantity": 24.255},
            "aggregate": {"quantity": 48.51},
        }
    ]

    result = calculator.calculate_material_costs(
        materials=materials,
        city="Nagpur",
        finish_tier="standard",
    )

    assert len(result) == 3

    costs = {
        item["material"]: item["total_cost"]
        for item in result
    }

    assert costs["cement"] == 146693.4
    assert costs["sand"] == 43659.0
    assert costs["aggregate"] == 77616.0


def test_masonry_is_not_directly_priced():
    calculator = CostCalculator()

    materials = [
        {
            "material": "masonry",
            "total_quantity": 93.658,
        }
    ]

    result = calculator.calculate_material_costs(
        materials=materials,
        city="Nagpur",
        finish_tier="standard",
    )

    assert result == []


def test_duplicate_materials_are_aggregated():
    calculator = CostCalculator()

    material_costs = [
        {
            "material": "cement",
            "city": "Nagpur",
            "finish_tier": "standard",
            "rate": 420.0,
            "unit": "bag",
            "quantity": 100.0,
            "total_cost": 42000.0,
            "source": "mortar",
        },
        {
            "material": "cement",
            "city": "Nagpur",
            "finish_tier": "standard",
            "rate": 420.0,
            "unit": "bag",
            "quantity": 200.0,
            "total_cost": 84000.0,
            "source": "concrete",
        },
    ]

    result = calculator.aggregate_material_costs(
        material_costs
    )

    assert len(result) == 1
    assert result[0]["material"] == "cement"
    assert result[0]["quantity"] == 300.0
    assert result[0]["total_cost"] == 126000.0
    assert len(result[0]["breakdown"]) == 2


def test_full_material_cost_total():
    calculator = CostCalculator()

    material_costs = [
        {
            "material": "flooring",
            "city": "Nagpur",
            "finish_tier": "standard",
            "rate": 80.0,
            "unit": "sqft",
            "quantity": 1575.0,
            "total_cost": 126000.0,
        },
        {
            "material": "bricks",
            "city": "Nagpur",
            "finish_tier": "standard",
            "rate": 9.0,
            "unit": "piece",
            "quantity": 46829.0,
            "total_cost": 421461.0,
        },
        {
            "material": "reinforcement_steel",
            "city": "Nagpur",
            "finish_tier": "standard",
            "rate": 65.0,
            "unit": "kg",
            "quantity": 6300.0,
            "total_cost": 409500.0,
        },
    ]

    result = calculator.calculate_total_material_cost(
        material_costs
    )

    assert result == 956961.0


def test_layout_quantities_are_compatible_with_cost_calculator():
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

    quantity_calculator = QuantityCalculator()

    quantities = quantity_calculator.calculate_layout(
        project,
        layout,
    )

    cost_calculator = CostCalculator()

    result = cost_calculator.calculate_material_summary(
        materials=quantities["materials"],
        city=project["city"],
        finish_tier=project["finish_tier"],
    )

    assert result["total_material_cost"] > 0
    assert len(result["items"]) > 0

    materials = {
        item["material"]
        for item in result["items"]
    }

    assert "flooring" in materials
    assert "cement" in materials
    assert "sand" in materials
    assert "aggregate" in materials
    assert "bricks" in materials
    assert "reinforcement_steel" in materials
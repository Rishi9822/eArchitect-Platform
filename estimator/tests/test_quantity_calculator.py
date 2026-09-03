from app.calculators.quantity_calculator import QuantityCalculator


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
from app.calculators.boq_calculator import BoQCalculator


def test_build_material_boq():
    calculator = BoQCalculator()

    material_costs = [
        {
            "material": "cement",
            "quantity": 100.0,
            "unit": "bag",
            "rate": 420.0,
            "total_cost": 42000.0,
            "breakdown": [
                {
                    "source": "concrete",
                    "quantity": 60.0,
                    "total_cost": 25200.0,
                },
                {
                    "source": "mortar",
                    "quantity": 40.0,
                    "total_cost": 16800.0,
                },
            ],
        }
    ]

    result = calculator.build_material_boq(material_costs)

    assert len(result) == 1
    assert result[0]["material"] == "cement"
    assert result[0]["quantity"] == 100.0
    assert result[0]["unit"] == "bag"
    assert result[0]["rate"] == 420.0
    assert result[0]["total_cost"] == 42000.0


def test_build_source_boq():
    calculator = BoQCalculator()

    material_costs = [
        {
            "material": "cement",
            "quantity": 100.0,
            "unit": "bag",
            "rate": 420.0,
            "total_cost": 42000.0,
            "breakdown": [
                {
                    "source": "concrete",
                    "quantity": 60.0,
                    "total_cost": 25200.0,
                },
                {
                    "source": "mortar",
                    "quantity": 40.0,
                    "total_cost": 16800.0,
                },
            ],
        }
    ]

    result = calculator.build_source_boq(material_costs)

    assert len(result) == 2

    concrete = next(
        item
        for item in result
        if item["source"] == "concrete"
    )

    mortar = next(
        item
        for item in result
        if item["source"] == "mortar"
    )

    assert concrete["materials"][0]["material"] == "cement"
    assert concrete["materials"][0]["quantity"] == 60.0
    assert concrete["total_cost"] == 25200.0

    assert mortar["materials"][0]["material"] == "cement"
    assert mortar["materials"][0]["quantity"] == 40.0
    assert mortar["total_cost"] == 16800.0


def test_build_boq_returns_both_views():
    calculator = BoQCalculator()

    material_costs = [
        {
            "material": "bricks",
            "quantity": 29264.0,
            "unit": "piece",
            "rate": 9.0,
            "total_cost": 263376.0,
            "breakdown": [
                {
                    "source": "direct",
                    "quantity": 29264,
                    "total_cost": 263376.0,
                }
            ],
        }
    ]

    result = calculator.build_boq(material_costs)

    assert "materials" in result
    assert "sources" in result

    assert len(result["materials"]) == 1
    assert len(result["sources"]) == 1

    assert result["materials"][0]["material"] == "bricks"
    assert result["sources"][0]["source"] == "direct"


def test_source_breakdown_matches_material_totals():
    calculator = BoQCalculator()

    material_costs = [
        {
            "material": "cement",
            "quantity": 493.54,
            "unit": "bag",
            "rate": 420.0,
            "total_cost": 207286.80,
            "breakdown": [
                {
                    "source": "concrete",
                    "quantity": 349.27,
                    "total_cost": 146693.40,
                },
                {
                    "source": "mortar",
                    "quantity": 89.76,
                    "total_cost": 37699.20,
                },
                {
                    "source": "plaster",
                    "quantity": 54.51,
                    "total_cost": 22894.20,
                },
            ],
        },
        {
            "material": "sand",
            "quantity": 50.525,
            "unit": "m3",
            "rate": 1800.0,
            "total_cost": 90945.0,
            "breakdown": [
                {
                    "source": "concrete",
                    "quantity": 24.255,
                    "total_cost": 43659.0,
                },
                {
                    "source": "mortar",
                    "quantity": 18.7,
                    "total_cost": 33660.0,
                },
                {
                    "source": "plaster",
                    "quantity": 7.57,
                    "total_cost": 13626.0,
                },
            ],
        },
    ]

    result = calculator.build_boq(material_costs)

    cement = next(
        item
        for item in result["materials"]
        if item["material"] == "cement"
    )

    cement_sources = [
        item
        for source in result["sources"]
        for item in source["materials"]
        if item["material"] == "cement"
    ]

    cement_quantity = round(
        sum(item["quantity"] for item in cement_sources),
        2,
    )

    cement_cost = round(
        sum(item["total_cost"] for item in cement_sources),
        2,
    )

    assert cement_quantity == cement["quantity"]
    assert cement_cost == cement["total_cost"]

    sand = next(
        item
        for item in result["materials"]
        if item["material"] == "sand"
    )

    sand_sources = [
        item
        for source in result["sources"]
        for item in source["materials"]
        if item["material"] == "sand"
    ]

    sand_quantity = round(
        sum(item["quantity"] for item in sand_sources),
        3,
    )

    sand_cost = round(
        sum(item["total_cost"] for item in sand_sources),
        2,
    )

    assert sand_quantity == sand["quantity"]
    assert sand_cost == sand["total_cost"]
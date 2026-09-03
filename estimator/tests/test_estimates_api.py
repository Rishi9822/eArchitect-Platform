from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


VALID_PROJECT = {
    "built_up_area_sqft": 1500,
    "wall_length_ft": 420,
    "ceiling_height_ft": 10,
    "rooms": 4,
    "bathrooms": 2,
    "wall_thickness_in": 9,
    "flooring": "standard",
    "city": "Nagpur",
    "finish_tier": "standard",
}


def test_quick_estimate_returns_success():
    response = client.post(
        "/api/v1/estimates/quick",
        json={"project": VALID_PROJECT},
    )

    assert response.status_code == 200


def test_quick_estimate_contains_expected_sections():
    response = client.post(
        "/api/v1/estimates/quick",
        json={"project": VALID_PROJECT},
    )

    data = response.json()

    assert data["mode"] == "quick"
    assert "project" in data
    assert "quantities" in data
    assert "material_costs" in data
    assert "labor" in data
    assert "waste" in data
    assert "cost_summary" in data


def test_quick_estimate_contains_steel_with_wastage():
    response = client.post(
        "/api/v1/estimates/quick",
        json={"project": VALID_PROJECT},
    )

    data = response.json()

    steel = next(
        item
        for item in data["quantities"]["materials"]
        if item["material"] == "reinforcement_steel"
    )

    assert steel["base_quantity"] == 6000.0
    assert steel["wastage_quantity"] == 300.0
    assert steel["total_quantity"] == 6300.0


def test_quick_estimate_has_zero_global_waste():
    response = client.post(
        "/api/v1/estimates/quick",
        json={"project": VALID_PROJECT},
    )

    data = response.json()

    assert data["waste"]["waste_cost"] == 0.0
    assert data["cost_summary"]["waste_cost"] == 0.0


def test_quick_estimate_rejects_invalid_project():
    invalid_project = {
        **VALID_PROJECT,
        "built_up_area_sqft": -100,
    }

    response = client.post(
        "/api/v1/estimates/quick",
        json={"project": invalid_project},
    )

    assert response.status_code == 422
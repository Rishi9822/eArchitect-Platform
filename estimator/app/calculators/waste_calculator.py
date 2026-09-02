class WasteCalculator:
    """
    Calculates additional waste cost for materials.

    Materials whose wastage is already included in the quantity
    calculation are excluded here to prevent double counting.
    """

    EXCLUDED_MATERIALS = {
        "flooring",
        "masonry",
    }

    DEFAULT_WASTE_PERCENT = 5.0

    def calculate_waste_cost(
        self,
        material_costs: list[dict],
        waste_percent: float = DEFAULT_WASTE_PERCENT,
    ) -> dict:
        """
        Calculate additional waste cost for eligible materials.
        """

        eligible_items = [
            item
            for item in material_costs
            if item["material"] not in self.EXCLUDED_MATERIALS
        ]

        base_cost = sum(
            item["total_cost"]
            for item in eligible_items
        )

        waste_cost = base_cost * (waste_percent / 100)

        return {
            "basis": "eligible_material_cost",
            "waste_percent": waste_percent,
            "eligible_material_cost": round(base_cost, 2),
            "waste_cost": round(waste_cost, 2),
        }
class WasteCalculator:
    """
    Reports additional waste cost.

    Material wastage is already handled by the quantity calculators,
    so no additional global waste percentage is applied here.
    """

    def calculate_waste_cost(
        self,
        material_costs: list[dict],
    ) -> dict:
        """
        Return zero additional waste cost because wastage
        is handled during quantity calculation.
        """

        return {
            "basis": "quantity_level_wastage",
            "waste_percent": 0.0,
            "eligible_material_cost": 0.0,
            "waste_cost": 0.0,
        }
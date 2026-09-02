class LaborCalculator:
    """
    Calculates estimated labor cost from material cost.

    This is an estimation-level approach. Actual labor cost
    can later be replaced with trade-wise regional labor rates.
    """

    DEFAULT_LABOR_PERCENT = 30.0

    def calculate_labor_cost(
        self,
        material_cost: float,
        labor_percent: float = DEFAULT_LABOR_PERCENT,
    ) -> dict:
        """
        Calculate labor cost as a percentage of material cost.
        """

        labor_cost = material_cost * (labor_percent / 100)

        return {
            "basis": "material_cost",
            "labor_percent": labor_percent,
            "material_cost": material_cost,
            "labor_cost": round(labor_cost, 2),
        }
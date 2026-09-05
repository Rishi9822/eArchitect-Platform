from app.calculators.cost_calculator import CostCalculator
from app.calculators.labor_calculator import LaborCalculator
from app.calculators.quantity_calculator import QuantityCalculator
from app.calculators.waste_calculator import WasteCalculator
from app.models.estimate import (
    LayoutEstimateRequest,
    QuickEstimateRequest,
)
from app.calculators.boq_calculator import BoQCalculator

from datetime import datetime, timezone
from uuid import uuid4


class EstimationService:
    """
    Coordinates the complete estimation workflow.
    """

    def __init__(self):
        self.quantity_calculator = QuantityCalculator()
        self.cost_calculator = CostCalculator()
        self.labor_calculator = LaborCalculator()
        self.waste_calculator = WasteCalculator()
        self.boq_calculator = BoQCalculator()

    def _create_metadata(self) -> dict:
        """
        Create metadata for a generated estimate.
        """

        return {
            "estimate_id": uuid4(),
            "created_at": datetime.now(timezone.utc),
            "currency": "INR",
        }

    def create_quick_estimate(
        self,
        request: QuickEstimateRequest,
    ) -> dict:
        """
        Create a complete quick construction estimate.
        """

        quantities = self.quantity_calculator.calculate_quick(
            request.project.model_dump()
        )    

        material_summary = self.cost_calculator.calculate_material_summary(
            materials=quantities["materials"],
            city=request.project.city,
            finish_tier=request.project.finish_tier,
        )

        boq = self.boq_calculator.build_boq(
            material_summary["items"]
        )

        labor = self.labor_calculator.calculate_labor_cost(
            material_cost=material_summary["total_material_cost"]
        )

        waste = self.waste_calculator.calculate_waste_cost(
            material_costs=material_summary["items"]
        )

        cost_summary = self.cost_calculator.calculate_cost_summary(
            material_cost=material_summary["total_material_cost"],
            labor_cost=labor["labor_cost"],
            waste_cost=waste["waste_cost"],
        )

        metadata = self._create_metadata()

        return {
            "mode": "quick",
            "project": request.project.model_dump(),
            "quantities": quantities,
            "material_costs": material_summary,
            "labor": labor,
            "waste": waste,
            "cost_summary": cost_summary,
            "boq": boq,
            "metadata": metadata,
        }

    def create_layout_estimate(
        self,
        request: LayoutEstimateRequest,
    ) -> dict:
        quantities = self.quantity_calculator.calculate_layout(
            request.project.model_dump(),
            request.layout.model_dump(),
        )

        material_summary = self.cost_calculator.calculate_material_summary(
            materials=quantities["materials"],
            city=request.project.city,
            finish_tier=request.project.finish_tier,
        )

        boq = self.boq_calculator.build_boq(
            material_summary["items"]
        )

        labor = self.labor_calculator.calculate_labor_cost(
            material_cost=material_summary["total_material_cost"]
        )

        waste = self.waste_calculator.calculate_waste_cost(
            material_costs=material_summary["items"]
        )

        cost_summary = self.cost_calculator.calculate_cost_summary(
            material_cost=material_summary["total_material_cost"],
            labor_cost=labor["labor_cost"],
            waste_cost=waste["waste_cost"],
        )

        metadata = self._create_metadata()

        return {
            "mode": "layout",
            "project": request.project.model_dump(),
            "layout_id": request.layout.id,
            "quantities": quantities,
            "material_costs": material_summary,
            "labor": labor,
            "waste": waste,
            "cost_summary": cost_summary,
            "boq": boq,
            "metadata": metadata,
        }
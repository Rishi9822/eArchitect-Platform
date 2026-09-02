from app.models.estimate import (
    LayoutEstimateRequest,
    QuickEstimateRequest,
)


class EstimationService:
    """
    Coordinates the estimation workflow.

    Calculation logic will be delegated to dedicated
    calculators as the estimator is developed.
    """

    def create_quick_estimate(
        self,
        request: QuickEstimateRequest,
    ) -> dict:
        """
        Create a quick estimate from project information.
        """

        return {
            "status": "received",
            "mode": "quick",
            "project": request.project.model_dump(),
        }

    def create_layout_estimate(
        self,
        request: LayoutEstimateRequest,
    ) -> dict:
        """
        Create an estimate from project information
        and a selected geometry-engine layout.
        """

        return {
            "status": "received",
            "mode": "layout",
            "project": request.project.model_dump(),
            "layout_id": request.layout.id,
        }
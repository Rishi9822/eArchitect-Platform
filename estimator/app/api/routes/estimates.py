from fastapi import APIRouter

from app.models.estimate import (
    EstimateResponse,
    LayoutEstimateRequest,
    QuickEstimateRequest,
)
from app.services.estimation_service import EstimationService


router = APIRouter(
    prefix="/api/v1/estimates",
    tags=["Estimates"],
)


estimation_service = EstimationService()


@router.post(
    "/quick",
    response_model=EstimateResponse,
)
def create_quick_estimate(request: QuickEstimateRequest):
    """
    Create a quick construction estimate.
    """

    return estimation_service.create_quick_estimate(request)


@router.post(
    "/layout",
    response_model=EstimateResponse,
)
def create_layout_estimate(request: LayoutEstimateRequest):
    """
    Create an estimate using a selected geometry-engine layout.
    """

    return estimation_service.create_layout_estimate(request)
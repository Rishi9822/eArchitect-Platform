from pydantic import BaseModel, Field

from app.models.layout import LayoutCandidate
from app.models.project import ProjectInput


class QuickEstimateRequest(BaseModel):
    """
    Request model for a quick construction estimate.

    No generated layout is required.
    """

    project: ProjectInput


class LayoutEstimateRequest(BaseModel):
    """
    Request model for estimating a selected geometry-engine layout.
    """

    project: ProjectInput

    layout: LayoutCandidate


class EstimateSummary(BaseModel):
    """
    High-level cost summary returned by the estimator.
    """

    material_cost: float = Field(
        ge=0,
        default=0,
    )

    labor_cost: float = Field(
        ge=0,
        default=0,
    )

    waste_cost: float = Field(
        ge=0,
        default=0,
    )

    subtotal: float = Field(
        ge=0,
        default=0,
    )

    total_cost: float = Field(
        ge=0,
        default=0,
    )
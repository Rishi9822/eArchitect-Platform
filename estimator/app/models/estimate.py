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


class BoQMaterialItem(BaseModel):
    """
    Consolidated material-level Bill of Quantities item.
    """

    material: str = Field(min_length=1)

    quantity: float = Field(
        ge=0,
    )

    unit: str = Field(min_length=1)

    rate: float = Field(
        ge=0,
    )

    total_cost: float = Field(
        ge=0,
    )


class BoQSourceMaterialItem(BaseModel):
    """
    Material cost contribution from a specific
    construction source such as concrete, mortar,
    or plaster.
    """

    material: str = Field(min_length=1)

    quantity: float = Field(
        ge=0,
    )

    unit: str = Field(min_length=1)

    rate: float = Field(
        ge=0,
    )

    total_cost: float = Field(
        ge=0,
    )


class BoQSourceItem(BaseModel):
    """
    Construction-source-level Bill of Quantities item.

    Examples of sources:
    - concrete
    - mortar
    - plaster
    - direct
    """

    source: str = Field(min_length=1)

    materials: list[BoQSourceMaterialItem] = Field(
        default_factory=list,
    )

    total_cost: float = Field(
        ge=0,
        default=0,
    )


class BoQ(BaseModel):
    """
    Bill of Quantities containing both material-level
    and construction-source-level views.
    """

    materials: list[BoQMaterialItem] = Field(
        default_factory=list,
    )

    sources: list[BoQSourceItem] = Field(
        default_factory=list,
    )

from datetime import datetime
from uuid import UUID


class EstimateMetadata(BaseModel):
    """
    Metadata identifying a generated estimate.
    """

    estimate_id: UUID

    created_at: datetime

    currency: str = Field(
        min_length=1,
        default="INR",
    )

class EstimateResponse(BaseModel):
    """
    Complete response returned by the estimator.
    """

    metadata: EstimateMetadata

    mode: str = Field(
        min_length=1,
    )

    project: dict

    layout_id: str | None = None

    quantities: dict

    material_costs: dict

    boq: BoQ

    labor: dict

    waste: dict

    cost_summary: EstimateSummary
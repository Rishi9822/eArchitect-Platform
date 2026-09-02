from typing import Any, Dict, List

from pydantic import BaseModel, Field


class LayoutCandidate(BaseModel):
    """
    Selected layout candidate produced by eArchitect-engine.

    The estimator does not generate or modify the geometry.
    It consumes the selected candidate as input for quantity estimation.
    """

    id: str = Field(
        min_length=1,
        description="Unique candidate ID from the geometry engine.",
    )

    strategy: str = Field(
        min_length=1,
        description="Layout generation strategy used by the engine.",
    )

    variation: str = Field(
        min_length=1,
        description="Candidate variation identifier.",
    )

    rooms: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Rooms contained in the selected layout.",
    )

    corridors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Corridors contained in the selected layout.",
    )

    walls: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Wall segments contained in the selected layout.",
    )

    doors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Doors contained in the selected layout.",
    )

    windows: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Windows contained in the selected layout.",
    )

    entrances: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Entrances contained in the selected layout.",
    )

    parking: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Parking areas contained in the selected layout.",
    )

    measurements: Dict[str, Any] = Field(
        default_factory=dict,
        description="Measurements calculated by the geometry engine.",
    )

    metrics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Layout metrics calculated by the geometry engine.",
    )

    score: Dict[str, Any] = Field(
        default_factory=dict,
        description="Layout quality scores calculated by the geometry engine.",
    )

    validation: Dict[str, Any] = Field(
        default_factory=dict,
        description="Layout validation results.",
    )
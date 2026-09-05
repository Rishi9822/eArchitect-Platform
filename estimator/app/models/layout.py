from typing import Any, Dict, List

from pydantic import BaseModel, Field


class LayoutCandidate(BaseModel):
    id: str = Field(min_length=1)
    strategy: str = Field(min_length=1)
    variation: str = Field(min_length=1)

    rooms: List[Dict[str, Any]] = Field(default_factory=list)
    corridors: List[Dict[str, Any]] = Field(default_factory=list)
    walls: List[Dict[str, Any]] = Field(default_factory=list)
    doors: List[Dict[str, Any]] = Field(default_factory=list)
    windows: List[Dict[str, Any]] = Field(default_factory=list)
    entrances: List[Dict[str, Any]] = Field(default_factory=list)
    parking: List[Dict[str, Any]] = Field(default_factory=list)
    dead_spaces: List[Dict[str, Any]] = Field(default_factory=list)

    circulation: Dict[str, Any] = Field(default_factory=dict)
    measurements: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    score: Dict[str, Any] = Field(default_factory=dict)
    validation: Dict[str, Any] = Field(default_factory=dict)
    timings: Dict[str, Any] = Field(default_factory=dict)

    rank: int | None = None
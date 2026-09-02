from typing import Literal

from pydantic import BaseModel, Field


class ProjectInput(BaseModel):
    """
    Common project information used by the estimator.
    """

    built_up_area_sqft: float = Field(
        gt=0,
        description="Built-up area in square feet.",
    )

    wall_length_ft: float = Field(
        gt=0,
        description="Total wall length in feet.",
    )

    ceiling_height_ft: float = Field(
        gt=0,
        description="Ceiling height in feet.",
    )

    rooms: int = Field(
        ge=1,
        description="Total number of rooms.",
    )

    bathrooms: int = Field(
        ge=0,
        description="Total number of bathrooms.",
    )

    wall_thickness_in: float = Field(
        gt=0,
        description="Wall thickness in inches.",
    )

    flooring: Literal[
        "standard",
        "premium",
        "luxury",
    ] = Field(
        default="standard",
        description="Flooring finish level.",
    )

    city: str = Field(
        min_length=1,
        description="Project city used for regional pricing.",
    )

    finish_tier: Literal[
        "standard",
        "premium",
        "luxury",
    ] = Field(
        default="standard",
        description="Overall construction finish tier.",
    )
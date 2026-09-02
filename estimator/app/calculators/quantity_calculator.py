from typing import Any, Dict

from app.core.constants import (
    CEMENT_BAG_WEIGHT_KG,
    DEFAULT_BRICK_HEIGHT_M,
    DEFAULT_BRICK_LENGTH_M,
    DEFAULT_BRICK_WIDTH_M,
    DEFAULT_CONCRETE_CEMENT_RATIO,
    DEFAULT_CONCRETE_DRY_VOLUME_FACTOR,
    DEFAULT_CONCRETE_SAND_RATIO,
    DEFAULT_CONCRETE_VOLUME_M3_PER_SQFT,
    DEFAULT_FLOORING_WASTAGE_PERCENT,
    DEFAULT_MASONRY_WASTAGE_PERCENT,
    DEFAULT_MORTAR_JOINT_M,
    DEFAULT_STEEL_KG_PER_SQFT,
    DEFAULT_PLASTER_THICKNESS_M,
    DEFAULT_CONCRETE_AGGREGATE_RATIO,
    SQFT_TO_SQM,
)


class QuantityCalculator:
    """
    Calculates construction material quantities.
    """

    def calculate_flooring_quantity(
        self,
        floor_area_sqft: float,
    ) -> Dict[str, Any]:
        """
        Calculate flooring quantity including wastage.

        Parameters
        ----------
        floor_area_sqft:
            Floor area in square feet.

        Returns
        -------
        Dictionary containing usable area, wastage,
        and total flooring quantity.
        """

        if floor_area_sqft <= 0:
            raise ValueError("Floor area must be greater than zero.")

        wastage_area_sqft = (
            floor_area_sqft
            * DEFAULT_FLOORING_WASTAGE_PERCENT
            / 100
        )

        total_area_sqft = (
            floor_area_sqft
            + wastage_area_sqft
        )

        return {
            "material": "flooring",
            "base_quantity": round(floor_area_sqft, 2),
            "base_unit": "sqft",
            "wastage_percent": DEFAULT_FLOORING_WASTAGE_PERCENT,
            "wastage_quantity": round(wastage_area_sqft, 2),
            "total_quantity": round(total_area_sqft, 2),
            "total_unit": "sqft",
            "total_quantity_sqm": round(
                total_area_sqft * SQFT_TO_SQM,
                2,
            ),
        }

    def calculate_masonry_quantity(
        self,
        wall_length_ft: float,
        wall_height_ft: float,
        wall_thickness_in: float,
    ) -> Dict[str, Any]:
        """
        Calculate masonry wall volume including wastage.

        This is an estimation-level masonry volume calculation.
        Openings such as doors and windows are not deducted here yet.
        """

        if wall_length_ft <= 0:
            raise ValueError("Wall length must be greater than zero.")

        if wall_height_ft <= 0:
            raise ValueError("Wall height must be greater than zero.")

        if wall_thickness_in <= 0:
            raise ValueError("Wall thickness must be greater than zero.")

        wall_length_m = wall_length_ft * 0.3048
        wall_height_m = wall_height_ft * 0.3048
        wall_thickness_m = wall_thickness_in * 0.0254

        wall_volume_m3 = (
            wall_length_m
            * wall_height_m
            * wall_thickness_m
        )

        wastage_volume_m3 = (
            wall_volume_m3
            * DEFAULT_MASONRY_WASTAGE_PERCENT
            / 100
        )

        total_volume_m3 = (
            wall_volume_m3
            + wastage_volume_m3
        )

        return {
            "material": "masonry",
            "base_quantity": round(wall_volume_m3, 3),
            "base_unit": "m3",
            "wastage_percent": DEFAULT_MASONRY_WASTAGE_PERCENT,
            "wastage_quantity": round(wastage_volume_m3, 3),
            "total_quantity": round(total_volume_m3, 3),
            "total_unit": "m3",
        }

    def calculate_brick_quantity(
        self,
        masonry_volume_m3: float,
    ) -> Dict[str, Any]:
        """
        Estimate the number of bricks required for a given
        masonry volume.

        The calculation uses the nominal brick dimensions plus
        mortar joint allowance.

        This is an estimation quantity, not a final procurement quantity.
        """

        if masonry_volume_m3 <= 0:
            raise ValueError(
                "Masonry volume must be greater than zero."
            )

        brick_module_length_m = (
            DEFAULT_BRICK_LENGTH_M
            + DEFAULT_MORTAR_JOINT_M
        )

        brick_module_width_m = (
            DEFAULT_BRICK_WIDTH_M
            + DEFAULT_MORTAR_JOINT_M
        )

        brick_module_height_m = (
            DEFAULT_BRICK_HEIGHT_M
            + DEFAULT_MORTAR_JOINT_M
        )

        brick_module_volume_m3 = (
            brick_module_length_m
            * brick_module_width_m
            * brick_module_height_m
        )

        brick_count = (
            masonry_volume_m3
            / brick_module_volume_m3
        )

        return {
            "material": "bricks",
            "masonry_volume": round(
                masonry_volume_m3,
                3,
            ),
            "masonry_volume_unit": "m3",
            "brick_count": round(
                brick_count,
            ),
            "brick_unit": "pieces",
            "brick_dimensions": {
                "length_m": DEFAULT_BRICK_LENGTH_M,
                "width_m": DEFAULT_BRICK_WIDTH_M,
                "height_m": DEFAULT_BRICK_HEIGHT_M,
            },
            "mortar_joint_m": DEFAULT_MORTAR_JOINT_M,
        }

    def calculate_steel_quantity(
        self,
        built_up_area_sqft: float,
    ) -> Dict[str, Any]:
        """
        Estimate reinforcement steel quantity from built-up area.

        This is an estimation allowance only.
        Actual reinforcement quantities must come from structural design.
        """

        if built_up_area_sqft <= 0:
            raise ValueError(
                "Built-up area must be greater than zero."
            )

        steel_quantity_kg = (
            built_up_area_sqft
            * DEFAULT_STEEL_KG_PER_SQFT
        )

        steel_quantity_tonnes = (
            steel_quantity_kg / 1000
        )

        return {
            "material": "reinforcement_steel",
            "quantity": round(
                steel_quantity_kg,
                2,
            ),
            "unit": "kg",
            "quantity_tonnes": round(
                steel_quantity_tonnes,
                3,
            ),
            "rate": DEFAULT_STEEL_KG_PER_SQFT,
            "rate_unit": "kg_per_sqft",
            "basis": "built_up_area",
            "assumption": True,
        }


    def calculate_concrete_volume(
        self,
        built_up_area_sqft: float,
    ) -> Dict[str, Any]:
        """
        Estimate concrete volume from built-up area.

        This is an estimation-level allowance and is not a
        structural design calculation.
        """

        if built_up_area_sqft <= 0:
            raise ValueError(
                "Built-up area must be greater than zero."
            )

        concrete_volume_m3 = (
            built_up_area_sqft
            * DEFAULT_CONCRETE_VOLUME_M3_PER_SQFT
        )

        return {
            "material": "concrete",
            "base_quantity": round(
                concrete_volume_m3,
                3,
            ),
            "base_unit": "m3",
            "basis": "built_up_area",
            "rate": DEFAULT_CONCRETE_VOLUME_M3_PER_SQFT,
            "rate_unit": "m3_per_sqft",
            "assumption": True,
        }

    def calculate_concrete_materials(
        self,
        concrete_volume_m3: float,
    ) -> Dict[str, Any]:
        """
        Convert concrete volume into estimated cement, sand,
        and aggregate quantities using the configured mix ratio.

        This is an estimation-level calculation and not a
        structural mix-design calculation.
        """

        if concrete_volume_m3 <= 0:
            raise ValueError(
                "Concrete volume must be greater than zero."
            )

        dry_volume = (
            concrete_volume_m3
            * DEFAULT_CONCRETE_DRY_VOLUME_FACTOR
        )

        cement_ratio = DEFAULT_CONCRETE_CEMENT_RATIO
        sand_ratio = DEFAULT_CONCRETE_SAND_RATIO
        aggregate_ratio = DEFAULT_CONCRETE_AGGREGATE_RATIO

        total_ratio = (
            cement_ratio
            + sand_ratio
            + aggregate_ratio
        )

        cement_volume_m3 = (
            dry_volume
            * cement_ratio
            / total_ratio
        )

        sand_volume_m3 = (
            dry_volume
            * sand_ratio
            / total_ratio
        )

        aggregate_volume_m3 = (
            dry_volume
            * aggregate_ratio
            / total_ratio
        )

        cement_weight_kg = (
            cement_volume_m3
            * 1440
        )

        cement_bags = (
            cement_weight_kg
            / CEMENT_BAG_WEIGHT_KG
        )

        return {
            "concrete_volume": round(
                concrete_volume_m3,
                3,
            ),
            "concrete_volume_unit": "m3",

            "dry_volume": round(
                dry_volume,
                3,
            ),
            "dry_volume_unit": "m3",

            "cement": {
                "quantity": round(
                    cement_bags,
                    2,
                ),
                "unit": "bags",
                "volume_m3": round(
                    cement_volume_m3,
                    3,
                ),
                "weight_kg": round(
                    cement_weight_kg,
                    2,
                ),
            },

            "sand": {
                "quantity": round(
                    sand_volume_m3,
                    3,
                ),
                "unit": "m3",
            },

            "aggregate": {
                "quantity": round(
                    aggregate_volume_m3,
                    3,
                ),
                "unit": "m3",
            },

            "mix_ratio": (
                f"{cement_ratio}:"
                f"{sand_ratio}:"
                f"{aggregate_ratio}"
            ),

            "dry_volume_factor": (
                DEFAULT_CONCRETE_DRY_VOLUME_FACTOR
            ),

            "assumption": True,
        }

    def calculate_plaster_quantity(
        self,
        wall_length_ft: float,
        wall_height_ft: float,
    ) -> Dict[str, Any]:
        """
        Calculate gross plaster quantity for both sides of walls.

        This is an estimation-level calculation.
        Door and window opening deductions will be handled separately
        when actual layout geometry is available.
        """

        if wall_length_ft <= 0:
            raise ValueError("Wall length must be greater than zero.")

        if wall_height_ft <= 0:
            raise ValueError("Wall height must be greater than zero.")

        wall_length_m = wall_length_ft * 0.3048
        wall_height_m = wall_height_ft * 0.3048

        gross_wall_area_sqm = (
            wall_length_m
            * wall_height_m
            * 2
        )

        plaster_thickness_m = DEFAULT_PLASTER_THICKNESS_M

        plaster_volume_m3 = (
            gross_wall_area_sqm
            * plaster_thickness_m
        )

        return {
            "material": "plaster",
            "wall_surface_area": round(
                gross_wall_area_sqm,
                2,
            ),
            "surface_area_unit": "sqm",
            "plaster_thickness": plaster_thickness_m,
            "thickness_unit": "m",
            "base_quantity": round(
                plaster_volume_m3,
                3,
            ),
            "base_unit": "m3",
        }

    def calculate_quick(
        self,
        project: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate material quantities for a quick estimate.
        """

        flooring = self.calculate_flooring_quantity(
            project["built_up_area_sqft"]
        )

        masonry = self.calculate_masonry_quantity(
            project["wall_length_ft"],
            project["ceiling_height_ft"],
            project["wall_thickness_in"],
        )

        bricks = self.calculate_brick_quantity(
            masonry["total_quantity"]
        )

        plaster = self.calculate_plaster_quantity(
            project["wall_length_ft"],
            project["ceiling_height_ft"],
        )

        concrete = self.calculate_concrete_volume(
            project["built_up_area_sqft"]
        )

        concrete_materials = self.calculate_concrete_materials(
            concrete["base_quantity"]
        )

        concrete.update(concrete_materials)

        steel = self.calculate_steel_quantity(
            project["built_up_area_sqft"]
        )

        return {
            "mode": "quick",
            "materials": [
                flooring,
                masonry,
                bricks,
                plaster,
                concrete,
                steel,
            ],
            "assumptions": [
                {
                    "name": "flooring_wastage",
                    "value": DEFAULT_FLOORING_WASTAGE_PERCENT,
                    "unit": "percent",
                },
                {
                    "name": "masonry_wastage",
                    "value": DEFAULT_MASONRY_WASTAGE_PERCENT,
                    "unit": "percent",
                },
                {
                    "name": "plaster_thickness",
                    "value": DEFAULT_PLASTER_THICKNESS_M,
                    "unit": "m",
                },
            ],
        }

    def calculate_layout(
        self,
        project: Dict[str, Any],
        layout: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate material quantities using the selected
        geometry-engine layout.
        """

        measurements = layout.get("measurements", {})

        floor_area_sqft = measurements.get("floor_area_sqft")

        if not floor_area_sqft:
            floor_area_sqft = measurements.get(
                "built_up_area_sqft"
            )

        if not floor_area_sqft:
            raise ValueError(
                "Layout does not contain a usable floor area."
            )

        flooring = self.calculate_flooring_quantity(
            floor_area_sqft
        )

        return {
            "mode": "layout",
            "materials": [
                flooring,
            ],
            "assumptions": [
                {
                    "name": "flooring_wastage",
                    "value": DEFAULT_FLOORING_WASTAGE_PERCENT,
                    "unit": "percent",
                }
            ],
        }
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
    DEFAULT_MORTAR_RATIO_CEMENT,
    DEFAULT_MORTAR_RATIO_SAND,
    DEFAULT_STEEL_KG_PER_SQFT,
    DEFAULT_PLASTER_CEMENT_RATIO,
    DEFAULT_PLASTER_SAND_RATIO,
    DEFAULT_PLASTER_THICKNESS_M,
    DEFAULT_CONCRETE_AGGREGATE_RATIO,
    SQFT_TO_SQM,
    FT_TO_M,
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

    def calculate_mortar_quantity(
        self,
        masonry_volume_m3: float,
        brick_count: int,
    ) -> dict:
        """
        Estimate masonry mortar and its cement/sand components.

        This is an estimation-level calculation. Mortar wastage is
        applied once to the base mortar volume.
        """

        brick_volume = (
            brick_count
            * DEFAULT_BRICK_LENGTH_M
            * DEFAULT_BRICK_WIDTH_M
            * DEFAULT_BRICK_HEIGHT_M
        )

        base_mortar_volume = max(
            masonry_volume_m3 - brick_volume,
            0.0,
        )

        wastage_quantity = (
            base_mortar_volume
            * DEFAULT_MASONRY_WASTAGE_PERCENT
            / 100
        )

        total_mortar_volume = (
            base_mortar_volume + wastage_quantity
        )

        dry_volume = (
            total_mortar_volume
            * DEFAULT_CONCRETE_DRY_VOLUME_FACTOR
        )

        total_ratio = (
            DEFAULT_MORTAR_RATIO_CEMENT
            + DEFAULT_MORTAR_RATIO_SAND
        )

        cement_volume = (
            dry_volume
            * DEFAULT_MORTAR_RATIO_CEMENT
            / total_ratio
        )

        sand_volume = (
            dry_volume
            * DEFAULT_MORTAR_RATIO_SAND
            / total_ratio
        )

        cement_weight_kg = cement_volume * 1440.0
        cement_bags = cement_weight_kg / CEMENT_BAG_WEIGHT_KG

        return {
            "material": "mortar",
            "base_quantity": round(base_mortar_volume, 3),
            "base_unit": "m3",
            "wastage_percent": DEFAULT_MASONRY_WASTAGE_PERCENT,
            "wastage_quantity": round(wastage_quantity, 3),
            "total_quantity": round(total_mortar_volume, 3),
            "total_unit": "m3",
            "dry_volume": round(dry_volume, 3),
            "dry_volume_unit": "m3",
            "cement": {
                "quantity": round(cement_bags, 2),
                "unit": "bags",
                "volume_m3": round(cement_volume, 3),
                "weight_kg": round(cement_weight_kg, 2),
            },
            "sand": {
                "quantity": round(sand_volume, 3),
                "unit": "m3",
            },
            "mix_ratio": "1:6",
            "dry_volume_factor": DEFAULT_CONCRETE_DRY_VOLUME_FACTOR,
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
            "wastage_included": True,
            "wastage_source": "masonry",
        }

    def calculate_steel_quantity(
        self,
        built_up_area_sqft: float,
    ) -> dict:
        if built_up_area_sqft <= 0:
            raise ValueError(
                "Built-up area must be greater than zero."
            )

        base_quantity = (
            built_up_area_sqft * DEFAULT_STEEL_KG_PER_SQFT
        )

        wastage_percent = 5.0
        wastage_quantity = base_quantity * wastage_percent / 100
        total_quantity = base_quantity + wastage_quantity

        return {
            "material": "reinforcement_steel",
            "base_quantity": round(base_quantity, 2),
            "base_unit": "kg",
            "wastage_percent": wastage_percent,
            "wastage_quantity": round(wastage_quantity, 2),
            "total_quantity": round(total_quantity, 2),
            "total_unit": "kg",
            "quantity_tonnes": round(total_quantity / 1000, 3),
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

        wastage_percent = 5.0
        wastage_quantity = (
            concrete_volume_m3
            * wastage_percent
            / 100
        )

        total_quantity = (
            concrete_volume_m3
            + wastage_quantity
        )

        return {
            "material": "concrete",
            "base_quantity": round(
                concrete_volume_m3,
                3,
            ),
            "base_unit": "m3",
            "wastage_percent": wastage_percent,
            "wastage_quantity": round(
                wastage_quantity,
                3,
            ),
            "total_quantity": round(
                total_quantity,
                3,
            ),
            "total_unit": "m3",
            "basis": "built_up_area",
            "rate": DEFAULT_CONCRETE_VOLUME_M3_PER_SQFT,
            "rate_unit": "m3_per_sqft",
            "assumption": True,
        }
    def calculate_concrete_materials(self, concrete_volume_m3: float) -> dict:
        wastage_percent = 5.0
        wastage_quantity = concrete_volume_m3 * wastage_percent / 100
        total_concrete_volume = concrete_volume_m3 + wastage_quantity

        dry_volume = (
            total_concrete_volume
            * DEFAULT_CONCRETE_DRY_VOLUME_FACTOR
        )

        total_ratio = (
            DEFAULT_CONCRETE_CEMENT_RATIO
            + DEFAULT_CONCRETE_SAND_RATIO
            + DEFAULT_CONCRETE_AGGREGATE_RATIO
        )

        cement_volume = (
            dry_volume
            * DEFAULT_CONCRETE_CEMENT_RATIO
            / total_ratio
        )

        sand_volume = (
            dry_volume
            * DEFAULT_CONCRETE_SAND_RATIO
            / total_ratio
        )

        aggregate_volume = (
            dry_volume
            * DEFAULT_CONCRETE_AGGREGATE_RATIO
            / total_ratio
        )

        cement_weight_kg = cement_volume * 1440.0
        cement_bags = cement_weight_kg / CEMENT_BAG_WEIGHT_KG

        return {
            "material": "concrete",
            "base_quantity": round(concrete_volume_m3, 3),
            "base_unit": "m3",
            "wastage_percent": wastage_percent,
            "wastage_quantity": round(wastage_quantity, 3),
            "total_quantity": round(total_concrete_volume, 3),
            "total_unit": "m3",
            "dry_volume": round(dry_volume, 3),
            "dry_volume_unit": "m3",
            "cement": {
                "quantity": round(cement_bags, 2),
                "unit": "bags",
                "volume_m3": round(cement_volume, 3),
                "weight_kg": round(cement_weight_kg, 2),
            },
            "sand": {
                "quantity": round(sand_volume, 3),
                "unit": "m3",
            },
            "aggregate": {
                "quantity": round(aggregate_volume, 3),
                "unit": "m3",
            },
            "mix_ratio": "1:2:4",
            "dry_volume_factor": DEFAULT_CONCRETE_DRY_VOLUME_FACTOR,
        }

    def calculate_plaster_quantity(
        self,
        wall_length_ft: float,
        wall_height_ft: float,
    ) -> Dict[str, Any]:
        """
        Calculate gross plaster quantity for both sides of walls
        and estimate cement/sand components using a 1:4 mix ratio.

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

        wastage_quantity = (
            plaster_volume_m3
            * DEFAULT_MASONRY_WASTAGE_PERCENT
            / 100
        )

        total_plaster_volume_m3 = (
            plaster_volume_m3
            + wastage_quantity
        )

        dry_volume = (
            total_plaster_volume_m3
            * DEFAULT_CONCRETE_DRY_VOLUME_FACTOR
        )

        cement_ratio = DEFAULT_PLASTER_CEMENT_RATIO
        sand_ratio = DEFAULT_PLASTER_SAND_RATIO

        total_ratio = (
            cement_ratio
            + sand_ratio
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

        cement_weight_kg = cement_volume_m3 * 1440.0

        cement_bags = (
            cement_weight_kg
            / CEMENT_BAG_WEIGHT_KG
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
                        "wastage_percent": DEFAULT_MASONRY_WASTAGE_PERCENT,
            "wastage_quantity": round(
                wastage_quantity,
                3,
            ),
            "total_quantity": round(
                total_plaster_volume_m3,
                3,
            ),
            "total_unit": "m3",
            
            "base_unit": "m3",
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
            "mix_ratio": (
                f"{cement_ratio}:"
                f"{sand_ratio}"
            ),
            "dry_volume_factor": (
                DEFAULT_CONCRETE_DRY_VOLUME_FACTOR
            ),
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

        mortar = self.calculate_mortar_quantity(
            masonry["total_quantity"],
            bricks["brick_count"],
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
                mortar,
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
                    "name": "concrete_wastage",
                    "value": 5.0,
                    "unit": "percent",
                },
                {
                    "name": "reinforcement_steel_wastage",
                    "value": 5.0,
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

        built_up_area_sqft = measurements.get(
            "built_up_area_sqft"
        )

        if not built_up_area_sqft:
            raise ValueError(
                "Layout does not contain a usable built-up area."
            )

        flooring = self.calculate_flooring_quantity(
            floor_area_sqft
        )

        concrete = self.calculate_concrete_volume(
        built_up_area_sqft
        )
        concrete_materials = self.calculate_concrete_materials(
        concrete["base_quantity"]
        )
        concrete.update(concrete_materials)

        steel = self.calculate_steel_quantity(
            built_up_area_sqft
        )

        total_wall_length_m = measurements.get(
            "total_wall_length_m"
        )

        if not total_wall_length_m:
            raise ValueError(
                "Layout does not contain a usable total wall length."
            )

        wall_length_ft = total_wall_length_m / FT_TO_M

        masonry = self.calculate_masonry_quantity(
            wall_length_ft=wall_length_ft,
            wall_height_ft=project["ceiling_height_ft"],
            wall_thickness_in=project["wall_thickness_in"],
        )


        brick_count = self.calculate_brick_quantity(
        masonry["total_quantity"]
        )

        mortar = self.calculate_mortar_quantity(
        masonry_volume_m3=masonry["total_quantity"],
        brick_count=brick_count["brick_count"],
        )

        plaster = self.calculate_plaster_quantity(
        wall_length_ft=wall_length_ft,
        wall_height_ft=project["ceiling_height_ft"],
        )

        return {
            "mode": "layout",
            "materials": [
                flooring,
                concrete,
                steel,
                masonry,
                brick_count,
                mortar,
                plaster,
            ],
            "assumptions": [
                {
                    "name": "flooring_wastage",
                    "value": DEFAULT_FLOORING_WASTAGE_PERCENT,
                    "unit": "percent",
                },
                {
                    "name": "concrete_wastage",
                    "value": 5.0,
                    "unit": "percent",
                },
                {
                    "name": "reinforcement_steel_wastage",
                    "value": 5.0,
                    "unit": "percent",
                },
            ],
        }
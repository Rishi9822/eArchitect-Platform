"""
Centralized estimator constants.

These values are intentionally kept separate from calculation logic.
They represent assumptions that can later be calibrated against
regional construction standards and pricing data.
"""

# Unit conversions

SQFT_TO_SQM = 0.092903
SQM_TO_SQFT = 10.7639

FT_TO_M = 0.3048
IN_TO_M = 0.0254

# Standard material units

CEMENT_BAG_WEIGHT_KG = 50.0


# Construction quantity assumptions
#
# These are estimation-level assumptions, not structural design values.
# They should be configurable/calibratable in future versions.

# Masonry

DEFAULT_BRICK_LENGTH_M = 0.19
DEFAULT_BRICK_WIDTH_M = 0.09
DEFAULT_BRICK_HEIGHT_M = 0.09

DEFAULT_MORTAR_JOINT_M = 0.01
DEFAULT_MORTAR_RATIO_CEMENT = 1
DEFAULT_MORTAR_RATIO_SAND = 6

# Concrete

DEFAULT_CONCRETE_VOLUME_M3_PER_SQFT = 0.035
DEFAULT_CONCRETE_DRY_VOLUME_FACTOR = 1.54

DEFAULT_CONCRETE_CEMENT_RATIO = 1
DEFAULT_CONCRETE_SAND_RATIO = 2
DEFAULT_CONCRETE_AGGREGATE_RATIO = 4

# Flooring

DEFAULT_FLOORING_WASTAGE_PERCENT = 5.0

# Plaster

DEFAULT_PLASTER_THICKNESS_M = 0.012
DEFAULT_PLASTER_CEMENT_RATIO = 1
DEFAULT_PLASTER_SAND_RATIO = 4

# Paint

DEFAULT_PAINT_COATS = 2
DEFAULT_PAINT_COVERAGE_SQM_PER_LITRE = 10.0
DEFAULT_PAINT_WASTAGE_PERCENT = 5.0

# Reinforcement steel
#
# This is only an estimation allowance.
# Actual reinforcement must come from structural design.

DEFAULT_STEEL_KG_PER_SQFT = 4.0

# General wastage

DEFAULT_MASONRY_WASTAGE_PERCENT = 5.0
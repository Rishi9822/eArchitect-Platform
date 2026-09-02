"""
Regional construction material rates.

These are initial estimation rates and should be treated as
configurable pricing data rather than fixed market prices.
"""

MATERIAL_RATES = {
    "Nagpur": {
        "cement": {
            "standard": 420.0,
            "premium": 450.0,
            "luxury": 480.0,
            "unit": "bag",
        },
        "bricks": {
            "standard": 9.0,
            "premium": 11.0,
            "luxury": 14.0,
            "unit": "piece",
        },
        "sand": {
            "standard": 1800.0,
            "premium": 2100.0,
            "luxury": 2400.0,
            "unit": "m3",
        },
        "aggregate": {
            "standard": 1600.0,
            "premium": 1850.0,
            "luxury": 2100.0,
            "unit": "m3",
        },
        "reinforcement_steel": {
            "standard": 65.0,
            "premium": 70.0,
            "luxury": 75.0,
            "unit": "kg",
        },
        "flooring": {
            "standard": 80.0,
            "premium": 140.0,
            "luxury": 250.0,
            "unit": "sqft",
        },
        "masonry": {
            "standard": 1800.0,
            "premium": 2100.0,
            "luxury": 2400.0,
            "unit": "m3",
        },
       "plaster": {
           "standard": 2200.0,
           "premium": 2600.0,
           "luxury": 3000.0,
           "unit": "m3",
        },  
    }
}
from typing import Any, Dict, List


class BoQCalculator:
    """
    Builds material-level and source-level Bills of Quantities
    from the material cost summary produced by CostCalculator.
    """

    def build_material_boq(
        self,
        material_costs: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Build the consolidated material-level BoQ.

        Each item represents one material with its total
        required quantity, unit rate, and total cost.
        """

        return [
            {
                "material": item["material"],
                "quantity": item["quantity"],
                "unit": item["unit"],
                "rate": item["rate"],
                "total_cost": item["total_cost"],
            }
            for item in material_costs
        ]

    def build_source_boq(
        self,
        material_costs: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Build the construction-source-level BoQ.

        Source-level entries preserve where each material
        contribution comes from, such as concrete, mortar,
        plaster, or direct.
        """

        sources: Dict[str, Dict[str, Any]] = {}

        for item in material_costs:
            material = item["material"]

            for breakdown in item.get("breakdown", []):
                source = breakdown["source"]

                if source not in sources:
                    sources[source] = {
                        "source": source,
                        "materials": [],
                        "total_cost": 0.0,
                    }

                sources[source]["materials"].append(
                    {
                        "material": material,
                        "quantity": breakdown["quantity"],
                        "unit": item["unit"],
                        "rate": item["rate"],
                        "total_cost": breakdown["total_cost"],
                    }
                )

                sources[source]["total_cost"] += (
                    breakdown["total_cost"]
                )

        for source in sources.values():
            source["total_cost"] = round(
                source["total_cost"],
                2,
            )

        return list(sources.values())

    def build_boq(
        self,
        material_costs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Build both material-level and source-level BoQ views.
        """

        return {
            "materials": self.build_material_boq(
                material_costs
            ),
            "sources": self.build_source_boq(
                material_costs
            ),
        }
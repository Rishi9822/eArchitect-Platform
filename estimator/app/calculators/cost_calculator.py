from app.core.rates import MATERIAL_RATES


class CostCalculator:
    """
    Calculates construction material costs using
    regional and finish-tier based rates.
    """

    def get_rate(
        self,
        city: str,
        material: str,
        finish_tier: str,
    ) -> dict:
        """
        Return the configured rate for a material.
        """

        city_rates = MATERIAL_RATES.get(city)

        if not city_rates:
            raise ValueError(
                f"Pricing is not available for city: {city}"
            )

        material_rate = city_rates.get(material)

        if not material_rate:
            raise ValueError(
                f"Pricing is not available for material: {material}"
            )

        rate = material_rate.get(finish_tier)

        if rate is None:
            raise ValueError(
                f"Pricing is not available for "
                f"{material} with finish tier: {finish_tier}"
            )

        return {
            "material": material,
            "city": city,
            "finish_tier": finish_tier,
            "rate": rate,
            "unit": material_rate["unit"],
        }

    def calculate_cost(
        self,
        quantity: float,
        city: str,
        material: str,
        finish_tier: str,
    ) -> dict:
        """
        Calculate total cost for a material quantity.
        """

        rate_info = self.get_rate(
            city=city,
            material=material,
            finish_tier=finish_tier,
        )

        total_cost = quantity * rate_info["rate"]

        return {
            **rate_info,
            "quantity": quantity,
            "total_cost": round(total_cost, 2),
        }

    def calculate_material_costs(
        self,
        materials: list[dict],
        city: str,
        finish_tier: str,
    ) -> list[dict]:
        """
        Calculate costs for all supported materials
        returned by the quantity calculator.
        """

        costs = []

        for material_data in materials:
            material = material_data.get("material")

            if not material:
                continue

            quantity = None

            if material == "masonry":
                continue


            elif material == "bricks":
                quantity = material_data.get("brick_count")

            elif material == "plaster":
                plaster_materials = []

                cement = material_data.get("cement", {})
                sand = material_data.get("sand", {})

                if cement.get("quantity") is not None:
                    plaster_materials.append(
                        {
                            **self.calculate_cost(
                                quantity=cement["quantity"],
                                city=city,
                                material="cement",
                                finish_tier=finish_tier,
                            ),
                            "source": "plaster",
                        }
                    )

                if sand.get("quantity") is not None:
                    plaster_materials.append(
                        {
                            **self.calculate_cost(
                                quantity=sand["quantity"],
                                city=city,
                                material="sand",
                                finish_tier=finish_tier,
                            ),
                            "source": "plaster",
                        }
                    )

                costs.extend(plaster_materials)
                continue

            elif material == "mortar":
                mortar_materials = []

                cement = material_data.get("cement", {})
                sand = material_data.get("sand", {})

                if cement.get("quantity") is not None:
                    mortar_materials.append(
                        {
                        **self.calculate_cost(
                            quantity=cement["quantity"],
                            city=city,
                            material="cement",
                            finish_tier=finish_tier,
                        ),
                        "source": "mortar",
                        }
                    )

                if sand.get("quantity") is not None:
                    mortar_materials.append(
                        {
                        **self.calculate_cost(
                            quantity=sand["quantity"],
                            city=city,
                            material="sand",
                            finish_tier=finish_tier,
                        ),
                        "source": "mortar",
                        }
                    )

                costs.extend(mortar_materials)
                continue

            elif material == "concrete":
                concrete_materials = []

                cement = material_data.get("cement", {})
                sand = material_data.get("sand", {})
                aggregate = material_data.get("aggregate", {})

                if cement.get("quantity") is not None:
                    concrete_materials.append(
                        {
                        **self.calculate_cost(
                            quantity=cement["quantity"],
                            city=city,
                            material="cement",
                            finish_tier=finish_tier,
                        ),
                        "source": "concrete",
                        }
                    )

                if sand.get("quantity") is not None:
                    concrete_materials.append(
                        {
                        **self.calculate_cost(
                            quantity=sand["quantity"],
                            city=city,
                            material="sand",
                            finish_tier=finish_tier,
                        ),
                        "source": "concrete",
                        }
                    )

                if aggregate.get("quantity") is not None:
                    concrete_materials.append(
                        {
                        **self.calculate_cost(
                            quantity=aggregate["quantity"],
                            city=city,
                            material="aggregate",
                            finish_tier=finish_tier,
                        ),
                        "source": "concrete",
                        }
                    )

                costs.extend(concrete_materials)
                continue

            elif material == "reinforcement_steel":
                quantity = material_data.get("total_quantity")

            elif "total_quantity" in material_data:
                quantity = material_data["total_quantity"]

            if quantity is None:
                continue

            costs.append(
                self.calculate_cost(
                    quantity=quantity,
                    city=city,
                    material=material,
                    finish_tier=finish_tier,
                )
            )

        return costs

    def aggregate_material_costs(
        self,
        material_costs: list[dict],
    ) -> list[dict]:
        """
        Aggregate duplicate material cost entries while
        preserving the source breakdown.
        """

        aggregated = {}

        for item in material_costs:
            material = item["material"]

            if material not in aggregated:
                aggregated[material] = {
                    "material": material,
                    "city": item["city"],
                    "finish_tier": item["finish_tier"],
                    "rate": item["rate"],
                    "unit": item["unit"],
                    "quantity": 0.0,
                    "total_cost": 0.0,
                    "breakdown": [],
                }

            aggregated[material]["quantity"] += item["quantity"]
            aggregated[material]["total_cost"] += item["total_cost"]

            aggregated[material]["breakdown"].append(
                {
                    "source": item.get("source", "direct"),
                    "quantity": item["quantity"],
                    "total_cost": item["total_cost"],
                }
            )

        for item in aggregated.values():
            item["quantity"] = round(item["quantity"], 3)
            item["total_cost"] = round(item["total_cost"], 2)

        return list(aggregated.values())

    def calculate_total_material_cost(
        self,
        material_costs: list[dict],
    ) -> float:
        """
        Calculate the total cost of all materials.
        """

        return round(
            sum(item["total_cost"] for item in material_costs),
            2,
        )


    def calculate_material_summary(
        self,
        materials: list[dict],
        city: str,
        finish_tier: str,
    ) -> dict:
        """
        Calculate material-level costs and aggregate
        duplicate material entries.
        """

        material_costs = self.calculate_material_costs(
            materials=materials,
            city=city,
            finish_tier=finish_tier,
        )

        aggregated_material_costs = self.aggregate_material_costs(
            material_costs
        )

        total_material_cost = self.calculate_total_material_cost(
            aggregated_material_costs
        )

        return {
            "items": aggregated_material_costs,
            "total_material_cost": total_material_cost,
        }


    def calculate_cost_summary(
        self,
        material_cost: float,
        labor_cost: float,
        waste_cost: float = 0.0,
    ) -> dict:
        """
        Calculate the overall construction cost summary.
        """

        subtotal = material_cost + labor_cost
        total_cost = subtotal + waste_cost

        return {
            "material_cost": round(material_cost, 2),
            "labor_cost": round(labor_cost, 2),
            "waste_cost": round(waste_cost, 2),
            "subtotal": round(subtotal, 2),
            "total_cost": round(total_cost, 2),
        }
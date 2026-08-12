import math
from typing import Dict, Any

class PassportWaterEngine:
    def __init__(self, currency: str = "USD"):
        self.currency = currency

    def calculate_virtual_water_factor(
        self, 
        evapotranspiration_m3_ha: float, 
        crop_yield_ton_ha: float
    ) -> float:
        """Formula: VWF = Evapotranspiration / Yield (m3 / metric ton)"""
        if crop_yield_ton_ha <= 0:
            raise ValueError("Crop yield must be greater than zero.")
        return round(evapotranspiration_m3_ha / crop_yield_ton_ha, 2)

    def calculate_implicit_water_value_index(
        self,
        virtual_water_factor: float,
        baseline_water_stress: float,
        local_tariff_m3: float,
        alpha_multiplier: float = 1.25
    ) -> float:
        """Formula: IWVI = Tariff + ((BWS / 5.0)^2 * alpha * (1000 / VWF))"""
        if virtual_water_factor <= 0:
            return 0.0
            
        scarcity_weight = math.pow(baseline_water_stress / 5.0, 2)
        iwvi = local_tariff_m3 + (scarcity_weight * alpha_multiplier * (1000 / virtual_water_factor))
        return round(iwvi, 4)

    def evaluate_arbitrage_delta(
        self,
        source_iwvi: float,
        destination_iwvi: float,
        volume_m3: float
    ) -> Dict[str, float]:
        """Quantifies the economic value spread via Virtual Water Arbitrage (VWA)."""
        value_spread = destination_iwvi - source_iwvi
        total_arbitrage_alpha = value_spread * volume_m3
        return {
            "value_spread_per_m3": round(value_spread, 4),
            "total_arbitrage_alpha": round(total_arbitrage_alpha, 2),
            "viability_index": 1.0 if value_spread > 0.50 else 0.0
        }
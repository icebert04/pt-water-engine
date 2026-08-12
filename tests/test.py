import sys
import os

# Adds the parent directory (pt-water-engine) to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.calculators import PassportWaterEngine
from data_pipeliners.wri_aqueduct import WRIAqueductConnector

def run_integration_test():
    # Initialize Engine & API Connector
    engine = PassportWaterEngine(currency="USD")
    wri_connector = WRIAqueductConnector()

    print("=== 1. FETCHING LIVE WATERSHED RISK METRICS ===")
    # Fresno, Central Valley, California (High Stress Region)
    fresno_lat, fresno_lon = 36.74, -119.78
    fresno_data = wri_connector.get_basin_scarcity_metrics(fresno_lat, fresno_lon)
    
    print(f"Location: Fresno, CA ({fresno_lat}, {fresno_lon})")
    print(f"Data Source : {fresno_data['data_source']}")
    print(f"BWS Score   : {fresno_data['baseline_water_stress']}")
    print(f"Risk Label  : {fresno_data['basin_label']}\n")

    print("=== 2. CALCULATING IMPLICIT WATER VALUE INDEX (IWVI) ===")
    # Inputs: 3000 m3/ha evapotranspiration, 1.5 ton/ha yield -> VWF = 2000 m3/ton
    vwf = engine.calculate_virtual_water_factor(evapotranspiration_m3_ha=3000.0, crop_yield_ton_ha=1.5)
    fresno_iwvi = engine.calculate_implicit_water_value_index(
        virtual_water_factor=vwf,
        baseline_water_stress=fresno_data["baseline_water_stress"],
        local_tariff_m3=0.50
    )
    print(f"Virtual Water Factor (VWF) : {vwf} m3/ton")
    print(f"Fresno IWVI Risk Value     : ${fresno_iwvi} / m3\n")

    print("=== 3. EVALUATING VIRTUAL WATER ARBITRAGE (VWA) ===")
    # Low-stress source region (e.g., IWVI = $0.55/m3)
    source_iwvi = 0.55
    volume_m3 = 50000.0  # 50,000 m3 volume
    arbitrage = engine.evaluate_arbitrage_delta(source_iwvi, fresno_iwvi, volume_m3)

    print(f"Source IWVI Spread         : ${arbitrage['value_spread_per_m3']} / m3")
    print(f"Total Arbitrage Value      : ${arbitrage['total_arbitrage_alpha']}")
    print(f"Viable Opportunity?        : {'YES' if arbitrage['viability_index'] == 1.0 else 'NO'}")

# --- EXECUTION / TESTING BLOCK ---
if __name__ == "__main__":
    # 1. Create an instance of your connector
    connector = WRIAqueductConnector()

    # 2. Define test coordinates (Fresno, California)
    fresno_lat, fresno_lon = 36.74, -119.78

    # 3. Call the method
    print("Fetching data from ArcGIS...\n")
    result = connector.get_basin_scarcity_metrics(latitude=fresno_lat, longitude=fresno_lon)

    # 4. Print the output dictionary
    import json
    print(json.dumps(result, indent=2))
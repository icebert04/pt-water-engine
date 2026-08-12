# PT Water Engine (`pt-water-engine`) 🐢💧

The open-source core data engine powering **Passport Turtles** (`passportturtles.com`).

This engine ingests spatial hydrological datasets from the **WRI Aqueduct 4.0 Atlas** and remote-sensing evapotranspiration metrics from the **UN FAO WaPOR portal** to compute localized **Virtual Water Factors (VWF)** and calculate the **Implicit Water Value Index (IWVI™)** for global enterprise supply chains.

## Core Capabilities

- **Volumetric Footprinting:** Standardized parsing of Green, Blue, and Grey water lifecycles using the ISO 14046 benchmark framework.
- **Regulatory Risk Translation:** Automated conversion of raw physical watershed scarcity metrics into localized risk-adjusted economic indicators.
- **Arbitrage Modeling:** Real-time value spread identification to support strategic **Virtual Water Arbitrage (VWA™)** routing.

## Quick Start (Python 3.10+)

```bash
git clone https://github.com
cd pt-water-engine
pip install -r requirements.txt
pytest tests/
```

## Institutional Alignment

Our software layer maps directly to global open-access standards, utilizing the official [FAO WaPOR Applications Framework](https://fao.org) and the data schemas established by the [World Resources Institute](https://wri.org).

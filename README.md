# Live Battery Monitoring System (Demo)

A starter project for a Formula Student battery dashboard until real STM32 and CAN Bus data are available.

This version uses:
- Python
- Streamlit
- Fake (simulated) data

Later, you can replace the fake source with:
- STM32 serial data
- CAN Bus frames
- DALY BMS values

## Features

- Live battery metrics (Voltage, Current, Temperature, SOC)
- Fault detection (High Temperature, Low Voltage, High Current)
- Live charts (Voltage, Temperature, Current)
- Battery charge gauge
- Battery pack information table
- Auto-refresh dashboard (1 second)

## Project Structure

- app.py: Main Streamlit dashboard application
- requirements.txt: Python dependencies

## Requirements

- Python 3.10+
- pip

## Setup

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install streamlit pandas plotly
```

## Run

From the project folder:

```bash
streamlit run app.py
```

Streamlit opens in your browser automatically.

## How It Works

In app.py, fake values are generated every cycle and stored in Streamlit session state.
Only the latest 20 points are kept for each time series.
The app reruns every second to simulate a live telemetry stream.

## Replacing Fake Data With Real Data

Current simulated section is the generate_fake_data function in app.py.

Example current pattern:

```python
readings = generate_fake_data()
voltage = readings["voltage"]
current = readings["current"]
temperature = readings["temperature"]
soc = readings["soc"]
```

Later, replace that with values read from your real interface (UART/USB/CAN parser), for example:

```python
readings = read_from_stm32_or_can()
voltage = readings["voltage"]
current = readings["current"]
temperature = readings["temperature"]
soc = readings["soc"]
```

No dashboard architecture change is required if the dictionary format stays the same.

## Next STM32 Integration Phase

1. Read CAN Bus data on STM32.
2. Send parsed values over UART or USB.
3. Parse incoming data in Python.
4. Feed parsed values into the same dashboard variables.

## Future Enhancements

- CAN Bus direct integration on PC
- Data logging to CSV/SQLite
- Fault history timeline
- Alerts/notifications
- Mobile-ready dashboard view
- GPS and lap telemetry integration
- Cooling system and relay status blocks
- Emergency shutdown status

## Notes

This repo is intentionally structured to scale from:
Fake Data -> STM32 Data -> CAN Bus -> Full Telemetry System.

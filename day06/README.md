# 🏕️ Weather-Based Camping Predictor

A Python command-line tool that downloads a real-time 7-day weather forecast and
analyses it to recommend which days of the week are best suited for outdoor camping.

---

## About the Data Source - Open-Meteo

[Open-Meteo](https://open-meteo.com/) is a free, open-source weather API designed for
non-commercial use. It aggregates data from several national meteorological services
(ECMWF, NOAA, DWD, and others) and exposes a clean REST interface that requires **no
API key or account**.

---

## How the Program Works

### 1. Data Download (`fetch_forecast`)

`main.py` sends an HTTP GET request to the Open-Meteo `/v1/forecast` endpoint with
the desired coordinates and a list of daily variables. The response is a JSON object
containing parallel arrays — one value per day for each requested variable.  
No API key is needed; the only dependency is the `requests` library.

### 2. Data Processing (`evaluate_day` + `analyse_forecast`)

Each day is scored out of **5 stars** using the following camping-comfort rules:

| Condition | Penalty |
|---|---|
| Rain > 3 mm | −2 stars |
| Rain 0–3 mm | −1 star |
| Wind > 30 km/h | −1 star |
| Max temp > 36 °C | −2 stars |
| Min temp < 8 °C | −1 star |
| Thunderstorm (WMO ≥ 95) | Score forced to 0 |

The score maps to a human verdict: **Excellent (5) → Good (4) → Fair (3) → Poor (2) → Avoid (0–1)**.

### 3. Report (`print_report`)

The script prints a day-by-day table with emoji indicators, temperature range,
precipitation, wind, a star-rating, and a list of specific reasons for each verdict.
A final summary highlights the best and worst days of the week.

---

## How to run

```bash
# 1. Clone / download the project files
# 2. Install the single dependency
pip install -r requirements.txt

# 3. Run the predictor (default location: Ashdod, Israel)
python main.py
```

To forecast a different location, open `main.py` and change the three constants near
the top of the file:

```python
LATITUDE      = 48.8566   # Paris, France
LONGITUDE     = 2.3522
LOCATION_NAME = "Paris, France"
```

### Example Output

```
==============================================================
  🏕️  CAMPING WEATHER FORECAST — Ashdod, Israel
  📅  Generated on 18 May 2025
==============================================================

Monday 2025-05-18  🌟 EXCELLENT
  Condition : Mainly clear
  Temp      : 17.3 °C – 26.8 °C
  Rain      : 0.0 mm    |    Wind: 18 km/h
  Score     : ★★★★★  (5/5)
  ✅ Conditions look stable

...

==============================================================
  SUMMARY
==============================================================

  🌟 Best days to camp  : Monday, Tuesday, Thursday
  ❌ Days to avoid      : Saturday
==============================================================
```

---

## Project Structure

```
.
├── main.py           
├── requirements.txt  
└── README.md         
```

---

## AI Interaction Disclosure

This project was developed with the assistance of **Claude (Anthropic)**

1. My Project Idea: I want to build a Weather-Based Camping Predictor using a free, open scientific weather database (like Open-Meteo API or OpenWeatherMap).

3. I described the program requirements

4. I described the goal and output request
---

## Requirements

- Python 3.10 or newer (uses `list[dict]` type hints — PEP 585)
- Internet connection (to reach `api.open-meteo.com`)
- `requests` library (see `requirements.txt`)

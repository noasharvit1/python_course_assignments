"""
Weather-Based Camping Predictor
================================
Downloads a 7-day weather forecast from the Open-Meteo API (https://open-meteo.com/)
and analyses each day to recommend which days are best suited for outdoor camping.

Usage:
    python main.py

No API key is required — Open-Meteo is a free, open-source weather API.
"""

import sys
import requests
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration — change LATITUDE / LONGITUDE to forecast for any location.
# ---------------------------------------------------------------------------
LATITUDE = 31.8  # Default: Be'er Sheva area, Israel
LONGITUDE = 34.65
LOCATION_NAME = "Ashdod, Israel"

# Open-Meteo endpoint for daily forecast variables
API_URL = "https://api.open-meteo.com/v1/forecast"

# Camping comfort thresholds
MAX_RAIN_MM = 3.0          # More than 3 mm of rain → avoid camping
MAX_WIND_KMH = 30.0        # Wind above 30 km/h → uncomfortably windy
MIN_TEMP_C = 8.0           # Below 8 °C at night → too cold without specialised gear
MAX_TEMP_C = 36.0          # Above 36 °C in the day → dangerously hot
IDEAL_MAX_TEMP_C = 28.0    # ≤ 28 °C → ideal daytime temperature


def fetch_forecast(lat: float, lon: float) -> dict:
    """
    Request a 7-day daily forecast from Open-Meteo.

    Parameters
    ----------
    lat : float  — latitude of the target location
    lon : float  — longitude of the target location

    Returns
    -------
    dict — parsed JSON response from the API
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
            "weathercode",
        ],
        "timezone": "auto",          # let the API pick the local timezone
        "forecast_days": 7,
    }

    print(f"Fetching 7-day forecast for {LOCATION_NAME} …\n")

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()  # raises HTTPError for 4xx / 5xx responses
    except requests.exceptions.ConnectionError:
        sys.exit("Error: Could not reach the Open-Meteo API. Check your internet connection.")
    except requests.exceptions.Timeout:
        sys.exit("Error: The request timed out. Try again later.")
    except requests.exceptions.HTTPError as exc:
        sys.exit(f"Error: API returned an error — {exc}")

    return response.json()


def decode_weather_code(code: int) -> str:
    """
    Translate a WMO Weather Interpretation Code into a human-readable string.

    Reference: https://open-meteo.com/en/docs (section 'WMO Weather Codes')
    """
    wmo_descriptions = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Icy fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
    }
    return wmo_descriptions.get(code, f"Weather code {code}")


def evaluate_day(
    date_str: str,
    temp_max: float,
    temp_min: float,
    rain_mm: float,
    wind_kmh: float,
    weather_code: int,
) -> dict:
    """
    Apply camping-suitability logic to a single day's forecast.

    Returns a dict with keys:
        date        — ISO date string
        day_name    — full weekday name (e.g. 'Monday')
        temp_max    — maximum temperature (°C)
        temp_min    — minimum temperature (°C)
        rain_mm     — total precipitation (mm)
        wind_kmh    — maximum wind speed (km/h)
        condition   — WMO weather description
        score       — integer 0–5 (higher = better for camping)
        verdict     — short label: 'Excellent', 'Good', 'Fair', 'Poor', 'Avoid'
        reasons     — list of human-readable reason strings
    """
    score = 5          # start with a perfect score and subtract for each issue
    reasons = []
    warnings = []

    # --- Rain check ---
    if rain_mm > MAX_RAIN_MM:
        score -= 2
        warnings.append(f"⚠️  Heavy rain expected ({rain_mm:.1f} mm)")
    elif rain_mm > 0:
        score -= 1
        reasons.append(f"☁️  Light precipitation possible ({rain_mm:.1f} mm)")

    # --- Wind check ---
    if wind_kmh > MAX_WIND_KMH:
        score -= 1
        warnings.append(f"⚠️  High winds ({wind_kmh:.0f} km/h)")
    elif wind_kmh > 20:
        reasons.append(f"🌬️  Moderate breeze ({wind_kmh:.0f} km/h)")

    # --- Temperature (day) check ---
    if temp_max > MAX_TEMP_C:
        score -= 2
        warnings.append(f"⚠️  Extreme heat ({temp_max:.1f} °C) — dangerous outdoors")
    elif temp_max <= IDEAL_MAX_TEMP_C:
        reasons.append(f"☀️  Pleasant daytime high ({temp_max:.1f} °C)")

    # --- Temperature (night) check ---
    if temp_min < MIN_TEMP_C:
        score -= 1
        warnings.append(f"⚠️  Cold night ({temp_min:.1f} °C) — warm sleeping gear required")

    # --- Thunderstorm is an automatic disqualifier ---
    if weather_code >= 95:
        score = 0
        warnings.append("⛈️  Thunderstorm forecast — camping strongly inadvisable")

    # Clamp score to [0, 5]
    score = max(0, score)

    # Map numeric score to a human verdict
    if score == 5:
        verdict = "Excellent"
    elif score == 4:
        verdict = "Good"
    elif score == 3:
        verdict = "Fair"
    elif score == 2:
        verdict = "Poor"
    else:
        verdict = "Avoid"

    # If no positive observations were recorded, add a neutral note
    if not reasons and not warnings:
        reasons.append("✅ Conditions look stable")

    return {
        "date": date_str,
        "day_name": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
        "temp_max": temp_max,
        "temp_min": temp_min,
        "rain_mm": rain_mm,
        "wind_kmh": wind_kmh,
        "condition": decode_weather_code(weather_code),
        "score": score,
        "verdict": verdict,
        "reasons": warnings + reasons,   # warnings listed first
    }


def analyse_forecast(data: dict) -> list[dict]:
    """
    Iterate over the daily forecast arrays returned by Open-Meteo
    and evaluate each day for camping suitability.

    Returns a list of evaluation dicts (one per day).
    """
    daily = data["daily"]

    days = []
    for i, date in enumerate(daily["time"]):
        day_eval = evaluate_day(
            date_str=date,
            temp_max=daily["temperature_2m_max"][i],
            temp_min=daily["temperature_2m_min"][i],
            rain_mm=daily["precipitation_sum"][i],
            wind_kmh=daily["windspeed_10m_max"][i],
            weather_code=daily["weathercode"][i],
        )
        days.append(day_eval)

    return days


def verdict_emoji(verdict: str) -> str:
    """Return a colourful emoji that matches the camping verdict."""
    return {
        "Excellent": "🌟",
        "Good":      "✅",
        "Fair":      "🟡",
        "Poor":      "🟠",
        "Avoid":     "❌",
    }.get(verdict, "")


def print_report(days: list[dict]) -> None:
    """
    Print a formatted camping-suitability report to the terminal.
    """
    separator = "=" * 62

    print(separator)
    print(f"  🏕️  CAMPING WEATHER FORECAST — {LOCATION_NAME}")
    print(f"  📅  Generated on {datetime.now().strftime('%d %B %Y')}")
    print(separator)

    for day in days:
        emoji = verdict_emoji(day["verdict"])
        print(f"\n{day['day_name']} {day['date']}  {emoji} {day['verdict'].upper()}")
        print(f"  Condition : {day['condition']}")
        print(f"  Temp      : {day['temp_min']:.1f} °C – {day['temp_max']:.1f} °C")
        print(f"  Rain      : {day['rain_mm']:.1f} mm    |    Wind: {day['wind_kmh']:.0f} km/h")
        print(f"  Score     : {'★' * day['score']}{'☆' * (5 - day['score'])}  ({day['score']}/5)")
        if day["reasons"]:
            for reason in day["reasons"]:
                print(f"  {reason}")

    # --- Summary: best and worst days ---
    print(f"\n{separator}")
    print("  SUMMARY")
    print(separator)

    best_days = [d for d in days if d["verdict"] in ("Excellent", "Good")]
    avoid_days = [d for d in days if d["verdict"] in ("Poor", "Avoid")]

    if best_days:
        names = ", ".join(d["day_name"] for d in best_days)
        print(f"\n  🌟 Best days to camp  : {names}")
    else:
        print("\n  🌟 No ideal camping days this week.")

    if avoid_days:
        names = ", ".join(d["day_name"] for d in avoid_days)
        print(f"  ❌ Days to avoid      : {names}")
    else:
        print("  ❌ No days to avoid this week — enjoy!")

    print(f"\n{separator}\n")


def main() -> None:
    """Entry point — orchestrates download, analysis, and reporting."""
    # 1. Download forecast data from Open-Meteo
    raw_data = fetch_forecast(LATITUDE, LONGITUDE)

    # 2. Analyse each day for camping suitability
    evaluated_days = analyse_forecast(raw_data)

    # 3. Print the user-friendly report
    print_report(evaluated_days)


if __name__ == "__main__":
    main()

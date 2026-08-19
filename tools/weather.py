import requests


def get_weather(city: str):
    """Get current weather for a city using Open-Meteo."""

    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {
                "success": False,
                "error": f"Could not find the city '{city}'."
            }

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                "timezone": "auto"
            },
            timeout=10
        )

        weather_response.raise_for_status()

        weather = weather_response.json()["current"]

        return {
            "success": True,
            "city": location["name"],
            "country": location.get("country"),
            "temperature_c": weather["temperature_2m"],
            "humidity_percent": weather["relative_humidity_2m"],
            "wind_speed_kmh": weather["wind_speed_10m"],
            "timezone": weather.get("timezone")
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Weather service unavailable: {str(e)}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected weather error: {str(e)}"
        }
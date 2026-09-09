import requests

from langchain_core.tools import tool


@tool
def weather_tool(city: str) -> str:
    """
    Get current weather information for a city.

    Example:
    Kuala Lumpur
    Singapore
    Tokyo
    """

    try:
        geocode_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
        )

        geo_response = requests.get(
            geocode_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )

        geo_data = geo_response.json()

        results = geo_data.get("results")

        if not results:
            return f"Could not find location: {city}"

        location = results[0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        location_name = location.get("name", city)
        country = location.get("country", "")

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "apparent_temperature,"
                    "relative_humidity_2m,"
                    "weather_code"
                ),
            },
            timeout=10,
        )

        weather_data = weather_response.json()
        current = weather_data.get("current", {})

        temperature = current.get("temperature_2m")
        feels_like = current.get("apparent_temperature")
        humidity = current.get("relative_humidity_2m")
        weather_code = current.get("weather_code")

        return f"""
Location: {location_name}, {country}
Temperature: {temperature} °C
Feels Like: {feels_like} °C
Humidity: {humidity} %
Weather Code: {weather_code}
"""

    except Exception as e:
        return (
            "Weather information is temporarily unavailable. "
            f"Error: {str(e)}"
        )

import requests


def get_weather(city: str):
    try:
        url = f"https://wttr.in/{city}?format=j1"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {
                "success": False,
                "error": "Unable to get weather information."
            }

        data = response.json()

        current = data["current_condition"][0]

        return {
            "success": True,
            "city": city,
            "temperature": current["temp_C"] + " °C",
            "condition": current["weatherDesc"][0]["value"]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
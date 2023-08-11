from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests


def get_picture_data(query):
    url = f"https://api.pexels.com/v1/search?query={query}"
    headers = {
        "Authorization": PEXELS_API_KEY
    }

    response = requests.get(url, headers=headers)
    api_dictionary = response.json()
    return api_dictionary["photos"][0]["src"]["original"]


def get_weather_data(city, state):

    url_one = "http://api.openweathermap.org/geo/1.0/direct"
    #set the parameters for the LON and LAT request
    params = {
        "q": f"{city},{state},US", # Query includes city, state, and country code (US)
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,#Adds the
    }
    response = requests.get(url_one, params=params)
    content = response.json()
    try:
        latitutde = content[0]["lat"]
        longitude = content[0]["lon"]
    except (KeyError, IndexError):
        return None

    params = {
        "lat": latitutde,
        "lon": longitude,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }
    url_two = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url_two, params=params)
    content = response.json()
    return {
        "description": content["weather"][0]["description"],
        "temperature": content["main"]["temp"],
    }

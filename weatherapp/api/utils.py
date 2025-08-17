import requests
from django.conf import settings

OWM_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
OWM_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"  # 5-day / 3-hour
OWM_GEOCODE = "http://api.openweathermap.org/geo/1.0/direct"        # q -> lat/lon
OWM_REVERSE = "http://api.openweathermap.org/geo/1.0/reverse"       # lat/lon -> place

class ApiError(Exception):
    pass


def geocode_location(query: str, limit: int = 1):
    params = {"q": query, "limit": limit, "appid": settings.OPENWEATHER_API_KEY}
    r = requests.get(OWM_GEOCODE, params=params, timeout=15)
    if r.status_code != 200:
        raise ApiError(f"Geocode failed: {r.text}")
    data = r.json()
    if not data:
        return None
    top = data[0]
    name = ", ".join([p for p in [top.get("name"), top.get("state"), top.get("country")] if p])
    return {"lat": top["lat"], "lon": top["lon"], "label": name}


def reverse_geocode(lat: float, lon: float):
    params = {"lat": lat, "lon": lon, "limit": 1, "appid": settings.OPENWEATHER_API_KEY}
    r = requests.get(OWM_REVERSE, params=params, timeout=15)
    if r.status_code != 200:
        raise ApiError(f"Reverse geocode failed: {r.text}")
    data = r.json()
    if not data:
        return None
    top = data[0]
    name = ", ".join([p for p in [top.get("name"), top.get("state"), top.get("country")] if p])
    return name


def fetch_current(lat: float, lon: float, units: str = "metric"):
    params = {"lat": lat, "lon": lon, "appid": settings.OPENWEATHER_API_KEY, "units": units}
    r = requests.get(OWM_WEATHER, params=params, timeout=20)
    if r.status_code != 200:
        raise ApiError(r.json().get("message", r.text))
    return r.json()


def fetch_forecast(lat: float, lon: float, units: str = "metric"):
    params = {"lat": lat, "lon": lon, "appid": settings.OPENWEATHER_API_KEY, "units": units}
    r = requests.get(OWM_FORECAST, params=params, timeout=20)
    if r.status_code != 200:
        raise ApiError(r.json().get("message", r.text))
    return r.json()


def youtube_search(location_label: str, max_results: int = 5):
    key = settings.YOUTUBE_API_KEY
    if not key:
        return {"error": "YOUTUBE_API_KEY not set"}
    q = f"{location_label} travel weather"
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": q,
        "type": "video",
        "maxResults": max_results,
        "key": key,
        "safeSearch": "moderate",
    }
    r = requests.get(url, params=params, timeout=20)
    return r.json()


